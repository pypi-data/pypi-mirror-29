# -*- coding: utf-8 -*-

from abc import abstractmethod
from toolz import merge
from toolz.compatibility import itervalues
import pandas as pd
import os
from xutils import find_and_parse_config
from argcheck import expect_types
from ct_manager.settings import Settings
from ct_manager.enums import DataSource


def _is_invalid_config(config_dict):
    value = list(itervalues(config_dict))
    if None in value:
        return True
    else:
        return False


class SimpleDataHanlder(object):
    def __init__(self, data_source):
        self.data_source = data_source

    @expect_types(data_to_save=(pd.DataFrame, pd.Series))
    def force_to_save(self, data_to_save, file_name):
        save_path = file_name.split('.')[0] + '.' + self.data_source
        if self.data_source == DataSource.CSV:
            data_to_save.to_csv(save_path)
        else:
            data_to_save.to_json(file_name)
        return

    def close(self):
        return


class DataHandler(object):
    def __init__(self, **kwargs):
        data_source = kwargs.get('data_source')
        default_config_path = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'config.yaml')
        config_connector_params = find_and_parse_config(Settings.config, default_config=default_config_path)[
            data_source]
        self.connector_params = merge(config_connector_params, kwargs)
        self.engine = None

    @property
    def data_engine(self):
        return self.engine

    @abstractmethod
    def init_db_url(self):
        raise NotImplementedError

    def execute(self, script):
        raise NotImplementedError

    def df_read_sql(self, script):
        ret = pd.read_sql(script, self.engine)
        return ret

    def df_to_sql(self, df, **kwargs):
        df.to_sql(con=self.engine, **kwargs)
        return


class MiscHandler(object):
    def __init__(self, **kwargs):
        misc_setting = Settings.misc_setting
        default_config_path = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'config.yaml')
        config_setting_params = find_and_parse_config(Settings.config, default_config=default_config_path)[misc_setting]
        self.misc_setting_params = merge(config_setting_params, kwargs)

    @property
    def misc_setting(self):
        return {} if _is_invalid_config(self.misc_setting_params) else self.misc_setting_params
