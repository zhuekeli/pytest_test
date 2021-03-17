import logging

import allure
import pytest

from src.api import user, store
from src.common import global_variable, allure_step
from src.config.application_config import ApplicationConfig
from src.db.store_repository import StoreRepository

logger = logging.getLogger(__name__)

store_repository = StoreRepository()


def get_customer() -> list:
    """获取客户的 id 列表"""
    return store_repository.get_customer_id_list()


@allure.parent_suite('登录测试')
@allure.suite('登录测试')
class TestLogin(object):

    @classmethod
    def setup(cls) -> None:
        cls.config = ApplicationConfig()
        cls.mobile = cls.config.get_value('BASE', 'mobile')
        cls.password = cls.config.get_value('BASE', 'password')
        cls.gv = global_variable
        cls.store_repository = store_repository

        logger.info("------------------TestLogin 测试开始-----------------")

    @classmethod
    def teardown(cls) -> None:
        logger.info("------------------TestLogin 测试结束-----------------")

    def test_01_login_init_user(self) -> None:
        """
        验证店铺初始化流程
        登录时初始化用户信息
        """

        logger.info("test_01_login_init_user ..........")
        data = {"mobile": self.mobile, "password": self.password}

        allure_step('登录账户', data)
        response = user.login(data)
        # 验证是否登录成功
        assert response['result'], response['message']

        user_id = response['data']['userId']
        user_info = self.store_repository.get_user_by_id(user_id)
        assert user_info is not None, '用户信息不存在'

        allure_step('初始化的用户信息', response['data'])
        # 初始化用户的 id 和 token
        token = response['data']['token']
        self.gv.set_user_id(user_id)
        self.gv.set_token(token)

    def test_02_login_init_store(self) -> None:
        """
        查询用户锁关联的店铺信息，初始化店铺信息
        通过获取店铺信息，触发店铺的初始化操作
        """
        logger.info("test_02_login_init_store ..........")
        # 获取老板的店铺信息，可以触发初始化操作
        user_id = self.gv.get_user_id()
        allure_step('获取老板的店铺信息-初始化店铺', user_id)
        resp = user.get_store_by_user(user_id)

        assert resp['result'] and len(resp['data']) >= 1, resp['message']
        allure_step('验证店铺是否初始化成功', resp['data'])

        store = resp['data'][0]
        store_db = self.store_repository.get_store_by_mobile(self.mobile)

        assert store['id'] == store_db['store_id'], '店铺信息错误'

    @allure.title('客户登录店铺测试')
    @pytest.mark.parametrize('customer_id', get_customer())
    def test_03_init_store_customer(self, customer_id) -> None:
        """客户关联店铺"""
        # 获取客户的 token
        token_resp = user.get_user_token(customer_id)
        assert token_resp['result'], token_resp['message']

        # 客户登录店铺
        token = token_resp['data']['token']
        switch_resp = store.switch_store(self.gv.get_store_id(), customer_id, token)
        assert switch_resp['result'], switch_resp['message']

    # 验证数据的初始化
