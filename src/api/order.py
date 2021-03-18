# -*- coding: utf-8 -*-
from src.common import http
from src.config.application_config import ApplicationConfig

load_config = ApplicationConfig()


def created_order(store_id, data):
    url = "{0}/store/{1}/order".format(load_config.get_value('API', "store_url"), store_id)

    return http.post(url, data)


def get_order_list(store_id, keyword):
    url = "{0}/store/{1}/orders?keyword={2}".format(load_config.get_value('API', "store_url"), store_id, keyword)
    return http.get(url)['data']['content']
