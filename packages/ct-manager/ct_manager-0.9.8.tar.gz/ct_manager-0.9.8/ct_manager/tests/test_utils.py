# -*- coding: utf-8 -*-


from argcheck import preprocess
from unittest import TestCase
import pandas as pd
from pandas.testing import assert_frame_equal
from ct_manager.utils import (ensure_date_format,
                              ensure_list,
                              calc_return_on_signal)
from parameterized import parameterized


class TestUtils(TestCase):
    @parameterized.expand(['20170926', '2017/09/26', '2017-09-26', '2017.09.26'])
    def test_ensure_date_format(self, ref_date):
        @preprocess(x=ensure_date_format)
        def check_date(x):
            return x

        self.assertEqual(check_date(ref_date), '2017-09-26')

    def test_ensure_list(self):
        @preprocess(x=ensure_list)
        def check_list(x):
            return x

        self.assertEqual(check_list(['high', 'vol']), ['high', 'vol'])
        self.assertEqual(check_list('high,vol'), ['high', 'vol'])
        self.assertEqual(check_list('high, vol'), ['high', 'vol'])
        self.assertEqual(check_list(['high,vol']), ['high', 'vol'])
        self.assertEqual(check_list(['high, vol']), ['high', 'vol'])

    def test_calc_return_on_signal(self):
        df = pd.DataFrame({'trade_date': ['20100101', '20100102', '20100103'],
                           'pct_change': [10, 20, 30],
                           'signal': [1, -1, 1]})
        calculated = calc_return_on_signal(df)
        expected = pd.DataFrame({'trade_date': ['20100101', '20100102', '20100103'],
                                 'cumul_return': [1.0, 1.2, 0.84]})
        expected = expected[['trade_date', 'cumul_return']]
        assert_frame_equal(calculated, expected)


