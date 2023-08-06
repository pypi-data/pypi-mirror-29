# -*- coding: utf-8 -*-

from ct_manager.models import Base
from sqlalchemy import BigInteger, Column, DateTime, Float, Index, Integer, String, Text, Boolean, text


class RiskCovDay(Base):
    __tablename__ = 'risk_cov_day'
    __table_args__ = (
        Index('risk_cov_day_idx', 'trade_date', 'FactorID', 'Factor', unique=True),
    )

    trade_date = Column(DateTime, primary_key=True, nullable=False)
    FactorID = Column(Integer, nullable=False)
    Factor = Column(String(50), primary_key=True, nullable=False)
    BETA = Column(Float(53))
    MOMENTUM = Column(Float(53))
    SIZE = Column(Float(53))
    EARNYILD = Column(Float(53))
    RESVOL = Column(Float(53))
    GROWTH = Column(Float(53))
    BTOP = Column(Float(53))
    LEVERAGE = Column(Float(53))
    LIQUIDTY = Column(Float(53))
    SIZENL = Column(Float(53))
    Bank = Column(Float(53))
    RealEstate = Column(Float(53))
    Health = Column(Float(53))
    Transportation = Column(Float(53))
    Mining = Column(Float(53))
    NonFerMetal = Column(Float(53))
    HouseApp = Column(Float(53))
    LeiService = Column(Float(53))
    MachiEquip = Column(Float(53))
    BuildDeco = Column(Float(53))
    CommeTrade = Column(Float(53))
    CONMAT = Column(Float(53))
    Auto = Column(Float(53))
    Textile = Column(Float(53))
    FoodBever = Column(Float(53))
    Electronics = Column(Float(53))
    Computer = Column(Float(53))
    LightIndus = Column(Float(53))
    Utilities = Column(Float(53))
    Telecom = Column(Float(53))
    AgriForest = Column(Float(53))
    CHEM = Column(Float(53))
    Media = Column(Float(53))
    IronSteel = Column(Float(53))
    NonBankFinan = Column(Float(53))
    ELECEQP = Column(Float(53))
    AERODEF = Column(Float(53))
    Conglomerates = Column(Float(53))
    COUNTRY = Column(Float(53))
    updateTime = Column(DateTime)


class RiskCovLong(Base):
    __tablename__ = 'risk_cov_long'
    __table_args__ = (
        Index('risk_cov_long_Date_Factor_uindex', 'trade_date', 'Factor', unique=True),
        Index('risk_cov_long_Date_FactorID_uindex', 'trade_date', 'FactorID', unique=True)
    )

    trade_date = Column(DateTime, primary_key=True, nullable=False)
    FactorID = Column(Integer)
    Factor = Column(String(50), primary_key=True, nullable=False)
    BETA = Column(Float(53))
    MOMENTUM = Column(Float(53))
    SIZE = Column(Float(53))
    EARNYILD = Column(Float(53))
    RESVOL = Column(Float(53))
    GROWTH = Column(Float(53))
    BTOP = Column(Float(53))
    LEVERAGE = Column(Float(53))
    LIQUIDTY = Column(Float(53))
    SIZENL = Column(Float(53))
    Bank = Column(Float(53))
    RealEstate = Column(Float(53))
    Health = Column(Float(53))
    Transportation = Column(Float(53))
    Mining = Column(Float(53))
    NonFerMetal = Column(Float(53))
    HouseApp = Column(Float(53))
    LeiService = Column(Float(53))
    MachiEquip = Column(Float(53))
    BuildDeco = Column(Float(53))
    CommeTrade = Column(Float(53))
    CONMAT = Column(Float(53))
    Auto = Column(Float(53))
    Textile = Column(Float(53))
    FoodBever = Column(Float(53))
    Electronics = Column(Float(53))
    Computer = Column(Float(53))
    LightIndus = Column(Float(53))
    Utilities = Column(Float(53))
    Telecom = Column(Float(53))
    AgriForest = Column(Float(53))
    CHEM = Column(Float(53))
    Media = Column(Float(53))
    IronSteel = Column(Float(53))
    NonBankFinan = Column(Float(53))
    ELECEQP = Column(Float(53))
    AERODEF = Column(Float(53))
    Conglomerates = Column(Float(53))
    COUNTRY = Column(Float(53))
    updateTime = Column(DateTime)


