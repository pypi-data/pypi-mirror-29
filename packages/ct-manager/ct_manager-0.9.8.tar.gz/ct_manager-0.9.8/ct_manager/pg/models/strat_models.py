# -*- coding: utf-8 -*-

from ct_manager.models import Base
from sqlalchemy import Column, DateTime, Float, Index, String, Integer


class DualThrust(Base):
    __tablename__ = 'strat_dt'
    __table_args__ = (
        Index('trade_date', 'ticker', 'dt_up', 'dt_down', unique=True),
    )

    trade_date = Column(DateTime, primary_key=True, nullable=False)
    ticker = Column(String(9), primary_key=True, nullable=False)
    dt_up = Column(Float(53), nullable=False)
    dt_down = Column(Float(53), nullable=False)


class RPS(Base):
    __tablename__ = 'strat_rps'
    __table_args__ = (
        Index('trade_date', 'ticker', 'signal', unique=True),
    )

    trade_date = Column(DateTime, primary_key=True, nullable=False)
    ticker = Column(String(9), primary_key=True, nullable=False)
    signal = Column(Integer, nullable=False)


class StratTradingRecord(Base):
    __tablename__ = 'strat_record'
    __table_args__ = (
        Index('buy_date', 'strat_name', unique=True),
    )

    buy_date = Column(DateTime, primary_key=True, nullable=False)
    sell_date = Column(DateTime, primary_key=True, nullable=False)
    strat_name = Column(String(9), primary_key=True, nullable=False)
    ticker = Column(String(9), primary_key=True, nullable=False)
