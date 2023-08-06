# -*- coding: utf-8 -*-


from ct_manager.models import Base
from sqlalchemy import Column, DateTime, Index, String


class Record(Base):
    __tablename__ = 'record'
    __table_args__ = (
        Index('table_name', unique=True),
    )
    __columnnames__ = ['table_name', 'user_name', 'update_time']

    table_name = Column(String(9), primary_key=True, nullable=False)
    user_name = Column(String(9), nullable=False)
    update_time = Column(DateTime, nullable=False)
