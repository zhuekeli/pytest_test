import logging

import pytest

from src.api import user
from src.common import global_variable
from src.common.db import DbUtil
from src.config.readConfig import ReadConfig

config = ReadConfig()
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def test_clear_user_db() -> None:
    """
    TODO
    清除 user 数据库
    1. 清除数据库中店铺信息
    2. 清除数据库中老板的信息
    3. 不要清除客户信息
    4. 清除客户和店铺之间的关系
    """
    user_db = DbUtil('obm_user')
    store_id = config.get_value('BASE', 'base_store_id')


@pytest.fixture(scope="session")
def test_clear_store_db() -> None:
    """
    TODO
    清除 store 数据库，清除指定店铺的所有信息
    """
    user_db = DbUtil('obm_user')
    store_id = config.get_value('BASE', 'base_store_id')


@pytest.fixture(scope="session")
def test_clear_store() -> None:
    """
    TODO
    调用接口清除店铺相关信息
    """
    user_db = DbUtil('obm_user')
    store_id = config.get_value('BASE', 'base_store_id')


@pytest.fixture(scope="session")
def test_init_store() -> None:
    """
    TODO
    初始化店铺信息
    1. 按照流程初始化信息
    2.
    """
    user_db = DbUtil('obm_user')
    store_id = config.get_value('BASE', 'base_store_id')

    logger.info("初始化 token ..........")
    response = user.login({
        "mobile": config.get_value("BASE", "mobile"),
        "password": config.get_value("BASE", "password")
    })
    global_variable.set_value("token", response['data']['token'])
    global_variable.set_value("user_id", response['data']['userId'])


@pytest.fixture(scope="session")
def test_init_store_customer():
    """
    TODO
    初始化店铺和客户之间的关系
    1. 通过调用接口的方式，让客户加入该店铺
    """
