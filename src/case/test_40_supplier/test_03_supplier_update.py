import logging
import os
import random

import allure
import pytest

from src.api import supplier, base
from src.common import global_variable
from src.common.json_util import OperationJson
from src.config.application_config import ApplicationConfig
from src.db.supplier_repository import SupplierRepository

logger = logging.getLogger(__name__)

cur_path = os.path.split(os.path.realpath(__file__))[0]
file_name = os.path.join(cur_path, "../../../resources/supplier/supplier_update.json")

operation_json = OperationJson(file_name)
store_id = global_variable.get_store_id()
config = ApplicationConfig()


def get_update_store_supplier_data():
    """获取要编辑的供应商数据"""
    supplier_data = operation_json.get_data('update_supplier')
    supplier_data['name'] = supplier_data['name'] + str(random.randint(0, 1000))
    supplier_data['type'] = random.randint(0, 5)
    supplier_data['contact'] = supplier_data['contact'] + str(random.randint(0, 1000))
    supplier_data['phone'] = base.random_phone()
    supplier_data['address'] = supplier_data['address'] + str(random.randint(0, 1000))
    return [supplier_data]


@allure.parent_suite('供应商测试')
@allure.suite('供应商编辑测试')
class TestSupplierUpdate(object):
    """
    供应商编辑 suite
    """

    @classmethod
    def setup(cls) -> None:
        cls.supplier_repository = SupplierRepository()
        cls.store_id = global_variable.get_store_id()
        logger.info("------------------测试开始-----------------")

    @classmethod
    def teardown(cls) -> None:
        logger.info("------------------测试结束-----------------")

    @allure.title('编辑供应商')
    @pytest.mark.parametrize('supplier_data', get_update_store_supplier_data())
    def test_01_update_store_supplier(self, supplier_data) -> None:
        """编辑供应商基本信息"""
        logger.info("test_01_update_store_supplier")
        # 随机选一个供应商
        random_supplier = supplier.random_supplier(self.store_id)
        if len(random_supplier) > 0:
            # 数据准备
            supplier_id = random_supplier['supplierId']
            print(self.supplier_repository.get_supplier_info(supplier_id))
            logger.info(f'正在编辑store_id:{store_id},supplier_id:{supplier_id}的供应商')
            supplier_name = supplier_data['name']
            supplier_type = supplier_data['type']
            supplier_contact = supplier_data['contact']
            supplier_phone = supplier_data['phone']
            supplier_address = supplier_data['address']
            # 调用接口
            resp = supplier.update_supplier(self.store_id, supplier_id, supplier_data)
            # 验证是否成功
            assert resp['code'] == 200, resp['message']
            # 验证数据
            supplier_from_db = self.supplier_repository.get_supplier_info(supplier_id)
            assert supplier_name == supplier_from_db['name']
            assert supplier_type == supplier_from_db['type']
            assert supplier_contact == supplier_from_db['contact']
            assert supplier_phone == supplier_from_db['phone']
            assert supplier_address == supplier_from_db['address']


if __name__ == "__main__":
    pytest.main()
