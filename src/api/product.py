from src.common import http
from src.config.readConfig import ReadConfig

load_config = ReadConfig()


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
