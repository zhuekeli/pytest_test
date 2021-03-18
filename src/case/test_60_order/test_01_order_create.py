import logging
import os

import allure
import pytest
import random

from src.api import order
from src.api.inventory import get_product_inventory_info
from src.api.order import get_order_list
from src.api.product import get_random_inventory_product_from_store
from src.common import global_variable
from src.common.json_util import OperationJson
from src.config.application_config import ApplicationConfig

logger = logging.getLogger(__name__)

cur_path = os.path.split(os.path.realpath(__file__))[0]
file_name = os.path.join(cur_path, "../../../resources/order/order.json")

operation_json = OperationJson(file_name)
store_id = global_variable.get_store_id()
config = ApplicationConfig()


def get_order_info():
    """获取订单数据"""
    order_info = operation_json.get_data('create_order')
    return order_info


@allure.parent_suite('订单测试')
@allure.suite('订单创建测试')
class TestOrderCreate(object):
    """
    订单创建 suite
    """

    @classmethod
    def setup(cls) -> None:
        logger.info("------------------测试开始-----------------")

    @classmethod
    def teardown(cls) -> None:
        logger.info("------------------测试结束-----------------")

    @allure.title('创建订单-商品有库存')
    # @pytest.mark.parametrize('order_info', get_order_info())
    def test_01_create_order_without_inventory(self) -> None:
        """
        创建订单
        有库存商品
        """
        order_info = get_order_info()
        logger.info("test_01_create_product_with_inventory")
        # 组织数据
        # 查询 库存商品
        inventory_product = get_random_inventory_product_from_store(store_id, 0)
        if inventory_product:
            total_paid_amount = 0
            for item in order_info['items']:
                item["prodCode"] = inventory_product["prodCode"]
                item["prodName"] = order_info["items"][0]["prodName"] + inventory_product["displayName"]
                item["price"] = inventory_product["salePrice"]
                item["unit"] = inventory_product["unit"]
                # 查询 商品库存信息
                inventory_info = get_product_inventory_info(store_id, inventory_product["prodCode"])
                item["quantity"] = inventory_info['data']["quantity"] % 10
                total_paid_amount = total_paid_amount + item['quantity'] * item['price']
            order_info['totalPaidAmount'] = total_paid_amount
            order_info['totalAmount'] = total_paid_amount
        else:
            # 查询 无库存商品
            raise TypeError("查询商品失败")

        # 调用接口
        resp = order.created_order(store_id, order_info)
        # 验证
        assert resp['code'] == 200, resp['message']
        # 验证库存
        order_list = get_order_list(store_id, inventory_product["displayName"])
        if order_list:
            assert order_list[0]["orderStatus"] == 2, "订单状态应为已完成"
        else:
            raise TypeError("查询不到订单")

    @allure.title('创建订单-商品无库存')
    # @pytest.mark.parametrize('create_order', get_order_info())
    def test_02_create_product_with_inventory(self) -> None:
        """
        创建订单
        商品库存不足
        """
        order_info = get_order_info()
        logger.info("test_01_create_product_with_inventory")
        # 组织数据
        # 查询 低库存商品
        low_inventory_product = get_random_inventory_product_from_store(store_id, 1)
        if low_inventory_product:
            total_paid_amount = 0
            for item in order_info['items']:
                item["prodCode"] = low_inventory_product["prodCode"]
                item["prodName"] = item["prodName"] + low_inventory_product[
                    "displayName"]
                item["price"] = low_inventory_product["salePrice"]
                item["unit"] = low_inventory_product["unit"]
                # 查询 商品库存信息
                inventory_info = get_product_inventory_info(store_id, low_inventory_product["prodCode"])
                if inventory_info['data']["thresholdQuantity"] != 0:
                    item["quantity"] = inventory_info['data']["thresholdQuantity"]
                else:
                    item["quantity"] = random(10, 20)
                total_paid_amount = total_paid_amount + item['price'] * item['quantity']
            order_info['totalPaidAmount'] = total_paid_amount
        else:
            # 查询 无库存商品
            low_inventory_product = get_random_inventory_product_from_store(store_id, 2)
            if low_inventory_product:
                total_paid_amount = 0
                for item in order_info['items']:
                    item["prodCode"] = low_inventory_product["prodCode"]
                    item["prodName"] = item["prodName"] + low_inventory_product[
                        "displayName"]
                    item["price"] = low_inventory_product["salePrice"]
                    item["unit"] = low_inventory_product["unit"]
                    item["quantity"] = random.randint(1, 5)
                    total_paid_amount = total_paid_amount + item['quantity'] * item['price']
                order_info['totalPaidAmount'] = total_paid_amount
                order_info['totalAmount'] = total_paid_amount
            else:
                raise TypeError("该店铺[" + store_id + "]无低库存或缺货商品")

        # 调用接口
        resp = order.created_order(store_id, order_info)
        # 验证
        assert resp['code'] == 200, resp['message']
        # 验证库存
        order_list = get_order_list(store_id, low_inventory_product["displayName"])
        if order_list:
            assert order_list[0]["orderStatus"] == 4, "订单状态应为发货中"
        else:
            raise TypeError("查询不到订单")


if __name__ == "__main__":
    pytest.main()
