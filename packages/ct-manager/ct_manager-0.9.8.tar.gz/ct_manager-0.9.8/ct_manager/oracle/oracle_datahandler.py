# -*- coding: utf-8 -*-

import os
import pandas as pd
import cx_Oracle
from ct_manager.settings import Settings
from ct_manager.enums import (DataSource,
                              ReportType)
from ct_manager.base_handler import DataHandler
from argcheck import *
from ct_manager.utils import ensure_date_format
from xutils import (Period,
                    Date)

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


class GogoalDataHandler(DataHandler):
    def __init__(self, **kwargs):
        super(GogoalDataHandler, self).__init__(data_source=DataSource.GOGOAL_ORACLE_LOCAL, **kwargs)
        self.user = self.connector_params['user']
        self.password = self.connector_params['password']
        self.host = self.connector_params['host']
        self.port = self.connector_params['port']
        self.database = self.connector_params['database']
        self.db_url = self.init_db_url()
        self.engine = cx_Oracle.connect(self.db_url)
        self.session = None

    def init_db_url(self):
        db_url = '{user}/{password}@{host}:{port}/{database}'.format(user=self.user,
                                                                     password=self.password,
                                                                     host=self.host,
                                                                     port=self.port,
                                                                     database=self.database)
        return db_url

    def close(self):
        if not self.engine:
            self.engine.close()

    def execute(self, script):
        cursor = self.engine.cursor()
        cursor.execute(script)
        ret = cursor.fetchall()
        cursor.close()
        return ret

    @preprocess(ref_date=ensure_date_format)
    def get_consensus_expectation_score(self, ref_date):
        """
        分析师一致预期得分
        :param ref_date: str, YYYY-MM-DD, 当前日期
        :return: pd.DataFrame, columns=['ticker', 'score']
        """
        query_script \
            = ''' select * from CON_FORECAST_SCHEDULE where CON_DATE = TO_DATE(\'{ref_date}\', 'yyyy-mm-dd') ''' \
            .format(ref_date=ref_date)
        ret = self.df_read_sql(query_script)
        ret = ret[['STOCK_CODE', 'SCORE']]
        ret.rename(columns={'STOCK_CODE': 'ticker', 'SCORE': 'score'}, inplace=True)
        return ret

    @preprocess(ref_date=ensure_date_format, prev_date=ensure_date_format)
    def get_consensus_expectation_upgrade(self, ref_date, prev_date, thresh=None, tickers=None):
        """
        :param ref_date: str, YYYY-MM-DD, 当前日期
        :param prev_date: ref_date: str, YYYY-MM-DD, 前一期日期
        :param thresh: optional, float, 当前得分超过某一阈值才被包括在返回值中
        :param tickers: optional, list, 标的列表
        :return: pd.DataFrame, columns=['ticker', current_score', 'prev_score']
        分析师一致预期得分在两个日期间提高的股票列表，如果thresh不为None，则在该列表中还要筛选出当前得分高于thresh的股票列表
        """
        current_score = self.get_consensus_expectation_score(ref_date)
        current_score.rename(columns={'score': 'current_score'}, inplace=True)
        prev_score = self.get_consensus_expectation_score(prev_date)
        prev_score.rename(columns={'score': 'prev_score'}, inplace=True)
        grade = pd.merge(prev_score, current_score, on='ticker')
        ret = grade[grade['current_score'] > grade['prev_score']]
        if thresh:
            ret = ret[ret['current_score'] > thresh]
        if tickers:
            ret = ret[ret['ticker'].isin(tickers)]
        return ret


