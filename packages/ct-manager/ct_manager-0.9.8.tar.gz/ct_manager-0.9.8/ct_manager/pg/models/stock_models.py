# -*- coding: utf-8 -*-

from ct_manager.models import Base
from sqlalchemy import BigInteger, Column, DateTime, Float, Index, Integer, String, Text, Boolean, text


class AShareCOB(Base):
    __tablename__ = 'ashare_cob'
    __table_args__ = (Index('ticker', 'trade_date', unique=True),)
    __columnnames__ = ['ticker', 'trade_date', 'open', 'high', 'low', 'close', 'pct_change', 'vol', 'amt', 'adj_factor',
                       'avg_price', 'trade_status']
    ticker = Column(String(9), primary_key=True, nullable=False)
    trade_date = Column(DateTime, primary_key=True, nullable=False)
    open = Column(Float(53))
    high = Column(Float(53))
    low = Column(Float(53))
    close = Column(Float(53))
    pct_change = Column(Float(53))
    vol = Column(Float(53))
    amt = Column(Float(53))
    adj_factor = Column(Float(53))
    avg_price = Column(Float(53))
    trade_status = Column(String(9))


class AShareLive(Base):
    __tablename__ = 'ashare_live'
    __table_args__ = (Index('ticker', 'trade_date', unique=True),)
    __columnnames__ = ['trade_date', 'ticker', 'open', 'high', 'low', 'last', 'vol', 'amt', 'vol_ratio', 'pct_chg_5min', 'type']
    ticker = Column(String(9), primary_key=True, nullable=False)
    trade_date = Column(DateTime, primary_key=True, nullable=False)
    open = Column(Float(53))
    high = Column(Float(53))
    low = Column(Float(53))
    close = Column(Float(53))
    pct_chg_5min = Column(Float(53))
    vol = Column(Float(53))
    amt = Column(Float(53))
    type = Column(Text(4))
