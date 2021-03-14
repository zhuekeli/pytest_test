# -*- coding: utf-8 -*-
from src.common import http, global_variable
from src.config.readConfig import ReadConfig

load_config = ReadConfig()


def login(data):
    url = "{0}/login".format(load_config.get_value('API', "user_url"))
    return http.post(url, data)


def get_store_by_user(user_id):
    url = '{}、employer/{}/stores'.format(load_config.get_value('API', 'user_url'), user_id)
    return http.get(url)


if __name__ == '__main__':
    global_variable.init()
    login({"mobile": "14000000010", "password": "123456"})
