# -*- coding: utf-8 -*-

from ct_manager.models import Base
from sqlalchemy import Column, DateTime, Index, String


class Industry(Base):
    __tablename__ = 'industry'
    __table_args__ = (
        Index('trade_date', unique=True),
    )
    __columnnames__ = ['trade_date', 'ticker', 'name', 'into_date', 'out_date', 'ind_1', 'ind_name_1', 'ind_2', 'ind_name_2']

    trade_date = Column(DateTime, primary_key=True, nullable=False)
    ticker = Column(String(9), primary_key=True, nullable=False)
    name = Column(String(9), nullable=False)
    into_date = Column(DateTime, nullable=False)
    out_date = Column(DateTime, nullable=False)
    ind_1 = Column(String(9), nullable=False)
    ind_name_1 = Column(String(9), nullable=False)
    ind_2 = Column(String(9), nullable=False)
    ind_name_2 = Column(String(9), nullable=False)