class RiskCovShort(Base):
    __tablename__ = 'risk_cov_short'
    __table_args__ = (
        Index('risk_cov_short_Date_FactorID_uindex', 'trade_date', 'FactorID', unique=True),
        Index('risk_cov_short_Date_Factor_uindex', 'trade_date', 'Factor', unique=True)
    )

    trade_date = Column(DateTime, primary_key=True, nullable=False)
    FactorID = Column(Integer)
    Factor = Column(String(50), primary_key=True, nullable=False)
    BETA = Column(Float(53))
    MOMENTUM = Column(Float(53))
    SIZE = Column(Float(53))
    EARNYILD = Column(Float(53))
    RESVOL = Column(Float(53))
    GROWTH = Column(Float(53))
    BTOP = Column(Float(53))
    LEVERAGE = Column(Float(53))
    LIQUIDTY = Column(Float(53))
    SIZENL = Column(Float(53))
    Bank = Column(Float(53))
    RealEstate = Column(Float(53))
    Health = Column(Float(53))
    Transportation = Column(Float(53))
    Mining = Column(Float(53))
    NonFerMetal = Column(Float(53))
    HouseApp = Column(Float(53))
    LeiService = Column(Float(53))
    MachiEquip = Column(Float(53))
    BuildDeco = Column(Float(53))
    CommeTrade = Column(Float(53))
    CONMAT = Column(Float(53))
    Auto = Column(Float(53))
    Textile = Column(Float(53))
    FoodBever = Column(Float(53))
    Electronics = Column(Float(53))
    Computer = Column(Float(53))
    LightIndus = Column(Float(53))
    Utilities = Column(Float(53))
    Telecom = Column(Float(53))
    AgriForest = Column(Float(53))
    CHEM = Column(Float(53))
    Media = Column(Float(53))
    IronSteel = Column(Float(53))
    NonBankFinan = Column(Float(53))
    ELECEQP = Column(Float(53))
    AERODEF = Column(Float(53))
    Conglomerates = Column(Float(53))
    COUNTRY = Column(Float(53))
    updateTime = Column(DateTime)


class RiskExposure(Base):
    __tablename__ = 'risk_exposure'
    __table_args__ = (
        Index('risk_exposure_idx', 'trade_date', 'ticker', unique=True),
    )

    trade_date = Column(DateTime, primary_key=True, nullable=False)
    ticker = Column(String(9), primary_key=True, nullable=False)
    exchangeCD = Column(String(4))
    secShortName = Column(String(20))
    BETA = Column(Float(53))
    MOMENTUM = Column(Float(53))
    SIZE = Column(Float(53))
    EARNYILD = Column(Float(53))
    RESVOL = Column(Float(53))
    GROWTH = Column(Float(53))
    BTOP = Column(Float(53))
    LEVERAGE = Column(Float(53))
    LIQUIDTY = Column(Float(53))
    SIZENL = Column(Float(53))
    Bank = Column(BigInteger)
    RealEstate = Column(BigInteger)
    Health = Column(BigInteger)
    Transportation = Column(BigInteger)
    Mining = Column(BigInteger)
    NonFerMetal = Column(BigInteger)
    HouseApp = Column(BigInteger)
    LeiService = Column(BigInteger)
    MachiEquip = Column(BigInteger)
    BuildDeco = Column(BigInteger)
    CommeTrade = Column(BigInteger)
    CONMAT = Column(BigInteger)
    Auto = Column(BigInteger)
    Textile = Column(BigInteger)
    FoodBever = Column(BigInteger)
    Electronics = Column(BigInteger)
    Computer = Column(BigInteger)
    LightIndus = Column(BigInteger)
    Utilities = Column(BigInteger)
    Telecom = Column(BigInteger)
    AgriForest = Column(BigInteger)
    CHEM = Column(BigInteger)
    Media = Column(BigInteger)
    IronSteel = Column(BigInteger)
    NonBankFinan = Column(BigInteger)
    ELECEQP = Column(BigInteger)
    AERODEF = Column(BigInteger)
    Conglomerates = Column(BigInteger)
    COUNTRY = Column(BigInteger)
    updateTime = Column(DateTime)


class RiskMaster(Base):
    __tablename__ = 'risk_master'

    factor = Column(String(30), nullable=False, unique=True)
    source = Column(String(30), nullable=False)
    alias = Column(String(30), nullable=False)
    type = Column(String(30))
    updateTime = Column(DateTime)
    description = Column(Text)
    FactorID = Column(Integer, primary_key=True, unique=True)
    vendor = Column(String(30))


