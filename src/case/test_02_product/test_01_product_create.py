import logging
import os
import random

import allure
import pytest

from src.api import category, product, base, supplier
from src.common import global_variable
from src.common.json_util import OperationJson
from src.config.application_config import ApplicationConfig
from src.db.product_repository import ProductRepository

logger = logging.getLogger(__name__)

cur_path = os.path.split(os.path.realpath(__file__))[0]
file_name = os.path.join(cur_path, "../../../resources/product/product_create.json")

operation_json = OperationJson(file_name)
store_id = global_variable.get_store_id()
config = ApplicationConfig()


def get_product_data_with_inventory():
    """获取有库存的商品创建数据"""
    product_data = operation_json.get_data('create_product_with_inventory')
    product_data['categoryId'] = category.choice_random_second_category()['id']
    product_data['name'] = product_data['name'] + str(random.randint(0, 1000))
    product_data['unit'] = base.random_unit()
    product_data['salePrice'] = base.random_price()
    product_data['purchasePrice'] = base.random_price()
    product_data['inventoryQuantity'] = base.random_number()  # 库存数量
    product_data['supplierName'] = supplier.random_supplier(store_id)['name']
    return [product_data]


def get_product_data_without_inventory():
    """获取无库存的商品创建数据"""
    category_id = category.choice_random_second_category()['id']

    product_data = operation_json.get_data('create_product_without_inventory')
    product_data['categoryId'] = category_id
    product_data['name'] = product_data['name'] + str(random.randint(0, 1000))
    product_data['unit'] = base.random_unit()
    product_data['salePrice'] = base.random_price()
    return [product_data]


@allure.parent_suite('商品测试')
@allure.suite('商品创建测试')
class TestProductCreate(object):
    """
    商品创建 suite
    """

    @classmethod
    def setup(cls) -> None:
        cls.product_repository = ProductRepository()
        cls.store_id = global_variable.get_store_id()
        logger.info("------------------测试开始-----------------")

    @classmethod
    def teardown(cls) -> None:
        logger.info("------------------测试结束-----------------")

    @allure.title('创建无库存的自建商品')
    @pytest.mark.parametrize('product_data', get_product_data_without_inventory())
    def test_01_create_product_without_inventory(self, product_data) -> None:
        """
        创建自建商品,没有库存
        """
        logger.info("test_01_create_product_without_inventory")
        # 组织数据
        category_id = product_data['categoryId']

        # 调用接口
        resp = product.product_create(self.store_id, product_data)

        # 验证
        assert resp['code'] == 200, resp['message']
        # TODO 验证商品其他信息，例如库存。 通过查询数据库的方式验证数字是否正确
        # 验证店铺分类是否已经存在了
        store_category_list = self.product_repository.get_store_category(self.store_id)
        assert category_id in store_category_list, '店铺未关联上分类'

    @allure.title('创建带有库存的自建商品')
    @pytest.mark.parametrize('product_data', get_product_data_with_inventory())
    def test_02_create_product_with_inventory(self, product_data) -> None:
        """
        创建自建商品
        带有库存
        """

        logger.info("test_01_create_product_with_inventory")
        # 组织数据
        inventory_quantity = product_data['inventoryQuantity']
        # 调用接口
        resp = product.product_create(self.store_id, product_data)
        # 接口返回的商品编码
        prod_code = resp['data']
        # 验证
        assert resp['code'] == 200, resp['message']
        # TODO 验证商品其他信息，例如库存。 通过查询数据库的方式验证数字是否正确
        # 验证库存
        inventory_quantity_from_db = self.product_repository.get_product_inventory_quantity(self.store_id, prod_code)
        assert inventory_quantity_from_db == inventory_quantity, '库存数量不匹配'


if __name__ == "__main__":
    pytest.main()
