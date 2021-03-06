import logging
import os
import unittest


from common.httpSet import HttpMethod
from common.operationJson import OperationJson
from config.readConfig import ReadConfig

proDir = os.path.split(os.path.realpath(__file__))[0]
file_name = os.path.join(proDir, "../../resources/product/product_create.json")

logger = logging.getLogger(__name__)


class TestProductCreate(unittest.TestCase):

    def setUp(self) -> None:
        self.http = HttpMethod()
        self.config = ReadConfig()
        self.log = Logger()
        self.json = OperationJson(file_name)
        logger.info("----------测试开始----------")

    def tearDown(self) -> None:
        logger.info("----------测试结束----------")

    def test_01_product_create(self) -> None:
        """
        创建自建商品
        """
        logger.info("test_01_product_create")

        pass


if __name__ == "__main__":
    unittest.main()
