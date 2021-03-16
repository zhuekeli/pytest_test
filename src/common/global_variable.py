# -*- coding: utf-8 -*-
from src.config.application_config import ApplicationConfig

config = ApplicationConfig()

_global_dict = {}


def _set_value(key, value):
    """ 定义一个全局变量 """
    _global_dict[key] = value


def _get_value(key, def_value=None):
    """ 获得一个全局变量,不存在则返回默认值 """
    try:
        return _global_dict[key]
    except KeyError:
        return def_value
    except NameError:
        return None


def get_token():
    return _get_value('token', config.get_value('BASE', 'token'))


def get_user_id():
    return _get_value('user_id', config.get_value('BASE', 'base_user_id'))


def get_store_id():
    return _get_value('store_id', config.get_value('BASE', 'base_store_id'))


def set_token(token):
    _set_value('token', token)


def set_store_id(store_id):
    _set_value('store_id', store_id)


def set_user_id(user_id):
    _set_value('user_id', user_id)
