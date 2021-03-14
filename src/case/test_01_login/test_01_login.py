import logging

from src.api import user
from src.common import global_variable
from src.config.readConfig import ReadConfig
from src.db.store_repository import StoreRepository

logger = logging.getLogger(__name__)


class TestLogin(object):

    @classmethod
    def setup(cls) -> None:
        cls.config = ReadConfig()
        cls.store_repository = StoreRepository()
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
        response = user.login({
            "mobile": self.config.get_value("BASE", "mobile"),
            "password": self.config.get_value("BASE", "password")
        })
        # 验证是否登录成功
        assert response['result'], response['message']

        user_id = response['data']['userId']
        user_info = self.store_repository.get_user_by_id(user_id)
        assert user_info is not None, '用户信息不存在'

        # 初始化用户的 id 和 token
        token = response['data']['token']
        global_variable.set_user_id(user_id)
        global_variable.set_token(token)

    def test_02_login_init_store(self):
        """
        查询用户锁关联的店铺信息，初始化店铺信息
        通过获取店铺信息，触发店铺的初始化操作
        """
        logger.info("test_02_login_init_store ..........")
        # 获取老板的店铺信息，可以触发初始化操作

        stores = user.get_store_by_user(global_variable.get_user_id())

        assert len(stores) >= 1, '未获取的老板的店铺信息'
