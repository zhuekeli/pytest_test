# -*- coding: utf-8 -*-
from src.common import http, global_variable
from src.config.readConfig import ReadConfig

load_config = ReadConfig()


def login(data):
    url = "{0}/login".format(load_config.get_value('API', "user_url"))
    return http.post(url, data)


if __name__ == '__main__':
    global_variable.init()
    login({"mobile": "14000000010", "password": "123456"})
