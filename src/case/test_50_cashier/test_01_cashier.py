import logging
import os

import pytest

from src.api import order
from src.common.json_util import OperationJson
from src.config.readConfig import ReadConfig

cur_path = os.path.split(os.path.realpath(__file__))[0]
file_name = os.path.join(cur_path, "../../../resources/cashier/cashier.json")

logger = logging.getLogger(__name__)


class TestCashier(object):

    @classmethod
    def setup(cls) -> None:
        cls.config = ReadConfig()
        cls.json = OperationJson(file_name)
        cls.store_id = cls.config.get_value('BASE', 'base_store_id')
        logger.info("----------测试开始----------")

    @classmethod
    def teardown(cls) -> None:
        logger.info("----------测试结束----------")

    def test_01_cashier_not_customer(self) -> None:
        """
        测试下单的正常流程
        没有客户的下单
        没有临时商品
        :return:
        """
        logger.info("test_01_cashier_not_customer")

        order_data = self.json.get_data('create_order')
        resp = order.created_order(self.store_id, order_data)
        assert resp['code'] == 200, resp['message']


if __name__ == "__main__":
    pytest.main()