class RiskReturn(Base):
    __tablename__ = 'risk_return'

    trade_date = Column(DateTime, primary_key=True, unique=True)
    BETA = Column(Float(53))
    MOMENTUM = Column(Float(53))
    SIZE = Column(Float(53))
    EARNYILD = Column(Float(53))
    RESVOL = Column(Float(53))
    GROWTH = Column(Float(53))
    BTOP = Column(Float(53))
    LEVERAGE = Column(Float(53))
    LIQUIDTY = Column(Float(53))
    SIZENL = Column(Float(53))
    Bank = Column(Float(53))
    RealEstate = Column(Float(53))
    Health = Column(Float(53))
    Transportation = Column(Float(53))
    Mining = Column(Float(53))
    NonFerMetal = Column(Float(53))
    HouseApp = Column(Float(53))
    LeiService = Column(Float(53))
    MachiEquip = Column(Float(53))
    BuildDeco = Column(Float(53))
    CommeTrade = Column(Float(53))
    CONMAT = Column(Float(53))
    Auto = Column(Float(53))
    Textile = Column(Float(53))
    FoodBever = Column(Float(53))
    Electronics = Column(Float(53))
    Computer = Column(Float(53))
    LightIndus = Column(Float(53))
    Utilities = Column(Float(53))
    Telecom = Column(Float(53))
    AgriForest = Column(Float(53))
    CHEM = Column(Float(53))
    Media = Column(Float(53))
    IronSteel = Column(Float(53))
    NonBankFinan = Column(Float(53))
    ELECEQP = Column(Float(53))
    AERODEF = Column(Float(53))
    Conglomerates = Column(Float(53))
    COUNTRY = Column(Float(53))
    updateTime = Column(DateTime)


class RiskStat(Base):
    __tablename__ = 'risk_stats'
    __table_args__ = (
        Index('risk_stats_uindex', 'trade_date', 'type', 'portfolio', 'source', 'universe', 'benchmark', 'factor',
              unique=True),
    )

    trade_date = Column(DateTime, primary_key=True, nullable=False)
    type = Column(String(20), primary_key=True, nullable=False)
    portfolio = Column(String(50), primary_key=True, nullable=False)
    source = Column(String(20), primary_key=True, nullable=False)
    universe = Column(String(50), primary_key=True, nullable=False)
    benchmark = Column(Integer, primary_key=True, nullable=False)
    factor = Column(String(30), primary_key=True, nullable=False)
    exposure = Column(Float(53))


class SpecificRiskDay(Base):
    __tablename__ = 'specific_risk_day'
    __table_args__ = (
        Index('specific_risk_day_Date_Code_uindex', 'trade_date', 'ticker', unique=True),
    )

    trade_date = Column(DateTime, primary_key=True, nullable=False)
    ticker = Column(String(9), primary_key=True, nullable=False)
    exchangeCD = Column(String(4))
    secShortName = Column(String(20))
    SRISK = Column(Float(53))
    updateTime = Column(DateTime)


class SpecificRiskLong(Base):
    __tablename__ = 'specific_risk_long'
    __table_args__ = (
        Index('specific_risk_long_Date_Code_uindex', 'trade_date', 'ticker', unique=True),
    )

    trade_date = Column(DateTime, primary_key=True, nullable=False)
    ticker = Column(String(9), primary_key=True, nullable=False)
    exchangeCD = Column(String(4))
    secShortName = Column(String(20))
    updateTime = Column(DateTime)
    SRISK = Column(Float(53))


class SpecificRiskShort(Base):
    __tablename__ = 'specific_risk_short'
    __table_args__ = (
        Index('specific_risk_short_Date_Code_uindex', 'trade_date', 'ticker', unique=True),
    )

    trade_date = Column(DateTime, primary_key=True, nullable=False)
    ticker = Column(String(9), primary_key=True, nullable=False)
    exchangeCD = Column(String(4))
    secShortName = Column(String(20))
    SRISK = Column(Float(53))
    updateTime = Column(DateTime)


class SpecificReturn(Base):
    __tablename__ = 'specific_return'
    __table_args__ = (
        Index('specific_return_Date_Code_uindex', 'trade_date', 'ticker', unique=True),
    )

    trade_date = Column(DateTime, primary_key=True, nullable=False)
    ticker = Column(String(9), primary_key=True, nullable=False)
    exchangeCD = Column(String(4))
    secShortName = Column(String(20))
    spret = Column(Float(53))
    updateTime = Column(DateTime)
