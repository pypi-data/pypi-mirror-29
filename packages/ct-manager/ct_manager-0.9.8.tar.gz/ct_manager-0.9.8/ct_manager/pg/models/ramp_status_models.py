# -*- coding: utf-8 -*-

from ct_manager.models import Base
from sqlalchemy import Column, String, Index


class RampStatus(Base):
    __tablename__ = 'ramp_status'
    __table_args__ = (
        Index('contrib_time', unique=True),
    )
    __columnnames__ = ['contrib_time', 'table_name', 'table_size', 'live_tup', 'dead_tup', 'last_vacuum', 'last_analyze',
                       'last_autovacuum', 'last_autoanalyze']

    contrib_time = Column(String(53), primary_key=True, nullable=False)
    table_name = Column(String(53), nullable=False)
    table_size = Column(String(53), nullable=False)
    live_tup = Column(String(53), nullable=False)
    dead_tup = Column(String(53), nullable=False)
    last_vacuum = Column(String(53), nullable=False)
    last_analyze = Column(String(53), nullable=False)
    last_autovacuum = Column(String(53), nullable=False)
    last_autoanalyze = Column(String(53), nullable=False)