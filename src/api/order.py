# -*- coding: utf-8 -*-
from src.common import http
from src.config.application_config import ApplicationConfig

load_config = ApplicationConfig()


def created_order(store_id, data):
    """
    创建订单
    :param store_id:
    :param data:
    :return:
    """
    url = "{0}/store/{1}/order".format(load_config.get_value('API', "store_url"), store_id)

    return http.post(url, data)


def get_order_list(store_id, keyword):
    """
    查询订单列表
    :param store_id:
    :param keyword:
    :return:
    """
    url = "{0}/store/{1}/orders?keyword={2}".format(load_config.get_value('API', "store_url"), store_id, keyword)
    return http.get(url)['data']['content']


def update_order(store_id, order_id, data):
    """
    修改订单
    :param store_id:
    :param order_id:
    :param data:
    :return:
    """
    url = "{0}/store/{1}/order/{2}".format(load_config.get_value('API', "store_url"), store_id, order_id, data)
    return http.put(url, data)


def update_order_status(store_id, order_id, data):
    """
    修改订单状态
    :param store_id:
    :param order_id:
    :param data:
    :return:
    """
    url = "{0}/store/{1}/order/{2}/status".format(load_config.get_value('API', "store_url"), store_id, order_id, data)
    return http.put(url, data)


def update_order_amount(store_id, order_id, data):
    """
    整单改价
    :param store_id:
    :param order_id:
    :param data:
    :return:
    """
    url = "{0}/store/{1}/order/{2}/amount".format(load_config.get_value('API', "store_url"), store_id, order_id, data)
    return http.put(url, data)
