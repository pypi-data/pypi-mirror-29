# -*- coding: utf-8 -*-


from enum import (Enum,
                  unique,
                  IntEnum)


class StrEnum(str, Enum):
    pass


@unique
class DataSource(StrEnum):
    UQER = 'Uqer'
    CT_PGSQL_LOCAL = 'CT_PostgresQL'
    WIND_ORACLE_LOCAL = 'Wind_Oracle'
    GOGOAL_ORACLE_LOCAL = 'Gogoal_Oracle'
    XRisk_ORACLE_LOCAL = 'XRisk_Oracle'
    WINDPY = 'Windpy'
    TUSHARE = 'Tushare'
    JSON = 'json'
    CSV = 'csv'


@unique
class SWIndustryLevel(IntEnum):
    L1 = 1
    L2 = 2


@unique
class PriceAdjMethod(IntEnum):
    UnAdjust = 0
    PreAdjust = 1
    PostAdjust = 2


@unique
class PriceType(StrEnum):
    Open = 'open'
    High = 'high'
    Low = 'low'
    Close = 'close'


@unique
class MiscSetting(StrEnum):
    EmailSetting = 'Email_Setting'
    OutputFile = 'Output_File'


@unique
class TrackingStrategy(StrEnum):
    DualThrust = 'DualThrust'
    RPS = 'RPS'


@unique
class ReportType(StrEnum):
    Report = 'Report'
    Preannouce = 'Preannounce'
    Express = 'Express'
