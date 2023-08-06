# -*- coding: utf-8 -*-


from ct_manager.utils.date_utils import (process_date,
                                         check_holiday,
                                         format_data,
                                         ensure_date_format,
                                         ensure_list,
                                         check_begin_or_end_of_month)

__all__ = ['process_date',
           'check_holiday',
           'format_data',
           'remove_suffix',
           'universe_ticker',
           'ensure_date_format',
           'ensure_list',
           'check_begin_or_end_of_month',
           'calc_return_on_signal']


def remove_suffix(df, column_name):
    return df[column_name].apply(lambda x: x[0:6])


def universe_ticker(ticker):
    ticker = ticker.lower()
    if ticker in ['000016', 'sz50', '50']:
        return '000016'
    elif ticker in ['000300', '399300', 'hs300', '300']:
        return '399300'
    elif ticker in ['000905', '399905', 'zz500', '500']:
        return '000905'
    elif ticker in ['000852', 'zz1000', '1000']:
        return '000852'
    else:
        return 'ashare' or 'fullA'


def calc_return_on_signal(df):
    """
    :param df: DataFrame, col = ['trade_date', 'pct_change', 'signal']
    :return: DataFrame, col = ['trade_date', 'cumul_return']
    计算根据信号得到的净值曲线: 当日的信号 对应 下一日的操作 - 下一日的收益

    """
    df['pct_change_direction'] = df['pct_change'] * df['signal'].shift(1).fillna(0)
    df['cumul_return'] = df['pct_change_direction'].apply(lambda x: 1 + x / 100.0).cumprod()
    return df[['trade_date', 'cumul_return']]
