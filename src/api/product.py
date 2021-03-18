import random

from src.common import http
from src.config.application_config import ApplicationConfig

load_config = ApplicationConfig()


def product_create(store_id, data):
    url = '{0}/store/{1}/product'.format(load_config.get_value('API', 'store_url'), store_id)
    return http.post(url, data)


def update_store_product(store_id, prod_code, data):
    """
    更新店铺自建商品
    :param store_id: 店铺ID
    :param prod_code: 商品编码
    :param data:
    :return:
    """
    url = '{0}/store/{1}/product/{2}'.format(load_config.get_value('API', 'store_url'), store_id, prod_code)
    return http.put(url, data)


def update_ruigu_product(store_id, prod_code, data):
    # /store/{storeId}/ruigu/product/{prodCode}

    url = '{0}/store/{1}/product/ruigu/{2}'.format(load_config.get_value('API', 'store_url'), store_id, prod_code)
    return http.put(url, data)


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


def get_random_store_product_from_store(store_id):
    """
    TODO
    通过接口查询店铺中的商品列表，随机选择一个自建商品
    :return:
    """
    url = '{0}/store/{1}/search-product?source=1&page=0&size=200'.format(load_config.get_value('API', 'store_url'),
                                                                         store_id)
    product_list = http.get(url)['data']['products']['content']
    # 随机返回店铺中的任意一个商品
    return product_list[random.randint(0, len(product_list) - 1)] if len(product_list) > 0 else []


def get_random_ruigu_product_from_store(store_id):
    """
    TODO
    通过接口查询店铺中的商品列表，随机选择一个锐锢商品
    :return:
    """
    url = '{0}/store/{1}/search-product?source=2&page=0&size=200'.format(load_config.get_value('API', 'store_url'),
                                                                         store_id)
    product_list = http.get(url)['data']['products']['content']
    # 随机返回店铺中的任意一个商品
    return product_list[random.randint(0, len(product_list) - 1)] if len(product_list) > 0 else []