class WindDataHandler(DataHandler):
    def __init__(self, **kwargs):
        super(WindDataHandler, self).__init__(data_source=DataSource.WIND_ORACLE_LOCAL, **kwargs)
        self.user = self.connector_params['user']
        self.password = self.connector_params['password']
        self.host = self.connector_params['host']
        self.port = self.connector_params['port']
        self.database = self.connector_params['database']
        self.db_url = self.init_db_url()
        self.engine = cx_Oracle.connect(self.db_url)
        self.session = None

    def init_db_url(self):
        db_url = '{user}/{password}@{host}:{port}/{database}'.format(user=self.user,
                                                                     password=self.password,
                                                                     host=self.host,
                                                                     port=self.port,
                                                                     database=self.database)
        return db_url

    def close(self):
        if not self.engine:
            self.engine.close()

    def execute(self, script):
        cursor = self.engine.cursor()
        cursor.execute(script)
        ret = cursor.fetchall()
        cursor.close()
        return ret

    @staticmethod
    def _clean_ticker(df, ticker=None):
        df['ticker'] = df['ticker'].apply(lambda x: x.split('.')[0])
        if ticker is not 'ashare':
            df = df[df['ticker'].isin(ticker)]
        return df

    def get_net_profit_express(self,
                               report_date,
                               ref_date=None,
                               ticker='ashare'):
        sql = '''select S_INFO_WINDCODE, REPORT_PERIOD, ANN_DT, NET_PROFIT_EXCL_MIN_INT_INC from AShareProfitExpress where 
                                REPORT_PERIOD = {report_date} '''.format(report_date=report_date)

        if ref_date is not None:
            sql += '''and ANN_DT <= {announce_date} ORDER BY S_INFO_WINDCODE  '''.format(
                announce_date=ref_date)
        sql += '''ORDER BY S_INFO_WINDCODE '''
        ret = self.df_read_sql(sql)
        ret.rename(columns={'S_INFO_WINDCODE': 'ticker',
                            'REPORT_PERIOD': 'report_date',
                            'ANN_DT': 'announce_date',
                            'NET_PROFIT_EXCL_MIN_INT_INC': 'net_profit'},
                   inplace=True)
        ret = self._clean_ticker(ret, ticker)
        # 把净利润的单位为元转化为万元
        ret['net_profit'] /= 10000
        ret.sort_values('announce_date', inplace=True)
        return ret

    def get_net_profit(self,
                       report_date,
                       ref_date=None,
                       ticker='ashare',
                       use_simple_algo=False):
        """
        :param ref_date: str, YYYYMMDD, 当前日期
        :param report_date: str, YYYYMMDD, optional, 如果是None, 那么根据ref_date计算出最近的report_date
        :param ticker: str/list, optional, 如果是'ashare'就返回全市场股票
        :param use_simple_algo, bool, optinal, 如果是否则使用较为复杂的判断方法选取最近报告日的报告
        :return: pd.DataFrame, columns=['ticker', report_date', 'announce_date', 'statement_type', 'net_profit']
        给定某个当前日期，返回 财报 最近报告期的净利润数据，或者给定报告期返回该期净利润数据

        """

        sql = '''select S_INFO_WINDCODE, REPORT_PERIOD, ANN_DT, STATEMENT_TYPE, NET_PROFIT_INCL_MIN_INT_INC
                                            from AShareIncome  where 
                                            REPORT_PERIOD = {report_date} and
                                            STATEMENT_TYPE in {report}
                                             '''.format(report_date=report_date,
                                                        report=('408001000') if use_simple_algo
                                                        else ('408001000', '408004000', '408005000'))

        if ref_date is not None:
            sql += '''and ANN_DT <= {announce_date} ORDER BY S_INFO_WINDCODE '''.format(announce_date=ref_date)
        else:
            sql += '''ORDER BY S_INFO_WINDCODE '''

        ret = self.df_read_sql(sql)
        ret.rename(columns={'S_INFO_WINDCODE': 'ticker',
                            'REPORT_PERIOD': 'report_date',
                            'ANN_DT': 'announce_date',
                            'STATEMENT_TYPE': 'statement_type',
                            'NET_PROFIT_INCL_MIN_INT_INC': 'net_profit'},
                   inplace=True)

        ret = self._clean_ticker(ret, ticker)
        # 把净利润的单位为元转化为万元
        ret['net_profit'] /= 10000
        # 为避免使用未来数据，对公告日再对报告类型排序，详见AlphaNote
        ret.sort_values('statement_type', inplace=True)
        ret.sort_values('announce_date', inplace=True)
        group = ret.groupby(['ticker']).last()
        return pd.DataFrame(group).reset_index()

    def get_net_profit_preannounce(self, report_date, ref_date=None, ticker='ashare', groupby_last=True):
        """
        :param ref_date: str, YYYYMMDD, 当前日期
        :param report_date: str, YYYYMMDD, optional, 如果是None, 那么根据ref_date计算出最近的report_date
        :param ticker: str/list, optional, 如果是'ashare'就返回全市场股票
        :param grouby_last: bool, optional, 是否仅采用最新的报告数字
        :return: pd.DataFrame, columns=['ticker', report_date', 'announce_date', 'net_profit_min', 'net_profit_max', 'net_profit_mean']
        给定某个当前日期，返回 业绩预告 最近报告期的净利润数据，或者给定报告期返回该期净利润数据

        """
        sql = '''select S_INFO_WINDCODE, S_PROFITNOTICE_PERIOD, S_PROFITNOTICE_DATE, S_PROFITNOTICE_NUMBER, S_PROFITNOTICE_NETPROFITMIN, S_PROFITNOTICE_NETPROFITMAX 
                        from AShareProfitNotice   where 
                        S_PROFITNOTICE_PERIOD = {report_date} and
                        S_PROFITNOTICE_NETPROFITMIN > -1000000000 and
                         S_PROFITNOTICE_NETPROFITMAX > -1000000000 '''.format(report_date=report_date)

        if ref_date is not None:
            sql += '''and S_PROFITNOTICE_DATE <= {announce_date} ORDER BY S_INFO_WINDCODE,S_PROFITNOTICE_DATE  '''.format(
                announce_date=ref_date)
        else:
            sql += '''ORDER BY S_INFO_WINDCODE,S_PROFITNOTICE_DATE  '''

        ret = self.df_read_sql(sql)
        ret.rename(columns={'S_INFO_WINDCODE': 'ticker',
                            'S_PROFITNOTICE_NUMBER': 'notice_number',
                            'S_PROFITNOTICE_PERIOD': 'report_date',
                            'S_PROFITNOTICE_DATE': 'announce_date',
                            'S_PROFITNOTICE_NETPROFITMIN': 'net_profit_min',
                            'S_PROFITNOTICE_NETPROFITMAX': 'net_profit_max',
                            }, inplace=True)

        ret = self._clean_ticker(ret, ticker)
        ret['net_profit_mean'] = (ret['net_profit_min'] + ret['net_profit_max']) / 2
        if groupby_last:
            group = ret.groupby(['ticker']).last()
            return pd.DataFrame(group).reset_index()
        else:
            return ret

    def get_market_value(self, ref_date, ticker='ashare'):
        sql = '''select S_INFO_WINDCODE, TRADE_DT, S_VAL_MV
                        from AShareEODDerivativeIndicator where 
                        TRADE_DT = {trade_date} 
                        ORDER BY S_INFO_WINDCODE '''.format(trade_date=ref_date)
        ret = self.df_read_sql(sql)
        ret.rename(columns={'S_INFO_WINDCODE': 'ticker',
                            'TRADE_DT': 'trade_date',
                            'S_VAL_MV': 'mv'},
                   inplace=True)
        ret = self._clean_ticker(ret, ticker)
        return ret

    def calc_historical_preannouce_sue(self, report_date, report_date_prev):
        """
        计算 预报日对应的SUE（假设已经全部披露）
        depreciated
        """
        net_profit_prev = self.get_net_profit(report_date=report_date_prev)
        net_profit_current_preannouce = self.get_net_profit_preannounce(report_date=report_date)
        mv = self.get_market_value(ref_date=report_date)

        data_container = pd.merge(net_profit_prev, net_profit_current_preannouce, on='ticker')
        data_container = pd.merge(data_container, mv, on='ticker')

        data_container['sue'] = (data_container['net_profit_mean'] - data_container['net_profit']) \
            .div(data_container['mv'])
        data_container.sort_values('sue', inplace=True, ascending=False)

        return data_container

    def _get_profit(self, report_date, report_type):
        if report_type == ReportType.Report:
            ref_date = Date.strptime(report_date, date_format='%Y%m%d') + Period('4M')
            ref_date = ref_date.strftime('%Y%m%d')
            return self.get_net_profit(report_date, ref_date=ref_date)
        elif report_type == ReportType.Express:
            return self.get_net_profit_express(report_date)
        else:
            return self.get_net_profit_preannounce(report_date)

    def calc_sue(self, report_dict, report_prev_dict, mv_date=None):
        report_date = report_dict['report_date']
        report_type = report_dict['report_type']
        report_date_prev = report_prev_dict['report_date']
        report_prev_type = report_prev_dict['report_type']

        net_profit = self._get_profit(report_date, report_type)
        if report_type == ReportType.Report:
            net_profit.rename(columns={'net_profit': 'net_profit_mean'}, inplace=True)
        net_profit_prev = self._get_profit(report_date_prev, report_prev_type)
        mv = self.get_market_value(mv_date) if mv_date is not None else self.get_market_value(report_date)

        data_container = pd.merge(net_profit_prev[['ticker', 'net_profit']], net_profit, on='ticker')
        data_container = pd.merge(data_container, mv, on='ticker')

        data_container['sue'] = (data_container['net_profit_mean'] - data_container['net_profit']) \
            .div(data_container['mv'])
        data_container.sort_values('sue', inplace=True, ascending=False)

        return data_container


