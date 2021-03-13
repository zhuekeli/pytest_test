# -*- coding: utf-8 -*-
from src.common import http
from src.config.readConfig import ReadConfig

load_config = ReadConfig()


def created_order(store_id, data):
    url = "{0}/store/{1}/order".format(load_config.get_value('API', "store_url"), store_id)

    return http.post(url, data)
