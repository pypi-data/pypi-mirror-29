# -*- coding: utf-8 -*-

from ct_manager.models import Base
from sqlalchemy import BigInteger, Column, DateTime, Float, Index, Integer, String, Text, Boolean, text


class EquityIndexFuturesCOB(Base):
    __tablename__ = 'equity_index_fut_cob'
    __table_args__ = (
        Index('ticker', 'trade_date'),
    )
    __columnnames__ = ['ticker', 'trade_date', 'presettle', 'open', 'high', 'low', 'close', 'settle', 'vol', 'amt',
                       'oi', 'change']

    trade_date = Column(DateTime, primary_key=True, nullable=False)
    ticker = Column(Integer, primary_key=True, nullable=False)
    open = Column(Float(53))
    high = Column(Float(53))
    low = Column(Float(53))
    close = Column(Float(53))
    change = Column(Float(53))
    oi = Column(Float(53))
    presettle = Column(Float(53))
    settle = Column(Float(53))
    amt = Column(Float(53))
    vol = Column(Float(53))
