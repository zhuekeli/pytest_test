import logging
import os

from src.api import supplier
from src.common import global_variable
from src.common.json_util import OperationJson
from src.config.readConfig import ReadConfig

cur_path = os.path.split(os.path.realpath(__file__))[0]
file_name = os.path.join(cur_path, "../../../resources/supplier/supplier_create.json")

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
        cls.store_id = global_variable.get_store_id()

        logger.info("------------------测试开始-----------------")

    @classmethod
    def teardown(cls) -> None:
        logger.info("------------------测试结束-----------------")

    def test_01_create_supplier(self) -> None:
        """
        创建供应商信息
        """
        logger.info("test_01_create_supplier")
        # 组织数据
        suppliers = self.json.get_data('create_product')

        for s in suppliers:
            resp = supplier.create_supplier(self.store_id, s)
            assert resp['code'] == 200, resp['message']


if __name__ == "__main__":
    TestProductCreate().test_01_create_supplier()
