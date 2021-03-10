import logging
import os
import random

import pytest

from src.api import category, product, base
from src.common.json_util import OperationJson
from src.config.readConfig import ReadConfig

file_name = os.path.join(os.getcwd(), 'resources/product/product_create.json')

logger = logging.getLogger(__name__)
load_config = ReadConfig()


class TestProductSearch(object):

    @pytest.fixture(scope='class')
    def setup(self) -> None:
        self.config = ReadConfig()
        self.json = OperationJson(file_name)
        logger.info("------------------测试开始-----------------")

    @pytest.fixture(scope='class')
    def teardown(self) -> None:
        logger.info("------------------测试结束-----------------")

    def test_01_search_product_with_scan_code(self) -> None:
        """
        使用商品识别码搜索商品
        """
        logger.info("test_01_search_product_with_scan_code")
        # 获取可见的商品识别码

        product_data = self.json.get_data('create_product_without_inventory')
        product_data['categoryId'] = category.choice_random_second_category()['id']
        product_data['name'] = product_data['name'] + str(random.randint(0, 1000))
        product_data['unit'] = base.random_unit()
        product_data['salePrice'] = base.random_price()

        store_id = load_config.get_value('BASE', 'base_store_id')
        # 调用接口
        resp = product.product_create(store_id, product_data)

        # 验证
        assert resp['code'] == 200, resp['message']

    def test_01_create_product_with_inventory(self) -> None:
        """
        创建自建商品
        带有库存
        """
        logger.info("test_01_create_product_with_inventory")
        # 组织数据


if __name__ == "__main__":
    pytest.main()