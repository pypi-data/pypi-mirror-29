# -*- coding: utf-8 -*-

from ct_manager.models import Base
from sqlalchemy import BigInteger, Column, DateTime, Float, Index, Integer, String, Text, Boolean, text


class HaltList(Base):
    __tablename__ = 'halt_list'
    __table_args__ = (
        Index('halt_list_Date_Code_haltBeginTime_uindex', 'trade_date', 'code', 'halt_begin_time', unique=True),
    )

    trade_date = Column(DateTime, primary_key=True, nullable=False)
    code = Column(Integer, primary_key=True, nullable=False)
    halt_begin_time = Column(DateTime, primary_key=True, nullable=False)
    halt_end_time = Column(DateTime)
    sec_name = Column(String(20))
    exchangeCD = Column(String(4))
    list_status = Column(String(4))
    delist_date = Column(DateTime)
    asset_class = Column(String(4))


class IndexComponents(Base):
    __tablename__ = 'index_components'
    __table_args__ = (
        Index('index_ticker', 'trade_date'),
    )
    __columnnames__ = ['index_ticker', 'cons_ticker', 'trade_date', 'weight']

    trade_date = Column(DateTime, primary_key=True, nullable=False)
    index_ticker = Column(String(9), primary_key=True, nullable=False)
    cons_ticker = Column(String(9), primary_key=True, nullable=False)
    weight = Column(Float(53))


class EquityIndex(Base):
    __tablename__ = 'equity_index_cob'
    __table_args__ = (
        Index('ticker', 'trade_date'),
    )
    __columnnames__ = ['ticker', 'trade_date', 'open', 'high', 'low', 'close', 'pct_change', 'vol', 'amt']

    trade_date = Column(DateTime, primary_key=True, nullable=False)
    ticker = Column(Integer, primary_key=True, nullable=False)
    open = Column(Float(53))
    high = Column(Float(53))
    low = Column(Float(53))
    close = Column(Float(53))
    pct_change = Column(Float(53))
    amt = Column(Float(53))
    vol = Column(Float(53))


class EquityIndexLive(Base):
    __tablename__ = 'equity_index_live'
    __table_args__ = (Index('ticker', 'trade_date', unique=True),)
    __columnnames__ = ['trade_date', 'ticker', 'open', 'high', 'low', 'last', 'vol', 'amt', 'vol_ratio', 'pct_chg_5min',
                       'type']
    ticker = Column(String(9), primary_key=True, nullable=False)
    trade_date = Column(DateTime, primary_key=True, nullable=False)
    open = Column(Float(53))
    high = Column(Float(53))
    low = Column(Float(53))
    last = Column(Float(53))
    pct_chg_5min = Column(Float(53))
    vol = Column(Float(53))
    amt = Column(Float(53))
    type = Column(Text(4))


class EquityIndexLiveIntraday(Base):
    __tablename__ = 'equity_index_live_intraday'
    __table_args__ = (Index('ticker', 'trade_date', unique=True),)
    __columnnames__ = ['trade_date', 'ticker', 'open', 'high', 'low', 'last', 'vol', 'amt', 'vol_ratio', 'pct_chg_5min',
                       'type']
    ticker = Column(String(9), primary_key=True, nullable=False)
    trade_date = Column(DateTime, primary_key=True, nullable=False)
    open = Column(Float(53))
    high = Column(Float(53))
    low = Column(Float(53))
    last = Column(Float(53))
    pct_chg_5min = Column(Float(53))
    vol = Column(Float(53))
    amt = Column(Float(53))
    type = Column(Text(4))


class EquityIndexIntraday(Base):
    __tablename__ = 'equity_index_intraday'
    __table_args__ = (Index('ticker', 'trade_date', unique=True),)
    __columnnames__ = ['trade_date', 'ticker', 'open', 'high', 'low', 'last', 'vol', 'amt', 'vol_ratio', 'pct_chg_5min']
    ticker = Column(String(9), primary_key=True, nullable=False)
    trade_date = Column(DateTime, primary_key=True, nullable=False)
    open = Column(Float(53))
    high = Column(Float(53))
    low = Column(Float(53))
    last = Column(Float(53))
    pct_chg_5min = Column(Float(53))
    vol = Column(Float(53))
    amt = Column(Float(53))


class FutureIndex(Base):
    __tablename__ = 'future_index'
    __table_args__ = (
        Index('ticker', 'trade_date'),
    )
    __columnnames__ = ['ticker', 'trade_date', 'open', 'high', 'low', 'close', 'pct_change', 'vol', 'amt']

    trade_date = Column(DateTime, primary_key=True, nullable=False)
    ticker = Column(Integer, primary_key=True, nullable=False)
    open = Column(Float(53))
    high = Column(Float(53))
    low = Column(Float(53))
    close = Column(Float(53))
    pct_change = Column(Float(53))
    amt = Column(Float(53))
    vol = Column(Float(53))


class Market(Base):
    __tablename__ = 'market'
    __table_args__ = (
        Index('market_idx', 'trade_date', 'code', unique=True),
    )

    trade_date = Column(DateTime, primary_key=True, nullable=False)
    code = Column(Integer, primary_key=True, nullable=False)
    sec_name = Column(String(10))
    exchangeCD = Column(String(4))
    pre_close_price = Column(Float(53))
    act_preclose_price = Column(Float(53))
    open_price = Column(Float(53))
    highest_price = Column(Float(53))
    lowest_price = Column(Float(53))
    close_price = Column(Float(53))
    turnover_vol = Column(BigInteger)
    turnover_value = Column(Float(53))
    deal_amount = Column(BigInteger)
    turnover_rate = Column(Float(53))
    accum_adj_factor = Column(Float(53))
    neg_market_value = Column(Float(53))
    market_value = Column(Float(53))
    pct_change = Column(Float(53))
    pe = Column(Float(53))
    pe1 = Column(Float(53))
    pb = Column(Float(53))
    is_open = Column(Integer)
    vwap = Column(Float(53))


class Universe(Base):
    __tablename__ = 'universe'
    __table_args__ = (
        Index('universe_idx', 'trade_date', 'universe', 'code', unique=True),
    )

    trade_date = Column(DateTime, primary_key=True, nullable=False)
    universe = Column(String(20), primary_key=True, nullable=False)
    code = Column(Integer, primary_key=True, nullable=False)
