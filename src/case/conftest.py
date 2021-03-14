#!/usr/bin/env/python3
# -*- coding:utf-8 -*-
"""
"""
import logging
import os

import pytest

from src.api import store
from src.common.db_util import DbUtil
from src.config.readConfig import ReadConfig
from src.db.store_repository import StoreRepository

logger = logging.getLogger(__name__)


@pytest.fixture(scope='session')
@pytest.mark.skip
def reset():
    cur_path = os.path.split(os.path.realpath(__file__))[0]
    file_name = os.path.join(cur_path, "../../resources/store_tables.txt")

    config = ReadConfig()
    store_repository = StoreRepository()
    store_info = store_repository.get_store_by_mobile(config.get_value('BASE', 'mobile'))

    # 清除店铺信息
    store_repository.clear_employer(store_info['store_id'])
    logger.info('店铺关联的用户已清除........')

    store_db = DbUtil('skoyi_store_jinyong')
    store_id = store_info['store_id']

    for line in open(file_name):
        clear_sql = 'delete from {} where store_id = %s'.format(line.strip())
        store_db.execute(clear_sql, store_id)
    logger.info(f"店铺{store_info['store_id']} 已清除")

    store.clear_all_cache()


def read_testcase():
    return [{'case_code': 'case_001',
             'case_title': 'get请求实现登录',
             'case_path': 'https://rbox.ruigushop.com/passport/oauth/token',
             'case_process': 'Y',
             'case_method': 'POST',
             'case_request_type': 'params',
             'case_request_data': '{"username":"lijiajia","password":"123456","grant_type":"password","scope":"server","client_id":"client_2","client_secret":"abcd"}',
             'case_expect': '{"$.code": -1}'
             },
            {'case_code': 'case_002',
             'case_title': '验证是否可正确获取区域信息',
             'case_path': 'https://rbox.ruigushop.com/metadata/system/address/provinces/cities/regions',
             'case_process': 'Y',
             'case_method': 'GET',
             'case_request_type': 'params',
             'case_request_data': '',
             'case_expect': '{"$.code": 200}'
             }]


@pytest.fixture(params=read_testcase(), scope='session')
def cases(request):
    """用例数据，测试方法参数入参该方法名 cases即可，实现同样的参数化
    目前来看相较于@pytest.mark.parametrize 更简洁。
    """
    return request.param
