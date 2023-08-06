# -*- coding: utf-8 -*-


import datetime as dt
from toolz import merge
import time
import pandas as pd
import functools
from sqlalchemy.exc import (ProgrammingError,
                            OperationalError)
from ct_manager.pg import PGDataHandler
from ct_manager.oracle import (WindDataHandler,
                               XRiskDataHandler)
from ct_manager.uqer import UqerDataHandler
from ct_manager.base_handler import SimpleDataHanlder
from ct_manager.enums import (SWIndustryLevel,
                              PriceAdjMethod,
                              PriceType,
                              TrackingStrategy,
                              DataSource)
from ct_manager.utils import (process_date,
                              universe_ticker,
                              ensure_list)
from ct_manager.const import FUT_MULTI
from ct_manager.settings import SettingsFactory
from argcheck import *
from xutils import (Date,
                    Calendar,
                    Period,
                    BizDayConventions,
                    CustomLogger)

__all__ = ['contrib_process',
           'set_ramp_user',
           'ramp_read',
           'ramp_execute',
           'set_xrisk_user',
           'set_xrisk_password',
           'get_industry',
           'universe',
           'get_index_industry_weight',
           'get_ptf_industry_weight',
           'get_ptf_detail',
           'get_equity_market_cob',
           'get_equity_market',
           'get_equity_return',
           'get_equity_price',
           'get_strat_signal',
           'construct_portfolio_by_weight',
           'evaluate_portfolio_by_weight',
           'exclude_ticker_by_status',
           'check_status',
           'table_fields',
           'default_ref_date']

PCT_THRESH = 9.5



