# -*- coding: utf-8 -*-

from ct_manager.models import Base
from sqlalchemy import Column, DateTime, Float, Index, String


class Portfolio(Base):
    __tablename__ = 'portfolio'
    __table_args__ = (
        Index('trade_date', unique=True),
    )
    __columnnames__ = ['trade_date', 'product', 'ticker', 'name', 'holding', 'current_price', 'cost', 'direction', 'type']

    trade_date = Column(DateTime, primary_key=True, nullable=False)
    product = Column(String(9), primary_key=True, nullable=False)
    ticker = Column(String(9), primary_key=True, nullable=False)
    name = Column(String(9), nullable=False)
    holding = Column(Float(53), nullable=False)
    current_price = Column(Float(53), nullable=False)
    cost = Column(Float(53), nullable=False)
    direction = Column(String(9), nullable=False)
    type = Column(String(9), nullable=False)
