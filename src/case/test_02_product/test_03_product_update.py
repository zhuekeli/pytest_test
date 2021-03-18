import logging
import os
import random

import allure
import pytest

from src.api import category, product, base
from src.common import global_variable
from src.common.json_util import OperationJson
from src.config.application_config import ApplicationConfig
from src.db.product_repository import ProductRepository

logger = logging.getLogger(__name__)

cur_path = os.path.split(os.path.realpath(__file__))[0]
file_name = os.path.join(cur_path, "../../../resources/product/product_update.json")

operation_json = OperationJson(file_name)
store_id = global_variable.get_store_id()
config = ApplicationConfig()


def get_update_store_product_data():
    """获取有库存的商品创建数据"""
    product_data = operation_json.get_data('update_store_product')
    product_data['categoryId'] = category.choice_random_second_category()['id']
    product_data['name'] = product_data['name'] + str(random.randint(0, 1000))
    product_data['unit'] = base.random_unit()
    product_data['salePrice'] = base.random_price()
    return [product_data]


def get_update_ruigu_product_data():
    """获取无库存的商品创建数据"""
    product_data = operation_json.get_data('update_ruigu_product')
    product_data['displayName'] = product_data['displayName'] + str(random.randint(0, 1000))
    product_data['salePrice'] = base.random_price()
    return [product_data]


@allure.parent_suite('商品测试')
@allure.suite('商品编辑测试')
class TestProductUpdate(object):
    """
    商品编辑 suite
    """

    @classmethod
    def setup(cls) -> None:
        cls.product_repository = ProductRepository()
        cls.store_id = global_variable.get_store_id()
        logger.info("------------------测试开始-----------------")

    @classmethod
    def teardown(cls) -> None:
        logger.info("------------------测试结束-----------------")

    @allure.title('编辑自建商品')
    @pytest.mark.parametrize('product_data', get_update_store_product_data())
    def test_01_update_store_product(self, product_data) -> None:
        """
        编辑自建商品
        """
        logger.info("test_01_update_store_product")
        # 随机从店铺搞一个自建商品
        random_product = product.get_random_store_product_from_store(self.store_id)
        if len(random_product) > 0:
            prod_code = random_product['prodCode']
            # 分类ID
            category_id = product_data['categoryId']
            # 调用接口
            resp = product.update_store_product(self.store_id, prod_code, product_data)
            # 验证
            assert resp['code'] == 200, resp['message']
            # 从db查询出该商品看看是否修改成功了
            product_from_db = self.product_repository.get_store_product(store_id, prod_code)
            assert category_id == product_from_db['category_id'], '店铺自建商品分类修改失败'

            # 验证店铺分类是否已经存在了
            store_category_list = self.product_repository.get_store_category(self.store_id)
            assert category_id in store_category_list, '店铺未关联上分类'

    @allure.title('编辑锐锢商品')
    @pytest.mark.parametrize('product_data', get_update_ruigu_product_data())
    def test_02_update_ruigu_product(self, product_data) -> None:
        """
        编辑锐锢商品
        """

        logger.info("test_02_update_ruigu_product")
        # 组织数据

        random_product = product.get_random_ruigu_product_from_store(self.store_id)
        if len(random_product) > 0:
            prod_code = random_product['prodCode']

            display_name = product_data['displayName']

            # 调用接口
            resp = product.update_ruigu_product(self.store_id, prod_code, product_data)
            # 接口返回的商品编码
            prod_code = resp['data']
            # 验证
            assert resp['code'] == 200, resp['message']
            # 验证库存
            product_from_db = self.product_repository.get_store_product(self.store_id, prod_code)
            assert display_name == product_from_db['display_name'], '锐锢商品显示名称修改失败'


if __name__ == "__main__":
    pytest.main()
