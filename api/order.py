# -*- coding: utf-8 -*-
from common import http
from config.readConfig import ReadConfig

load_config = ReadConfig()


def created_order(store_id, data):
    url = "{0}/store/{1}/order".format(load_config.get_value('api', "base_url"), store_id)

    response = http.post(url, data)
    print(response)
