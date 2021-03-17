import random

from src.common import http
from src.config.application_config import ApplicationConfig

load_config = ApplicationConfig()


def product_create(store_id, data):
    url = '{0}/store/{1}/product'.format(load_config.get_value('API', 'store_url'), store_id)
    return http.post(url, data)


def get_random_product_from_ruigu():
    """
    TODO
    随机从rbox_product 库中获取一个商品信息，不包含 SKU
    :return: 商品信息
    """


def get_random_product_from_store(store_id):
    """
    TODO
    通过接口查询店铺中的商品列表，随机选择一个商品添加
    :return:
    """
    url = '{0}/store/{1}/search-product?page=0&size=200'.format(load_config.get_value('API', 'store_url'), store_id)
    product_list = http.get(url)['data']['products']['content']
    # 随机返回店铺中的任意一个商品
    return product_list[random.randint(0, len(product_list) - 1)]