def contrib_process(data_source=DataSource.WIND_ORACLE_LOCAL, contrib_dest=DataSource.CT_PGSQL_LOCAL, logger=None):
    """
    decorator of contribution to pg database with various sources, with functionality of logger
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 得到数据源
            if data_source == DataSource.CT_PGSQL_LOCAL:
                source_handler = PGDataHandler()
            elif data_source == DataSource.WIND_ORACLE_LOCAL:
                source_handler = WindDataHandler()
            elif data_source == DataSource.UQER:
                source_handler = UqerDataHandler()
            elif data_source == DataSource.XRisk_ORACLE_LOCAL:
                source_handler = XRiskDataHandler()
            else:
                source_handler = None

            # 创建目标源
            if contrib_dest == DataSource.CT_PGSQL_LOCAL:
                contrib_handler = PGDataHandler()
            else:
                contrib_handler = SimpleDataHanlder(contrib_dest)

            kwargs = (merge(merge(kwargs, {'contrib_handler': contrib_handler}), {'source_handler': source_handler}))

            if logger is not None:
                logger.info('Contribution source - {source}'.format(source=data_source))
                logger.info('Contribution process {func_name} runs at time {runtime}'.
                            format(func_name=func.__name__,
                                   runtime=time.asctime(time.localtime(time.time()))))

            ret = func(*args, **kwargs)

            if logger is not None:
                logger.info('Contribution process {func_name} finishes at time {runtime}'.
                            format(func_name=func.__name__,
                                   runtime=time.asctime(time.localtime(time.time()))))

            if contrib_handler is not None:
                contrib_handler.close()

            if source_handler is not None:
                source_handler.close()

            return ret

        return wrapper

    return decorator


def set_ramp_user(user_name):
    SettingsFactory.ramp_user = user_name
    return


def ramp_read(script):
    pg_handler = PGDataHandler()
    ret = pg_handler.df_read_sql(script)
    pg_handler.close()
    return ret


def ramp_execute(script):
    pg_handler = PGDataHandler()
    pg_handler.execute(script)
    pg_handler.close()
    return


def set_xrisk_user(user_name):
    SettingsFactory.xrisk_user = user_name
    return


def set_xrisk_password(password):
    SettingsFactory.xrisk_password = password
    return


@preprocess(ticker=ensure_list)
def get_industry(ticker, sw_level=SWIndustryLevel.L1, ref_date=None):
    if not isinstance(ticker, list):
        ticker = list(ticker)
    ref_date = default_ref_date(ref_date)
    pg_handler = PGDataHandler()
    industry_map = pg_handler.get_industry_map(ref_date, sw_level=sw_level)
    ret = industry_map[industry_map['ticker'].isin(ticker)]
    ret.columns = ['ticker', 'name', 'industry_ticker', 'industry_name']
    pg_handler.close()
    return ret


def universe(ticker_or_name, ref_date=None, pandas_format=0):
    ticker = universe_ticker(ticker_or_name)
    ref_date = default_ref_date(ref_date)
    pg_handler = PGDataHandler()
    ret = pg_handler.get_index_component(ref_date=ref_date, index_ticker=ticker, out_weight=False)
    pg_handler.close()
    if not pandas_format:
        try:
            ret = ret['cons_ticker'].tolist()
        except KeyError:
            ret = ret['ticker'].tolist()
    return ret


def get_index_industry_weight(ticker_or_name, ref_date=None, sw_level=SWIndustryLevel.L1):
    ticker = universe_ticker(ticker_or_name)
    ref_date = default_ref_date(ref_date)
    pg_handler = PGDataHandler()
    index_compo = pg_handler.get_index_component(ref_date=ref_date, index_ticker=ticker, out_weight=True)
    index_compo.columns = ['ticker', 'weight']
    industry_map = pg_handler.get_industry_map(ref_date, sw_level=sw_level)
    industry_map.columns = ['ticker', 'name', 'industry_ticker', 'industry_name']
    ret = _lookup_industry(index_compo, industry_map)
    pg_handler.close()
    return ret


def get_ptf_industry_weight(ticker_and_weight, ref_date=None, sw_level=SWIndustryLevel.L1):
    pg_handler = PGDataHandler()
    ref_date = default_ref_date(ref_date)
    ptf = ticker_and_weight
    ptf.columns = ['ticker', 'weight']
    industry_map = pg_handler.get_industry_map(ref_date, sw_level=sw_level)
    industry_map.columns = ['ticker', 'name', 'industry_ticker', 'industry_name']
    ret = _lookup_industry(ptf, industry_map)
    pg_handler.close()
    return ret


def get_ptf_detail(ptf_name, start_date, end_date, **kwargs):
    return_info = kwargs.get('return_info', 'long_short')
    pg_handler = PGDataHandler()
    ret = pg_handler.get_portfolio_holding(ptf_name, start_date, end_date)

    def futures_multiplier(ticker):
        prefix = ticker[:2]
        try:
            return FUT_MULTI[prefix]
        except KeyError:
            return 1

    ret['holding'] = ret['holding'] * ret['ticker'].map(futures_multiplier)
    ret['mkt_value'] = ret['holding'] * ret['current_price']

    if return_info == 'total_holding':
        return ret
    elif return_info == 'equity_holding':
        return ret[ret['type'] == u'股票']
    elif return_info == 'equity_weight':
        equity_weight = ret[ret['type'] == u'股票'].copy()
        mkt_sum = equity_weight['mkt_value'].sum()
        equity_weight['weight'] = equity_weight['mkt_value'] / mkt_sum * 100
        return equity_weight.sort_values('mkt_value', ascending=False)
    elif return_info == 'total_exposure':
        ret = ret[['trade_date', 'direction', 'mkt_value']]
        ret = ret.groupby(['trade_date', 'direction']).sum().reset_index()
        ret_long = ret[ret['direction'] == u'多仓'][['trade_date', 'mkt_value']]
        ret_short = ret[ret['direction'] == u'空仓'][['trade_date', 'mkt_value']]
        ret = ret_long.merge(ret_short, on='trade_date', how='outer')
        ret.columns = ['trade_date', 'long', 'short']
    pg_handler.close()
    return ret


@preprocess(ticker=ensure_list, fields=ensure_list)
def get_equity_market_cob(ticker, fields, is_index=False, ref_date=None):
    ref_date = default_ref_date(ref_date)
    pg_handler = PGDataHandler()
    market = pg_handler.get_equity_market_cob(ticker, ref_date=ref_date, fields=fields, is_index=is_index)
    pg_handler.close()
    return market


@preprocess(ticker=ensure_list, fields=ensure_list)
def get_equity_market(ticker, start_date, end_date, fields, is_index=False):
    pg_handler = PGDataHandler()
    ret = pg_handler.get_equity_market_range(ticker, start_date, end_date, fields, is_index)
    pg_handler.close()
    return ret


@preprocess(ticker=ensure_list)
def get_equity_return(ticker, start_date, end_date, is_index=False, cumul_return=True):
    pg_handler = PGDataHandler()
    ret = pg_handler.get_equity_market_range(ticker, start_date, end_date, ['pct_change'], is_index)
    if cumul_return:
        ret = pd.DataFrame(ret['pct_change'].apply(lambda x: 1 + x / 100).groupby(ret['ticker']).prod() - 1)
    pg_handler.close()
    return ret


@preprocess(ticker=ensure_list)
def get_equity_price(ticker,
                     start_date,
                     end_date,
                     price_type=PriceType.Close,
                     is_index=False,
                     price_adj=PriceAdjMethod.UnAdjust):
    pg_handler = PGDataHandler()
    fields = [price_type] if price_adj == PriceAdjMethod.UnAdjust or is_index else [price_type, 'adj_factor']
    if start_date == end_date:
        ret = pg_handler.get_equity_market_cob(ticker, start_date, fields, is_index)
    else:
        ret = pg_handler.get_equity_market_range(ticker, start_date, end_date, fields, is_index)
    pg_handler.close()

    if not is_index:
        if price_adj == PriceAdjMethod.PostAdjust:  # T日后复权收盘价 = (T日最新价)×(T日复权因子)
            ret[price_type] = ret[price_type] * ret['adj_factor']
        elif price_adj == PriceAdjMethod.PreAdjust:  # T日前复权收盘价 =(T日复权收盘价) ÷ (最新复权因子)
            adj_price = ret[price_type] * ret['adj_factor']
            adj_factor = ret['adj_factor'].values[-1]
            ret[price_type] = adj_price / adj_factor
    ret = ret[['trade_date', 'ticker', price_type]]
    return ret


@preprocess(ticker=ensure_list)
@expect_types(strategy=TrackingStrategy)
def get_strat_signal(start_date, end_date, ticker, strategy):
    pg_handler = PGDataHandler()
    ret = pg_handler.get_strat_signal(ticker, start_date, end_date, strategy)
    pg_handler.close()
    return ret


def table_fields(table):
    pg_handler = PGDataHandler()
    ret = pg_handler.get_col_names(table)
    pg_handler.close()
    return ret


def check_status(ticker, ref_date, thresh=PCT_THRESH):
    """
    判断给定交易日给定标的是否停牌或者(接近)涨停
    """
    ret = _filter_status(ticker, ref_date, thresh)
    if len(ret) == 0 or ticker not in ret['ticker'].tolist():
        return False
    else:
        return True


def exclude_ticker_by_status(ticker, ref_date):
    """
    去除停牌以及(接近)涨停股票
    """
    market = get_equity_market_cob(ticker=ticker,
                                   ref_date=ref_date,
                                   fields=['pct_change', 'vol', 'trade_status'],
                                   is_index=False)
    ret = market[market['trade_status'] == u'交易']
    if len(ret) > 0:
        ret = ret[ret['vol'] > 0.0]
    if len(ret) > 0:
        ret = ret[ret['pct_change'] <= PCT_THRESH]

    all_ticker = market['ticker'].tolist()
    ret_ticker = ret['ticker'].tolist()
    exclude_ticker = list(set(all_ticker).difference(set(ret_ticker)))

    return ret_ticker, exclude_ticker


def construct_portfolio_by_weight(ticker,
                                  ref_date,
                                  weight=None,
                                  check_ticker_status=True):
    """
    :param ticker: list, 标的列表
    :param ref_date: str, YYYYMMDD， 构建组合的日期
    :param weight: list, optional, 标的的权重向量
    :param check_ticker_status: bool, optional, 是否去除停牌以及涨停股
    :return: pd.DataFrame, col = ['ticker', 'weight']
    """
    portfolio = pd.DataFrame()
    portfolio['ticker'] = ticker
    portfolio['weight'] = [1.0 / len(ticker)] * len(ticker) if weight is None else weight

    ticker_, exclude_ticker_ = exclude_ticker_by_status(ticker, ref_date) if check_ticker_status else ticker
    if len(exclude_ticker_) > 0:
        sum_weight_exclude = portfolio[portfolio['ticker'].isin(exclude_ticker_)]['weight'].sum()
        constant = sum_weight_exclude / len(ticker_)
        # update weight
        portfolio = portfolio[portfolio['ticker'].isin(ticker_)]
        portfolio['weight'] = portfolio['weight'] + constant
    portfolio.reset_index(inplace=True)
    portfolio = portfolio[['ticker', 'weight']]
    return portfolio


def evaluate_portfolio_by_weight(portfolio, start_date, end_date, start_value=1.0):
    """
    :param portfolio: pd.DataFrame, col=['ticker', 'weight']
    两个调仓期之间，计算组合净值的每日净值
    (不包括第一个调仓日，表示已经建仓完毕，故不再考虑去除停牌等股票)
    :param start_date: 开始日期
    :param end_date: 结束日期
    :param start_value: 组合净值的初始值
    :return: pd.DataFrame, col=['trade_date', 'value']
    """
    tickers = portfolio['ticker'].tolist()
    portfolio_return = get_equity_return(tickers,
                                         start_date=start_date,
                                         end_date=end_date,
                                         is_index=False,
                                         cumul_return=False)
    portfolio_return = portfolio_return.set_index(['ticker', 'trade_date'])
    portfolio_curve = pd.DataFrame()
    for ticker in tickers:
        temp = portfolio_return.loc[ticker]['pct_change'].apply(
            lambda x: 1 + x / 100.0).cumprod()
        temp /= temp.iloc[0]
        temp *= portfolio[portfolio.ticker == ticker].weight.iloc[0]
        portfolio_curve = pd.concat([portfolio_curve, temp.reset_index()], axis=0)

    portfolio_curve = portfolio_curve.groupby('trade_date').sum()

    portfolio_curve.columns = ['value']
    portfolio_curve = portfolio_curve.reset_index()
    portfolio_curve['value'] *= start_value
    return portfolio_curve


def default_ref_date(ref_date=None, back_unit='-1M', in_format='%Y%m%d',out_format='%Y%m%d'):
    Cal = Calendar('China.SSE')
    if ref_date is None:
        today = dt.date.today()
        today = Date(today.year, today.month, today.day)
        ref_date = Cal.advanceDate(today, Period(back_unit), BizDayConventions.Unadjusted)
    else:
        ref_date = Date.strptime(ref_date, in_format)
    if back_unit[-1] == 'M':
        ref_date = Cal.endOfMonth(ref_date)
    ref_date = str(ref_date)
    if out_format == '%Y-%m-%d':
        return ref_date
    ref_date, _ = process_date(ref_date)

    return ref_date


def _lookup_industry(ptf, industry_map):
    ret = pd.merge(ptf, industry_map, on='ticker')
    ret = ret.groupby(ret['industry_name']).sum().reset_index()
    return ret


def _filter_status(ticker, ref_date, thresh):
    market = get_equity_market_cob(ticker=ticker,
                                   ref_date=ref_date,
                                   fields=['pct_change', 'vol', 'trade_status'],
                                   is_index=False)
    ret = market[market['trade_status'] == u'交易']
    if len(ret) > 0:
        ret = ret[ret['vol'] > 0.0]
    if len(ret) > 0:
        ret = ret[ret['pct_change'] <= thresh]

    return ret
