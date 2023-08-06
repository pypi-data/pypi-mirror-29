# -*- coding: utf-8 -*-

import datetime as dt
import pandas as pd
from xutils import (Calendar,
                    Date)
from xutils import BizDayConventions
import sys

if sys.version_info[0] >= 3:
    unicode_type = str
    basestring_type = str
else:
    unicode_type = unicode
    basestring_type = basestring


def process_date(ds, in_format='%Y-%m-%d', out_format='%Y%m%d'):
    struct_date = dt.datetime.strptime(ds, in_format)
    str_date = struct_date.strftime(out_format)
    return str_date, struct_date


def format_data(df, date_col='trade_date', format='%Y%m%d'):
    df[date_col] = pd.to_datetime(df[date_col], format=format)


def check_holiday(this_date):
    flag = Calendar('China.SSE').isBizDay(this_date)
    return flag


def get_report_date(act_date, return_biz_day=True):
    """
    :param act_date: str/datetime.datetime, 任意日期
    :param return_biz_day: bool, 是否返回交易日
    :return: datetime, 对应应使用的报告日期， 从wind数据库中爬取
    此函数的目的是要找到，任意时刻可使用最新的季报数据的日期，比如2-20日可使用的最新季报是去年的三季报（对应日期为9-30），
    """

    if isinstance(act_date, str):
        act_date = Date.strptime(act_date)
    elif isinstance(act_date, dt.datetime):
        act_date = Date.fromDateTime(act_date)
    act_month = act_date.month()
    act_year = act_date.year()
    if 1 <= act_month <= 3:  # 第一季度使用去年三季报的数据
        year = act_year - 1
        month = 9
        day = 30
    elif 4 <= act_month <= 7:  # 第二季度使用当年一季报
        year = act_year
        month = 3
        day = 31
    elif 8 <= act_month <= 9:  # 第三季度使用当年中报
        year = act_year
        month = 6
        day = 30
    else:
        year = act_year  # 第四季度使用当年三季报
        month = 9
        day = 30
    if return_biz_day:
        date_adj = Calendar('China.SSE').adjustDate(Date(year, month, day), BizDayConventions.Preceding)
        ret = date_adj.toDateTime()
    else:
        ret = dt.datetime(year, month, day)
    return ret


def ensure_date_format(func, argname, arg):
    if len(arg) == 10:
        ret = arg[:4] + '-' + arg[5:7] + '-' + arg[8:]
        return ret
    elif len(arg) == 8:
        ret = arg[:4] + '-' + arg[4:6] + '-' + arg[6:]
        return ret
    else:
        raise ValueError("Input date format not recognized: use 'YYYYMMDD', 'YYYY-MM-DD' or 'YYYY/MM/DD'!")


def ensure_list(func, argname, arg):
    if isinstance(arg, list):
        if len(arg) == 1 and isinstance(arg[0], unicode_type):
            ret = arg[0].replace(' ', '')
            return ret.split(',')
        else:
            return arg
    elif isinstance(arg, unicode_type) or isinstance(arg, basestring_type):
        ret = arg.replace(' ', '')
        return ret.split(',')
    else:
        raise ValueError("Input format not recognized: use ['xxx','xxx'], ['xxx,xxx'] or 'xxx,xxx'!")


def check_begin_or_end_of_month(this_date, date_format='%Y%m%d'):
    date = Date.strptime(this_date, date_format)
    sse_cal = Calendar('China.SSE')
    begin_of_month = sse_cal.advanceDate(sse_cal.endOfMonth(sse_cal.advanceDate(date, '-1M')), '1B')
    if sse_cal.isEndOfMonth(date) or date == begin_of_month:
        return 1
    else:
        return 0
