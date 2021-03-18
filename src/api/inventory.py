import random

from src.common import http
from src.config.application_config import ApplicationConfig

load_config = ApplicationConfig()


def get_product_inventory_info(store_id, prod_code):
    """
    查询商品 库存信息
    :return:
    """
    url = "{0}/store/{1}/inventory/product-info?proCode={2}".format(load_config.get_value('API', 'store_url'), store_id,
                                                                    prod_code)
    return http.get(url, prod_code)
