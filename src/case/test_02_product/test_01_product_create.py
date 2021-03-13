import logging
import os
import random

import pytest

from src.api import category, product, base, supplier
from src.common.json_util import OperationJson
from src.config.readConfig import ReadConfig

file_name = os.path.join(os.getcwd(), 'resources/product/product_create.json')

logger = logging.getLogger(__name__)
load_config = ReadConfig()


class TestProductCreate(object):
    """
    商品创建 suite
    """

    @classmethod
    def setup(cls) -> None:
        cls.config = ReadConfig()
        cls.json = OperationJson(file_name)
        cls.store_id = load_config.get_value('BASE', 'base_store_id')

        logger.info("------------------测试开始-----------------")

    @classmethod
    def teardown(cls) -> None:
        logger.info("------------------测试结束-----------------")

    def test_01_create_product_without_inventory(self) -> None:
        """
        创建自建商品,没有库存
        """
        logger.info("test_01_create_product_without_inventory")
        # 组织数据
        product_data = self.json.get_data('create_product_without_inventory')
        product_data['categoryId'] = category.choice_random_second_category()['id']
        product_data['name'] = product_data['name'] + str(random.randint(0, 1000))
        product_data['unit'] = base.random_unit()
        product_data['salePrice'] = base.random_price()

        # 调用接口
        resp = product.product_create(self.store_id, product_data)

        # 验证
        assert resp['code'] == 200, resp['message']
        # TODO 验证商品其他信息，例如库存。 通过查询数据库的方式验证数字是否正确

    def test_01_create_product_with_inventory(self) -> None:
        """
        创建自建商品
        带有库存
        """

        logger.info("test_01_create_product_with_inventory")
        # 组织数据
        product_data = self.json.get_data('create_product_with_inventory')
        product_data['categoryId'] = category.choice_random_second_category()['id']
        product_data['name'] = product_data['name'] + str(random.randint(0, 1000))
        product_data['unit'] = base.random_unit()
        product_data['salePrice'] = base.random_price()
        product_data['purchasePrice'] = base.random_price()
        product_data['inventoryQuantity'] = base.random_number()  # 库存数量
        product_data['supplierId'] = supplier.random_supplier(self.store_id)['supplierId']

        # 调用接口
        resp = product.product_create(self.store_id, product_data)

        # 验证
        assert resp['code'] == 200, resp['message']
        # TODO 验证商品其他信息，例如库存。 通过查询数据库的方式验证数字是否正确


if __name__ == "__main__":
    pytest.main()
