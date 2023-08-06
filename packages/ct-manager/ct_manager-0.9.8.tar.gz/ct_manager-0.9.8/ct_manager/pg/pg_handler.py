# -*- coding: utf-8 -*-

from datetime import datetime as dt
import pandas as pd
import sqlalchemy as sa
import sqlalchemy.orm as orm
import sys
import time
from sqlalchemy import (select,
                        and_,
                        delete)
from sqlalchemy.exc import ProgrammingError
from ct_manager.base_handler import DataHandler
from ct_manager.settings import Settings
from ct_manager.enums import (DataSource,
                              SWIndustryLevel,
                              TrackingStrategy)
from ct_manager.pg.models import (AShareCOB,
                                  AShareLive,
                                  IndexComponents,
                                  Industry,
                                  EquityIndex,
                                  FutureIndex,
                                  EquityIndexFuturesCOB,
                                  Portfolio,
                                  DualThrust,
                                  RPS,
                                  Record,
                                  StratTradingRecord)


class PGDataHandler(DataHandler):
    def __init__(self, **kwargs):
        super(PGDataHandler, self).__init__(data_source=DataSource.CT_PGSQL_LOCAL, **kwargs)
        self.user = Settings.ramp_user
        self.host = self.connector_params['host']
        self.port = self.connector_params['port']
        self.database = self.connector_params['database']
        self.db_url = self.init_db_url()
        self.engine = sa.create_engine(self.db_url)
        self.session = None
        self.create_session()

    def init_db_url(self):
        db_url = 'postgresql+psycopg2://{user}@{host}:{port}/{database}'.format(user=self.user,
                                                                                host=self.host,
                                                                                port=self.port,
                                                                                database=self.database)
        return db_url

    def create_session(self):
        db_session = orm.sessionmaker(bind=self.engine)
        self.session = db_session()

    def execute(self, script):
        self.engine.execute(script)
        return

    def update_record(self, table_name):
        try:
            query = delete(Record).where(Record.table_name == table_name)
            self.execute(query)
        except ProgrammingError:
            pass
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        df = pd.DataFrame(
            {Record.table_name.name: [table_name],
             Record.user_name.name: [self.user],
             Record.update_time.name: [current_time]})
        df = df[[Record.table_name.name, Record.user_name.name, Record.update_time.name]]
        df.to_sql(Record.__tablename__, self.engine, index=False, if_exists='append')
        return

    def get_pg_version(self):
        """
        Get PostgreSQL server version.
        """
        query = "SELECT version() AS pg_version"
        cursor = self.engine.execute(query)
        ret = cursor.fetchone()
        return ret['pg_version']

    def close(self):
        if not self.session:
            self.session.close()

    def get_industry_map(self, ref_date, sw_level):
        if sw_level == SWIndustryLevel.L1:
            query = select([Industry.ticker, Industry.name, Industry.ind_1, Industry.ind_name_1]). \
                where(
                and_(Industry.into_date <= ref_date,
                     Industry.out_date >= ref_date)
            )
        else:
            query = select([Industry.ticker, Industry.name, Industry.ind_2, Industry.ind_name_2]). \
                where(
                and_(Industry.into_date <= ref_date,
                     Industry.out_date >= ref_date)
            )

        ret = self.df_read_sql(query)
        return ret

    def get_index_component(self, ref_date, index_ticker, out_weight):
        if index_ticker == 'ashare':
            query = select([AShareCOB.ticker]). \
                where(AShareCOB.trade_date == ref_date)
        else:
            if out_weight:
                query = select([IndexComponents.cons_ticker,
                                IndexComponents.weight]). \
                    where(
                    and_(IndexComponents.trade_date == ref_date,
                         IndexComponents.index_ticker == index_ticker)
                )
            else:
                query = select([IndexComponents.cons_ticker]). \
                    where(
                    and_(IndexComponents.trade_date == ref_date,
                         IndexComponents.index_ticker == index_ticker)
                )
        ret = self.df_read_sql(query)
        return ret

    def get_equity_market_cob(self, ticker, ref_date, fields, is_index):
        if is_index:
            query_fields = [eval('EquityIndex.' + field) for field in fields]
            query_fields.extend([EquityIndex.ticker, EquityIndex.trade_date])
            query = select(query_fields).where(
                and_(EquityIndex.trade_date == ref_date,
                     EquityIndex.ticker.in_(ticker))
            )
        else:
            query_fields = [eval('AShareCOB.' + field) for field in fields]
            query_fields.extend([AShareCOB.ticker, AShareCOB.trade_date])
            if ticker == ['ashare']:
                query = select(query_fields).where(
                    AShareCOB.trade_date == ref_date
                )
            else:
                query = select(query_fields).where(
                    and_(AShareCOB.trade_date == ref_date,
                         AShareCOB.ticker.in_(ticker))
                )

        ret = self.df_read_sql(query)
        return ret

    def get_equity_market_range(self, ticker, start_date, end_date, fields, is_index):
        if is_index:
            query_fields = [eval('EquityIndex.' + field) for field in fields]
            query_fields.extend([EquityIndex.ticker, EquityIndex.trade_date])
            query = select(query_fields).where(
                and_(EquityIndex.trade_date >= start_date,
                     EquityIndex.trade_date <= end_date,
                     EquityIndex.ticker.in_(ticker))
            ).order_by(EquityIndex.trade_date)
        else:
            query_fields = [eval('AShareCOB.' + field) for field in fields]
            query_fields.extend([AShareCOB.ticker, AShareCOB.trade_date])
            if ticker == ['ashare']:
                query = select(query_fields).where(
                    and_(AShareCOB.trade_date >= start_date,
                         AShareCOB.trade_date <= end_date)
                ).order_by(AShareCOB.trade_date)
            else:
                query = select(query_fields).where(
                    and_(AShareCOB.trade_date >= start_date,
                         AShareCOB.trade_date <= end_date,
                         AShareCOB.ticker.in_(ticker))
                ).order_by(AShareCOB.trade_date)
        ret = self.df_read_sql(query)
        return ret

    def get_strat_signal(self, ticker, start_date, end_date, strategy):
        model = DualThrust if strategy == TrackingStrategy.DualThrust else RPS
        query = select(['*']).where(
            and_(model.trade_date >= start_date,
                 model.trade_date <= end_date,
                 model.ticker.in_(ticker)))

        ret = self.df_read_sql(query)
        return ret

    def get_portfolio_holding(self, ptf_name, start_date, end_date):
        query = select(['*']).where(
            and_(Portfolio.trade_date >= start_date,
                 Portfolio.trade_date <= end_date,
                 Portfolio.product == ptf_name))
        ret = self.df_read_sql(query)
        return ret

    def update_strat_trading_record(self, df):
        df.to_sql(StratTradingRecord.__tablename__, self.engine, index=False, if_exists='append')
        self.update_record(StratTradingRecord.__tablename__)
        return

    @staticmethod
    def get_col_names(table):
        """
        :param table: model or string(tableName of model)
        :return: columnnames of model
        """
        models_import = dir(sys.modules[__name__])
        for model in models_import:
            try:
                if table == eval(model).__tablename__:
                    return eval(model).__columnnames__
            except AttributeError:
                pass
        return eval(table).__columnnames__

    """
    Database Maintenance Functions 
    """

    def maintenance_vacuum_analyze(self):
        """
        执行数据库清理操作
        """
        query = 'VACUUM ANALYZE'
        engine = sa.create_engine(self.db_url, isolation_level='AUTOCOMMIT')
        ret = engine.execute(query)
        return ret

    def maintenance_database_size(self, db_name):
        """
        查看某数据库占用的空间大小
        """
        query = '''select pg_size_pretty(pg_database_size('{db_name}'))'''.format(db_name=db_name)
        ret = self.df_read_sql(query)['pg_size_pretty']
        return ret

    def maintenance_pg_stat(self):
        query = '''with query1 as 
        (select table_name, pg_size_pretty(pg_relation_size(table_name)) from information_schema.tables 
        where table_schema='public' order by pg_relation_size(table_name) DESC),
        query2 as 
        (select relname, n_live_tup, n_dead_tup, last_vacuum, last_analyze, last_autovacuum, last_autoanalyze 
        from pg_stat_all_tables where schemaname = 'public') 
        select table_name, pg_size_pretty, n_live_tup, n_dead_tup, last_vacuum, last_analyze, last_autovacuum, 
        last_autoanalyze from query1 inner join query2 on query1.table_name = query2.relname'''
        ret = self.df_read_sql(query)
        ret = ret.assign(contrib_time=str(dt.today()))
        ret.columns = ['table_name', 'table_size', 'live_tup', 'dead_tup', 'last_vacuum',
                       'last_analyze', 'last_autovacuum', 'last_autoanalyze', 'contrib_time']
        ret = ret[['contrib_time', 'table_name', 'table_size', 'live_tup', 'dead_tup',
                   'last_vacuum', 'last_analyze', 'last_autovacuum', 'last_autoanalyze']]
        ret = ret.applymap(str)
        return ret

