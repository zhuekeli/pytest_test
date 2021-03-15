import logging
import os
import random

import allure
import pytest

from src.api import category, product, base, supplier
from src.common import global_variable
from src.common.json_util import OperationJson
from src.config.readConfig import ReadConfig
from src.db import product_repository

file_name = os.path.join(os.getcwd(), 'resources/product/product_create.json')

logger = logging.getLogger(__name__)
load_config = ReadConfig()


@allure.parent_suite('商品测试')
@allure.suite('商品创建测试')
class TestProductCreate(object):
    """
    商品创建 suite
    """

    @classmethod
    def setup(cls) -> None:
        cls.config = ReadConfig()
        cls.json = OperationJson(file_name)
        cls.store_id = global_variable.get_store_id()

        logger.info("------------------测试开始-----------------")

    @classmethod
    def teardown(cls) -> None:
        logger.info("------------------测试结束-----------------")

    @allure.title('创建无库存的自建商品')
    def test_01_create_product_without_inventory(self) -> None:
        """
        创建自建商品,没有库存
        """
        logger.info("test_01_create_product_without_inventory")
        # 组织数据
        category_id = category.choice_random_second_category()['id']

        product_data = self.json.get_data('create_product_without_inventory')
        product_data['categoryId'] = category_id
        product_data['name'] = product_data['name'] + str(random.randint(0, 1000))
        product_data['unit'] = base.random_unit()
        product_data['salePrice'] = base.random_price()

        # 调用接口
        resp = product.product_create(self.store_id, product_data)

        # 验证
        assert resp['code'] == 200, resp['message']
        # TODO 验证商品其他信息，例如库存。 通过查询数据库的方式验证数字是否正确
        # 验证店铺分类是否已经存在了
        store_category_list = product_repository.get_store_category(self.store_id)
        assert category_id in store_category_list, '店铺未关联上分类'

    @allure.title('创建带有库存的自建商品')
    def test_01_create_product_with_inventory(self) -> None:
        """
        创建自建商品
        带有库存
        """

        logger.info("test_01_create_product_with_inventory")
        # 组织数据
        inventory_quantity = base.random_number()
        product_data = self.json.get_data('create_product_with_inventory')
        product_data['categoryId'] = category.choice_random_second_category()['id']
        product_data['name'] = product_data['name'] + str(random.randint(0, 1000))
        product_data['unit'] = base.random_unit()
        product_data['salePrice'] = base.random_price()
        product_data['purchasePrice'] = base.random_price()
        product_data['inventoryQuantity'] = inventory_quantity  # 库存数量
        product_data['supplierName'] = supplier.random_supplier(self.store_id)['name']
        # 调用接口
        resp = product.product_create(self.store_id, product_data)
        # 接口返回的商品编码
        prod_code = resp['data']
        # 验证
        assert resp['code'] == 200, resp['message']
        # TODO 验证商品其他信息，例如库存。 通过查询数据库的方式验证数字是否正确
        # 验证库存
        inventory_quantity_from_db = product_repository.get_product_inventory_quantity(self.store_id, prod_code)
        assert inventory_quantity_from_db == inventory_quantity, '库存数量不匹配'


if __name__ == "__main__":
    pytest.main()
