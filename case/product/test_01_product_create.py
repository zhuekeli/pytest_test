import logging
import os
import unittest

from api import category, product
from common.operationJson import OperationJson
from config.readConfig import ReadConfig

proDir = os.path.split(os.path.realpath(__file__))[0]
file_name = os.path.join(proDir, "../../resources/product/product_create.json")

logger = logging.getLogger(__name__)
load_config = ReadConfig()


class TestProductCreate(unittest.TestCase):

    def setUp(self) -> None:
        self.config = ReadConfig()
        self.json = OperationJson(file_name)
        logger.info("----------测试开始----------")

    def tearDown(self) -> None:
        logger.info("----------测试结束----------")

    def test_01_create_product_without_inventory(self) -> None:
        """
        创建自建商品,没有库存
        """
        logger.info("test_01_product_create")
        product_data = self.json.get_data('create_product_without_inventory')
        product_data['categoryId'] = category.choice_random_second_category()['id']
        store_id = load_config.get_value('BASE', 'base_store_id')

        resp = product.product_create(store_id, product_data)
        logger.info(resp)
        self.assertEqual(resp['code'], 200, resp['message'])


if __name__ == "__main__":
    unittest.main()