class XRiskDataHandler(DataHandler):
    def __init__(self, **kwargs):
        super(XRiskDataHandler, self).__init__(data_source=DataSource.XRisk_ORACLE_LOCAL, **kwargs)
        self.user = Settings.xrisk_user
        self.password = Settings.xrisk_password
        self.host = self.connector_params['host']
        self.port = self.connector_params['port']
        self.database = self.connector_params['database']
        self.db_url = self.init_db_url()
        self.engine = cx_Oracle.connect(self.db_url)
        self.session = None

    def init_db_url(self):
        db_url = '{user}/{password}@{host}:{port}/{database}'.format(user=self.user,
                                                                     password=self.password,
                                                                     host=self.host,
                                                                     port=self.port,
                                                                     database=self.database)
        return db_url

    def close(self):
        if not self.engine:
            self.engine.close()

    def execute(self, script):
        cursor = self.engine.cursor()
        cursor.execute(script)
        ret = cursor.fetchall()
        cursor.close()
        return ret

    def get_portfolio(self, product_code, ref_date):
        sql = '''select * from ttmp_h_gzb where l_ztbh={product_code} and
        d_ywrq=TO_DATE(\'{ref_date}\', 'yyyymmdd') order by l_bh''' \
            .format(product_code=product_code,
                    ref_date=ref_date)
        ret = self.df_read_sql(sql)
        return ret


