import logging
import os
import random

import allure
import pytest

from src.api import category, product, base
from src.common import global_variable
from src.common.json_util import OperationJson
from src.config.application_config import ApplicationConfig

logger = logging.getLogger(__name__)


@allure.parent_suite('商品测试')
@allure.suite('商品搜索测试')
class TestProductSearch(object):

    @classmethod
    def setup(cls) -> None:
        cur_path = os.path.split(os.path.realpath(__file__))[0]
        file_name = os.path.join(cur_path, "../../../resources/product/product_create.json")

        cls.config = ApplicationConfig()
        cls.json = OperationJson(file_name)
        cls.store_id = global_variable.get_store_id()
        logger.info("------------------TestProductSearch 测试开始-----------------")

    @classmethod
    def teardown(cls) -> None:
        logger.info("------------------TestProductSearch 测试结束-----------------")

    @pytest.mark.skip(reason='not work')
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

        # 调用接口
        resp = product.product_create(self.store_id, product_data)

        # 验证
        assert resp['code'] == 200, resp['message']


if __name__ == "__main__":
    pytest.main()
