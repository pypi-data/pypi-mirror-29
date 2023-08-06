# -*- coding: utf-8 -*-

from xutils import (LiveFeed,
                    BarFrequency)
from ct_manager.base_handler import DataHandler
import tushare as ts


class TushareDataHandler(DataHandler):
    def __init__(self, **kwargs):
        super(TushareDataHandler, self).__init__(**kwargs)
        self.frequency = kwargs.get('frequency', BarFrequency.MINUTE)
        self.live_quote_func = kwargs.get('live_quote_func', ts.get_realtime_quotes)

    def init_db_url(self):
        pass

    def execute(self, script):
        pass

    def live_feed(self, ticker):
        return LiveFeed(tickers=ticker,
                        frequency=self.frequency,
                        live_quote_arg_func=self.live_quote_func)
