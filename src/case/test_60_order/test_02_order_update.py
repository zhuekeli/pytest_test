import logging
import os

import allure
import pytest

from src.common import global_variable
from src.common.json_util import OperationJson
from src.config.application_config import ApplicationConfig

logger = logging.getLogger(__name__)

cur_path = os.path.split(os.path.realpath(__file__))[0]
file_name = os.path.join(cur_path, "../../../resources/order/order_update.json")

operation_json = OperationJson(file_name)
store_id = global_variable.get_store_id()
config = ApplicationConfig()


def get_update_order_data():
    pass


@allure.parent_suite('订单测试测试')
@allure.suite('订单编辑编辑测试')
class TestSupplierUpdate(object):
    """
    订单编辑 suite
    """

    @classmethod
    def setup(cls) -> None:
        cls.store_id = global_variable.get_store_id()
        logger.info("------------------测试开始-----------------")

    @classmethod
    def teardown(cls) -> None:
        logger.info("------------------测试结束-----------------")

    @allure.title('编辑订单')
    @pytest.mark.parametrize('supplier_data', get_update_order_data())
    def test_01_update_order(self, supplier_data) -> None:
        """编辑订单信息"""
        logger.info("test_01_update_order")

        # 已完成 不可修改

        # 已取消 不可修改

        # 订单中商品为空 不能修改

    @allure.title('编辑订单状态')
    def test_02_update_order_status(self):
        """编辑订单状态"""
        logger.info("test_02_update_order_status")

        # 已完成 不可修改

        # 已取消 不可修改

    @allure.title('整单改价')
    def test_03_update_order_amount(self):
        """整单改价"""
        logger.info("test_03_update_order_amount")

        # 已完成 不可修改

        # 已取消 不可修改

        # 校验 实付金额和折扣


if __name__ == "__main__":
    pytest.main()
