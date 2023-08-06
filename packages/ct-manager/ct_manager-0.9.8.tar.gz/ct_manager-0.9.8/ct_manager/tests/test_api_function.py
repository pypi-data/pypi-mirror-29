# -*- coding:utf-8 -*-

from ct_manager.api import (get_equity_price,
                            get_equity_return,
                            get_equity_market,
                            get_index_industry_weight,
                            get_ptf_industry_weight,
                            get_equity_market_cob,
                            get_industry,
                            universe,
                            check_status,
                            exclude_ticker_by_status,
                            construct_portfolio_by_weight,
                            evaluate_portfolio_by_weight)
import pandas as pd
from unittest import TestCase
from pandas.util.testing import assert_frame_equal
from ct_manager.enums import (SWIndustryLevel,
                              PriceAdjMethod,
                              PriceType)

try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch


class TestAPI(TestCase):
    @patch('ct_manager.pg.pg_handler.PGDataHandler.get_equity_market_cob')
    def test_get_equity_price_1(self, mock_market_cob):
        # 读取指定区间股票价格序列（默认不复权收盘价）
        df = pd.DataFrame(data={'trade_date': ['20160204', '20160204'],
                                'ticker': ['002594', '600115'],
                                'close': [51.21, 6.21]})
        df = df[['close', 'ticker', 'trade_date']]
        mock_market_cob.return_value = df
        calculated = get_equity_price(['600115', '002594'],
                                      start_date='20160204',
                                      end_date='20160204')

        expected = pd.DataFrame(data={'trade_date': ['20160204', '20160204'],
                                      'ticker': ['002594', '600115'],
                                      'close': [51.21, 6.21]})
        expected = expected[['trade_date', 'ticker', 'close']]
        assert_frame_equal(expected, calculated)

    @patch('ct_manager.pg.pg_handler.PGDataHandler.get_equity_market_range')
    def test_get_equity_price_2(self, mock_market_range):
        # 读取指定区间股票价格序列（后复权开盘价）
        df = pd.DataFrame(data={'trade_date': ['20160204', '20160205', '20160204', '20160205'],
                                'adj_factor': [1.00097, 1.00097, 1.33991, 1.33991],
                                'ticker': ['002594', '002594', '600115', '600115'],
                                'open': [51.00, 51.50, 6.06, 6.25]})
        df = df[['open', 'adj_factor', 'ticker', 'trade_date']]
        mock_market_range.return_value = df
        calculated = get_equity_price(['600115', '002594'],
                                      start_date='20160204',
                                      end_date='20160205',
                                      price_type=PriceType.Open,
                                      price_adj=PriceAdjMethod.PostAdjust)

        expected = pd.DataFrame(data={'trade_date': ['20160204', '20160205', '20160204', '20160205'],
                                      'ticker': ['002594', '002594', '600115', '600115'],
                                      'open': [51.04947, 51.549955, 8.119867, 8.374450]})
        expected = expected[['trade_date', 'ticker', 'open']]
        assert_frame_equal(expected, calculated)

    @patch('ct_manager.pg.pg_handler.PGDataHandler.get_equity_market_range')
    def test_get_equity_price_3(self, mock_market_range):
        # 读取指定区间股票价格序列（前复权收盘价）
        df = pd.DataFrame(data={'trade_date': ['20160204', '20160205', '20160204', '20160205'],
                                'adj_factor': [1.00097, 1.00097, 1.33991, 1.33991],
                                'ticker': ['002594', '002594', '600115', '600115'],
                                'close': [51.21, 50.07, 6.21, 6.31]})
        df = df[['close', 'adj_factor', 'ticker', 'trade_date']]
        mock_market_range.return_value = df
        calculated = get_equity_price(['600115', '002594'],
                                      start_date='20160204',
                                      end_date='20160205',
                                      price_type=PriceType.Close,
                                      price_adj=PriceAdjMethod.PreAdjust)

        expected = pd.DataFrame(data={'trade_date': ['20160204', '20160205', '20160204', '20160205'],
                                      'ticker': ['002594', '002594', '600115', '600115'],
                                      'close': [38.25600, 37.40437, 6.21, 6.31]})
        expected = expected[['trade_date', 'ticker', 'close']]
        assert_frame_equal(expected, calculated)

    # 股票、不累计
    @patch('ct_manager.pg.pg_handler.PGDataHandler.get_equity_market_range')
    def test_get_equity_return(self, mock_get_equity_market_range):
        df = pd.DataFrame(data={'pct_change': [-0.0841, 0, 0.2244, 0.2257],
                                'ticker': ['601318', '601398', '601318', '601398'],
                                'trade_date': ['20170104', '20170104', '20170105', '20170105']
                                })
        mock_get_equity_market_range.return_value = df

        # 替换 get_equity_market_range 中的查数据库的函数
        calculated = get_equity_return(['601318', '601398'], '20170104', '20170105', is_index=False, cumul_return=False)
        expected = df
        assert_frame_equal(calculated, expected)

    # 股票、累计
    @patch('ct_manager.pg.pg_handler.PGDataHandler.get_equity_market_range')
    def test_get_equity_return_2(self, mock_get_equity_market_range):
        df = pd.DataFrame(data={'pct_change': [-0.0841, 0, 0.2244, 0.2257],
                                'ticker': ['601318', '601398', '601318', '601398'],
                                'trade_date': ['20170104', '20170104', '20170105', '20170105']
                                })
        mock_get_equity_market_range.return_value = df
        calculated = get_equity_return(['601318'], '20170104', '20170106', is_index=False, cumul_return=True)
        expected = pd.DataFrame(data={'pct_change': [0.001401112796, 0.002257]}, index=['601318', '601398'])
        expected.index.name = 'ticker'
        assert_frame_equal(calculated, expected)

    # 指数、不累计
    @patch('ct_manager.pg.pg_handler.PGDataHandler.get_equity_market_range')
    def test_get_equity_return_3(self, mock_get_equity_market_range):
        df = pd.DataFrame(data={'pct_change': [0.7805, -0.0155],
                                'ticker': ['000300', '000300'],
                                'trade_date': ['20170104', '20170105']})
        mock_get_equity_market_range.return_value = df

        # 替换 get_equity_market_range 中的查数据库的函数
        calculated = get_equity_return(['000300'], '20170104', '20170105', is_index=True, cumul_return=False)

        expected = pd.DataFrame(data={'pct_change': [0.7805, -0.0155],
                                      'ticker': ['000300', '000300'],
                                      'trade_date': ['20170104', '20170105']})
        assert_frame_equal(calculated, expected)

    # 指数、累计
    @patch('ct_manager.pg.pg_handler.PGDataHandler.get_equity_market_range')
    def test_get_equity_return_4(self, mock_get_equity_market_range):
        df = pd.DataFrame(data={'pct_change': [0.7805, -0.0155],
                                'ticker': ['000300', '000300'],
                                'trade_date': ['20170104', '20170105']})
        mock_get_equity_market_range.return_value = df
        calculated = get_equity_return(['000300'], '20170104', '20170105', is_index=True, cumul_return=True)
        calculated['pct_change'] = calculated['pct_change'].apply(lambda x: round(x, 6))  # 精度 ?
        expected = pd.DataFrame(data={'pct_change': [0.007649]}, index=['000300'])
        expected.index.name = 'ticker'
        assert_frame_equal(calculated, expected)

    # 测试获取所属行业 替换 pg_handler中的get_industry_map函数 SW 一级行业
    @patch('ct_manager.pg.pg_handler.PGDataHandler.get_industry_map')
    def test_get_industry(self, mock_get_industry_map):
        mock_df = pd.DataFrame(data={
            'ticker': ['601318', '600050', '601398'],
            'name': [u'中国平安', u'中国联通', u'工商银行'],
            'industry_ticker': ['1030322', '1030327', '1030321'],
            'industry_name': [u'非银金融', u'通信', u'银行']
        })
        mock_df = mock_df[['ticker', 'name', 'industry_ticker', 'industry_name']]
        mock_get_industry_map.return_value = mock_df

        calculated = get_industry(['601318', '600050'], sw_level=SWIndustryLevel.L1)
        expected = mock_df.copy()
        expected = expected.iloc[:2, :]

        assert_frame_equal(calculated, expected)

    # 测试获取所属行业 SW_level2
    @patch('ct_manager.pg.pg_handler.PGDataHandler.get_industry_map')
    def test_get_industry_2(self, mock_get_industry_map):
        # SW 二级行业
        mock_df = pd.DataFrame(data={
            'ticker': ['600050', '601318'],
            'name': [u'中国联通', u'中国平安'],
            'industry_ticker': ['0103032701', '0103032202'],
            'industry_name': [u'通信运营', u'保险']
        })
        mock_df = mock_df[['ticker', 'name', 'industry_ticker', 'industry_name']]
        mock_get_industry_map.return_value = mock_df

        calculated = get_industry(['601318', '600050'], sw_level=SWIndustryLevel.L2)
        expected = mock_df.copy()
        expected = expected.iloc[:2, :]

        assert_frame_equal(calculated, expected)

    # 测试股票是否为正常交易状态
    @patch('ct_manager.pg.pg_handler.PGDataHandler.get_equity_market_cob')
    def test_check_status_1(self, mock_get_equity_market_cob):
        expected = True  # 正常交易（没有涨跌停）
        # 涨跌停
        db_df = pd.DataFrame(data={'pct_change': 1.1905, 'vol': 2001432.36, 'trade_status': u'交易',
                                   'ticker': '600050', 'trade_date': '20171201'}, index=[0])
        mock_get_equity_market_cob.return_value = db_df[['pct_change', 'vol', 'trade_status', 'ticker', 'trade_date']]
        calculated = check_status('600050', '20171218')
        self.assertEqual(calculated, expected)

    # 测试股票停牌状态
    @patch('ct_manager.pg.pg_handler.PGDataHandler.get_equity_market_cob')
    def test_check_status_2(self, mock_get_equity_market_cob):
        db_df = pd.DataFrame(data={'pct_change': 1.1905, 'vol': 2001432.36, 'trade_status': u'交易',
                                   'ticker': '600050', 'trade_date': '20171201'}, index=[0])
        mock_get_equity_market_cob.return_value = db_df[
            ['pct_change', 'vol', 'trade_status', 'ticker', 'trade_date']]
        # 正常交易（并不是停牌）
        expected = True
        calculated = check_status('600050', ref_date='20171218', thresh=12)  # 返回True，即处于正常状态
        self.assertEqual(calculated, expected)

    # 根据交易状态把股票代码分为 ([正常交易], [涨跌停 或 停牌])
    @patch('ct_manager.pg.pg_handler.PGDataHandler.get_equity_market_cob')
    def test_exclude_ticker_by_status(self, mock_get_equity_market_cob):
        db_df = pd.DataFrame(data={'pct_change': 1.1905, 'vol': 2001432.36, 'trade_status': u'交易',
                                   'ticker': '600050', 'trade_date': '20171201'}, index=[0])
        mock_get_equity_market_cob.return_value = db_df[['pct_change', 'vol', 'trade_status', 'ticker', 'trade_date']]

        calculated = exclude_ticker_by_status('600050', '20171220')
        expected = (['600050'], [])  # e.g. 交易、涨跌停
        self.assertEqual(calculated, expected)

        db_df = pd.DataFrame(data={'pct_change': [1, 10], 'vol': [2, 1],
                                   'trade_status': [u'交易', u'交易'], 'ticker': ['600000', '603477'],
                                   'trade_date': ['20171220', '20171220']}, index=[0, 1])
        mock_get_equity_market_cob.return_value = db_df[['pct_change', 'vol', 'trade_status', 'ticker', 'trade_date']]
        calculated = exclude_ticker_by_status(['603477', '600000'], '20171220')
        expected = (['600000'], ['603477'])

        self.assertEqual(calculated, expected)

    # 测试构造一个组合
    @patch('ct_manager.api.exclude_ticker_by_status')
    def test_construct_portfolio_1(self, mock_exclude_ticker_by_status):
        mock_exclude_ticker_by_status.return_value = (['600002', '600003'], ['600000'])
        calculated = construct_portfolio_by_weight(ticker=['600000', '600002', '600003'],
                                                   ref_date='20171220')
        expected = pd.DataFrame(data={'ticker': ['600002', '600003'], 'weight': [0.5, 0.5]})
        assert_frame_equal(calculated, expected)

    # 测试构造一个组合
    @patch('ct_manager.api.exclude_ticker_by_status')
    def test_construct_portfolio_2(self, mock_exclude_ticker_by_status):
        mock_exclude_ticker_by_status.return_value = (['600002', '600003'], ['600000'])
        calculated = construct_portfolio_by_weight(ticker=['600000', '600002', '600003'],
                                                   ref_date='20171220',
                                                   weight=[0.5, 0.1, 0.4])
        expected = pd.DataFrame(data={'ticker': ['600002', '600003'], 'weight': [0.35, 0.65]})
        assert_frame_equal(calculated, expected)

    # 读取指定日期上证50的成分股列表
    @patch('ct_manager.pg.pg_handler.PGDataHandler.get_index_component')
    def test_universe(self, mock_get_index_component):
        mock_data = pd.DataFrame(data={
            'cons_ticker': ['600000', '600016', '600028', '600029', '600030']})
        mock_get_index_component.return_value = mock_data
        calculated = universe('000016', ref_date='20170929', pandas_format=1)  # df形式
        expected = mock_data
        assert_frame_equal(calculated, expected)

        calculated = universe('000016', ref_date='20170929', pandas_format=0)  # list形式
        expected = mock_data['cons_ticker'].tolist()
        self.assertEqual(calculated, expected)

    # 读取全市场标的列表
    @patch('ct_manager.pg.pg_handler.PGDataHandler.get_index_component')
    def test_universe(self, mock_get_index_component):
        mock_data = pd.DataFrame(data={
            'cons_ticker': ['600000', '600016', '600028', '600029', '600030']})
        mock_get_index_component.return_value = mock_data
        calculated = universe('000016', ref_date='20170929', pandas_format=1)  # df形式
        expected = mock_data
        assert_frame_equal(calculated, expected)

        calculated = universe('000016', ref_date='20170929', pandas_format=0)  # list形式
        expected = mock_data['cons_ticker'].tolist()
        self.assertEqual(calculated, expected)

    # 测试行业权重 SW一级行业
    @patch('ct_manager.pg.pg_handler.PGDataHandler.get_index_component')
    @patch('ct_manager.pg.pg_handler.PGDataHandler.get_industry_map')
    def test_get_index_industry_weight_1(self, mock_get_industry_map, mock_get_index_component):
        mock_data = pd.DataFrame(data={'cons_ticker': ['600000', '600016', '600028'],
                                       'weight': [3.168, 4.151, 1.358]})

        mock_get_index_component.return_value = mock_data

        mock_data2 = pd.DataFrame(data={'ticker': ['600000', '600016', '600028'],
                                        'name': ['浦发银行', '民生银行', '中国石化'],
                                        'industry_ticker': ['1030321', '1030321', '1030303'],
                                        'industry_name': ['银行', '银行', '化工']})
        mock_data2 = mock_data2[['ticker', 'name', 'industry_ticker', 'industry_name']]

        mock_get_industry_map.return_value = mock_data2

        calculated = get_index_industry_weight('000016', ref_date='20170929', sw_level=SWIndustryLevel.L1)
        expected = pd.DataFrame(data={'industry_name': ['化工', '银行'],
                                      'weight': [1.358, 3.168 + 4.151]})
        assert_frame_equal(calculated, expected)

    # 测试行业权重 SW二级行业
    @patch('ct_manager.pg.pg_handler.PGDataHandler.get_index_component')
    @patch('ct_manager.pg.pg_handler.PGDataHandler.get_industry_map')
    def test_get_index_industry_weight_2(self, mock_get_industry_map, mock_get_index_component):
        # SW二级行业
        mock_data = pd.DataFrame(data={'cons_ticker': ['600000', '600016', '600028'],
                                       'weight': [2.963, 4.271, 1.294]})

        mock_get_index_component.return_value = mock_data

        mock_data2 = pd.DataFrame(data={'ticker': ['600000', '600016', '600028'],
                                        'name': ['浦发银行', '民生银行', '中国石化'],
                                        'industry_ticker': ['103032101', '103032101', '103030301'],
                                        'industry_name': ['银行', '银行', '石油化工']})
        mock_data2 = mock_data2[['ticker', 'name', 'industry_ticker', 'industry_name']]

        mock_get_industry_map.return_value = mock_data2

        calculated = get_index_industry_weight('000016', ref_date='20170929', sw_level=SWIndustryLevel.L2)
        data = pd.DataFrame(data={'industry_name': ['石油化工', '银行'],
                                  'weight': [1.294, 2.963 + 4.271]})
        expected = data
        assert_frame_equal(calculated, expected)

    # 指定日的A股行情数据
    @patch('ct_manager.pg.pg_handler.PGDataHandler.get_equity_market_cob')
    def test_get_equity_market_cob(self, mock_get_equity_market_cob):
        # 读取指定日期股票开高低收价格信息
        data = pd.DataFrame(
            data={'open': [11.55, 17.4, 16.06, 63.5], 'high': [11.58, 17.48, 16.06, 64.5],
                  'low': [11.39, 17.25, 15.81, 63.31], 'close': [11.54, 17.32, 15.91, 64.36],
                  'ticker': ['000001', '600030', '600900', '601318'],
                  'trade_date': ['20171031', '20171031', '20171031', '20171031']})

        mock_get_equity_market_cob.return_value = data[['open', 'high', 'low', 'close', 'ticker', 'trade_date']]

        calculated = mock_get_equity_market_cob(['000001', '600030', '600900', '601318'],
                                                fields=['open', 'high', 'low', 'close'],
                                                ref_date='20171031')

        expected = data[['open', 'high', 'low', 'close', 'ticker', 'trade_date']]
        assert_frame_equal(calculated, expected)

        # 读取上个月末交易日中证500及沪深300指数涨跌幅数据
        data = pd.DataFrame(
            data={'pct_change': [-1.1755, -0.8696],
                  'ticker': ['000300', '000905'],
                  'trade_date': ['20171130', '20171130']})
        mock_get_equity_market_cob.return_value = data[['pct_change', 'ticker', 'trade_date']]
        calculated = mock_get_equity_market_cob(['000905', '000300'], fields='pct_change', is_index=True)
        expected = data[['pct_change', 'ticker', 'trade_date']]
        assert_frame_equal(calculated, expected)

    # 指定区间的A股行情数据
    @patch('ct_manager.pg.pg_handler.PGDataHandler.get_equity_market_range')
    def test_get_equity_market(self, mock_get_equity_market_range):
        # 读取指定区间股票涨跌幅及成交额信息
        data = pd.DataFrame(
            data={'pct_change': [-5.5046, -5.4167, 0.6178, 1.3216],
                  'amt': [660376.1531, 2468127.284, 755531.3537, 3002728.33],
                  'ticker': ['000001', '601318', '000001', '601318'],
                  'trade_date': ['20160104', '20160104', '20160105', '20160105']}
        )
        mock_get_equity_market_range.return_value = data[['pct_change', 'amt', 'ticker', 'trade_date']]
        calculated = get_equity_market(['000001', '601318'], start_date='20160104', end_date='20160105',
                                       fields=['pct_change', 'amt'])

        expected = data[['pct_change', 'amt', 'ticker', 'trade_date']]
        assert_frame_equal(calculated, expected)

        # 读取指定区间指数开高低收价格信息
        data = pd.DataFrame(data={'open': [2417.0246, 2230.08, 3725.8561, 3382.1769],
                                  'high': [2417.0246, 2309.5937, 3726.2446, 3518.217],
                                  'low': [2269.9671, 2223.0521, 3468.9485, 3377.2799],
                                  'close': [2270.4609, 2288.1127, 3469.0662, 3478.7797],
                                  'ticker': ['000016', '000016', '000300', '000300'],
                                  'trade_date': ['20160104', '20160105', '20160104', '20160105']})

        mock_get_equity_market_range.return_value = data[['open', 'high', 'low', 'close', 'ticker', 'trade_date']]
        calculated = get_equity_market(['000016', '000300'], start_date='20160104', end_date='20160105',
                                       fields=['open', 'high', 'low', 'close'], is_index=True)

        expected = data[['open', 'high', 'low', 'close', 'ticker', 'trade_date']]
        assert_frame_equal(calculated, expected)

    @patch('ct_manager.api.get_equity_return')
    def test_evaluate_portfolio_by_weight(self, mock_get_equity_return):
        portfolio = pd.DataFrame({'ticker': ['000001', '000002'], 'weight': [0.5, 0.5]})
        mock_get_equity_return.return_value = pd.DataFrame(
            {'trade_date': ['20170103', '20170103', '20170104', '20170104'],
             'ticker': ['000001', '000002', '000001', '000002'],
             'pct_change': [10, 10, -10, 5]})
        calculated = evaluate_portfolio_by_weight(portfolio, '20170101', '20170104')
        expected = pd.DataFrame({'trade_date': ['20170103', '20170104'],
                                 'value': [1.0, 0.975]})
        assert_frame_equal(calculated, expected)

    @patch('ct_manager.api.get_equity_return')
    def test_evaluate_portfolio_by_weight_2(self, mock_get_equity_return):
        portfolio = pd.DataFrame({'ticker': ['000001', '000002'], 'weight': [0.5, 0.5]})
        mock_get_equity_return.return_value = pd.DataFrame(
            {'trade_date': ['20170103', '20170103', '20170104', '20170104'],
             'ticker': ['000001', '000002', '000001', '000002'],
             'pct_change': [10, 10, -10, 5]})
        calculated = evaluate_portfolio_by_weight(portfolio, '20170101', '20170104', start_value=2.0)
        expected = pd.DataFrame({'trade_date': ['20170103', '20170104'],
                                 'value': [2.0, 1.95]})
        assert_frame_equal(calculated, expected)
