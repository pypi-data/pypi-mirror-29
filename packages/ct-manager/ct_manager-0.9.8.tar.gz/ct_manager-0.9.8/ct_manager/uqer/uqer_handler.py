# -*- coding: utf-8 -*-

import uqer
from uqer import DataAPI
from ct_manager.base_handler import DataHandler
from ct_manager.utils import (process_date,
                              check_holiday)
from ct_manager.settings import Settings
from ct_manager.enums import DataSource


uqer.DataAPI.api_base.timeout = 300


class UqerDataHandler(DataHandler):
    def __init__(self, **kwargs):
        Settings.data_source = DataSource.UQER
        super(UqerDataHandler, self).__init__(**kwargs)
        self.token = self.connector_params['token']
        self.create_session()

    def init_db_url(self):
        pass

    def create_session(self):
        _ = uqer.Client(token=self.token)
        return

    def execute(self, script):
        self.engine.execute(script)
        return

    @staticmethod
    def get_halt_list(query_date):
        ref_date, this_date = process_date(query_date)
        flag = check_holiday(this_date)

        if not flag:
            return

        df = DataAPI.SecHaltGet(beginDate=ref_date, endDate=ref_date)
        df = df[df.assetClass == 'E']
        df['trade_date'] = ref_date
        df.rename(columns={'ticker': 'code'}, inplace=True)
        df.code = df.code.astype(int)
        del df['secID']

        return df

    @staticmethod
    def calc_index_return(begin_date, end_date, ticker, fields='tradeDate, closeIndex', **kwargs):
        close = DataAPI.MktIdxdGet(ticker=ticker,
                                   beginDate=begin_date,
                                   endDate=end_date,
                                   field=fields,
                                   **kwargs)
        begin_price = close.head(n=1).iloc[0, 1]
        end_price = close.tail(n=1).iloc[0, 1]
        ret = end_price / begin_price - 1
        return ret

    @staticmethod
    def calc_sec_return(begin_date, end_date, ticker, fields='tradeDate, closePrice', **kwargs):
        close = DataAPI.MktEqudAdjGet(ticker=ticker,
                                      beginDate=begin_date,
                                      endDate=end_date,
                                      fields=fields,
                                      **kwargs)
        if len(close) > 0:
            begin_price = close.head(n=1).iloc[0, 1]
            end_price = close.tail(n=1).iloc[0, 1]
            ret = end_price / begin_price - 1
            status = 1
        else:
            ret = 0
            status = 0
        return ret, status

    @staticmethod
    def get_industry(industry='010303', **kwargs):
        ret = DataAPI.EquIndustryGet(industryVersionCD=industry, **kwargs)
        return ret

    @staticmethod
    def get_ashare_universe(ref_date):
        """
        https://uqer.datayes.com/community/share/5964c03a4030e00058381b43
        """
        universe = DataAPI.EquGet(equTypeCD='A', listStatusCD='L,S,DE', field='ticker,listDate,delistDate')
        universe['listdate'] = universe['listDate'].apply(lambda x: x.replace('-', ''))
        universe['delistdate'] = universe['delistDate'].apply(
            lambda x: x.replace('-', '') if isinstance(x, unicode) else '99999999')
        universe = universe[(universe['listdate'] <= ref_date) & (universe['delistdate'] > ref_date)]
        tickers = universe['ticker'].tolist()
        return tickers

    @staticmethod
    def get_net_profit_preannouce(ticker,
                                  report_type='',
                                  report_begin_date='',
                                  report_end_date='',
                                  publish_begin_date='',
                                  publish_end_date='',
                                  fields=None):
        fields = ['ticker', 'secShortName', 'actPubtime', 'NIncAPChgrLL', 'NIncAPChgrUPL', 'expnIncAPLL',
                  'expnIncAPUPL'] if fields is None else fields
        yugao = DataAPI.FdmtEfGet(ticker=ticker,
                                  reportType=report_type,
                                  beginDate=report_begin_date,
                                  endDate=report_end_date,
                                  publishDateBegin=publish_begin_date,
                                  publishDateEnd=publish_end_date,
                                  field=fields)
        yugao = yugao.sort_values('actPubtime', ascending=False).set_index('ticker').drop_duplicates('secShortName')

        return yugao

    @staticmethod
    def get_net_profit(ticker,
                       report_type='',
                       report_begin_date='',
                       report_end_date='',
                       publish_begin_date='',
                       publish_end_date='',
                       fields=None):
        fields = ['ticker', 'secShortName', 'actPubtime', 'fiscalPeriod', 'reportType', 'endDate', 'endDateRep',
                  'NIncome', 'NIncomeAttrP', 'minoritiyGain', 'basicEPS', 'dilutedEPS'] if fields is None else fields
        NI = DataAPI.FdmtISGet(ticker=ticker,
                               reportType=report_type,
                               beginDate=report_begin_date,
                               endDate=report_end_date,
                               publishDateBegin=publish_begin_date,
                               publishDateEnd=publish_end_date,
                               field=fields)
        NI = NI.sort_values('actPubtime', ascending=False).set_index('ticker')

        return NI

