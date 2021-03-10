import logging
import os

import pytest

from src.common.json_util import OperationJson
from src.config.readConfig import ReadConfig

proDir = os.path.split(os.path.realpath(__file__))[0]
file_name = os.path.join(proDir, "../../resources/cashier/cashier.json")

logger = logging.getLogger(__name__)


class TestCashier(object):

    @classmethod
    def setup(cls) -> None:
        cls.config = ReadConfig()
        cls.json = OperationJson(file_name)
        logger.info("----------测试开始----------")

    @classmethod
    def teardown(cls) -> None:
        logger.info("----------测试结束----------")

    def test_01_cashier_not_customer(self) -> None:
        """
        测试下单的正常流程
        没有客户的下单
        :return:
        """
        logger.info("test_01_cashier")


if __name__ == "__main__":
    pytest.main()
