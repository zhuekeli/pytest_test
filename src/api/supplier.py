import random

from src.common import http
from src.config.application_config import ApplicationConfig

config = ApplicationConfig()


def random_supplier(store_id):
    """
    随机供应商
    :return:
    """
    url = '{}/store/{}/supplier/supplier-brief'.format(config.get_value('API', 'store_url'), store_id)

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
    url = '{}/store/{}/supplier'.format(config.get_value('API', 'store_url'), store_id)
    return http.post(url, data)


def update_supplier(store_id, supplier_id, data):
    """
    编辑供应商
    :param store_id: 店铺id
    :param supplier_id: 供应商id
    :param data: 供应商编辑信息
    :return:
    """
    url = '{}/store/{}/supplier/{}'.format(config.get_value('API', 'store_url'), store_id, supplier_id)
    return http.put(url, data)


if __name__ == '__main__':
    random_supplier(1)
