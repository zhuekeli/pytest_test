#!/usr/bin/env/python3
# -*- coding:utf-8 -*-
"""
"""
import logging
import os

import pytest

from src.api import store
from src.common.sql_template import SqlTemplate
from src.config import case_config
from src.config.application_config import ApplicationConfig
from src.db.store_repository import StoreRepository

logger = logging.getLogger(__name__)


@pytest.fixture(scope='session', autouse=True)
def reset():
    cur_path = os.path.split(os.path.realpath(__file__))[0]
    file_name = os.path.join(cur_path, "../../resources/store_tables.txt")

    config = ApplicationConfig()
    store_repository = StoreRepository()

    store_info = store_repository.get_store_by_mobile(config.get_value('BASE', 'mobile'))

    # 清除店铺相关的用户信息
    if store_info is not None:
        store_repository.clear_employer(store_info['store_id'])
        logger.info('店铺关联的用户已清除........')
        # 清除店铺内的所有信息
        store_db = SqlTemplate('skoyi_store_jinyong')
        store_id = store_info['store_id']

        for line in open(file_name):
            clear_sql = 'delete from {} where store_id = %s'.format(line.strip())
            store_db.execute(clear_sql, store_id)
        logger.info(f"店铺{store_info['store_id']} 已清除")

    store.clear_all_cache()


@pytest.fixture(params=case_config.read_case_data(), scope='session')
def get_case(request):
    """用例数据，测试方法参数入参该方法名 cases即可，实现同样的参数化
    目前来看相较于@pytest.mark.parametrize 更简洁。
    """
    return request.param
