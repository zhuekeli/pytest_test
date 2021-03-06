import logging
import os
import random
import unittest

from src.api import category, product, base
from src.common.operationJson import OperationJson
from src.config.readConfig import ReadConfig

file_name = os.path.join(os.getcwd(), 'resources/product/product_create.json')

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
        ## 组织数据
        product_data = self.json.get_data('create_product_without_inventory')
        product_data['categoryId'] = category.choice_random_second_category()['id']
        product_data['name'] = product_data['name'] + str(random.randint(0, 1000))
        product_data['unit'] = base.random_unit()
        product_data['salePrice'] = base.random_price()

        store_id = load_config.get_value('BASE', 'base_store_id')

        resp = product.product_create(store_id, product_data)
        logger.info(resp)
        self.assertEqual(resp['code'], 200, resp['message'])


if __name__ == "__main__":
    unittest.main()
