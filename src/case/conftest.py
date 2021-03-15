#!/usr/bin/env/python3
# -*- coding:utf-8 -*-
"""
"""
import logging
import os

import pytest
import yaml

from src.api import store
from src.common.db_util import DbUtil
from src.config.readConfig import ReadConfig
from src.db.store_repository import StoreRepository

logger = logging.getLogger(__name__)


@pytest.fixture(scope='session' )
def reset():
    cur_path = os.path.split(os.path.realpath(__file__))[0]
    file_name = os.path.join(cur_path, "../../resources/store_tables.txt")

    config = ReadConfig()
    store_repository = StoreRepository()
    store_info = store_repository.get_store_by_mobile(config.get_value('BASE', 'mobile'))

    # 清除店铺相关的用户信息
    store_repository.clear_employer(store_info['store_id'])
    logger.info('店铺关联的用户已清除........')

    # 清除店铺内的所有信息
    store_db = DbUtil('skoyi_store_jinyong')
    store_id = store_info['store_id']

    for line in open(file_name):
        clear_sql = 'delete from {} where store_id = %s'.format(line.strip())
        store_db.execute(clear_sql, store_id)
    logger.info(f"店铺{store_info['store_id']} 已清除")

    store.clear_all_cache()


def read_testcase():
    return [{'code': 'case_001',
             'module': '测试',
             'title': 'get请求实现登录',
             'path': 'https://rbox.ruigushop.com/passport/oauth/token',
             'process': 'Y',
             'method': 'POST',
             'request_type': 'params',
             'request_data': '{"username":"lijiajia","password":"123456","grant_type":"password","scope":"server","client_id":"client_2","client_secret":"abcd"}',
             'expect': '{"$.code": -1}'
             }]


def read_yaml():
    cur_path = os.path.split(os.path.realpath(__file__))[0]
    file_name = os.path.join(cur_path, "../../resources/test_case_data.yaml")
    with open(file_name, 'r', encoding='utf-8') as file:
        yaml_dict = yaml.load(file.read(), Loader=yaml.FullLoader)

    result = []
    for suite in yaml_dict:
        for case in suite['cases']:
            case['suite_name'] = suite['name']
            result.append(case)
    return result


@pytest.fixture(params=read_testcase(), scope='session')
def get_case_from_text(request):
    """用例数据，测试方法参数入参该方法名 cases即可，实现同样的参数化
    目前来看相较于@pytest.mark.parametrize 更简洁。
    """
    return request.param


@pytest.fixture(params=read_yaml(), scope='session')
def get_case_from_yaml(request):
    """用例数据，测试方法参数入参该方法名 cases即可，实现同样的参数化
    目前来看相较于@pytest.mark.parametrize 更简洁。
    """
    return request.param
