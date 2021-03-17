import logging
import os

import allure
import pytest

from src.common.json_util import OperationJson
from src.config.application_config import ApplicationConfig

logger = logging.getLogger(__name__)


@allure.parent_suite('收银测试')
@allure.suite('收银测试')
class TestCashier(object):

    @classmethod
    def setup(cls) -> None:
        cur_path = os.path.split(os.path.realpath(__file__))[0]
        file_name = os.path.join(cur_path, "../../../resources/cashier/cashier.json")

        cls.config = ApplicationConfig()
        cls.json = OperationJson(file_name)
        cls.store_id = cls.config.get_value('BASE', 'base_store_id')
        logger.info("----------测试开始----------")

    @classmethod
    def teardown(cls) -> None:
        logger.info("----------测试结束----------")

    def test_01_cashier_without_customer(self) -> None:
        """
        测试下单的正常流程
        没有客户的下单
        没有临时商品
        :return:
        """
        logger.info("test_01_cashier_not_customer")

        pass

    def test_02_cashier_with_customer(self) -> None:
        """
        测试下单的正常流程
        没有客户的下单
        没有临时商品
        :return:
        """
        logger.info("test_01_cashier_not_customer")

        pass


if __name__ == "__main__":
    pytest.main()
