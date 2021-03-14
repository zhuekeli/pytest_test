import random

from src.common import http
from src.config.readConfig import ReadConfig

load_config = ReadConfig()


def random_supplier(store_id):
    """
    随机供应商
    :return:
    """
    url = '{}/store/{}/supplier/supplier-brief'.format(load_config.get_value('API', 'store_url'), store_id)

    resp = http.get(url)
    if resp['result']:
        return resp['data'][random.randint(0, len(resp['data']) - 1)]


def create_supplier(store_id, data):
    """
    创建供应商
    :param data: 供应商信息
    :param store_id: 店铺 id
    :return:
    """
    url = '{}/store/{}/supplier'.format(load_config.get_value('API', 'store_url'), store_id)
    return http.post(url, data)


if __name__ == '__main__':
    random_supplier(1)