# -*- coding: utf-8 -*-
from common import http, global_variable
from config.readConfig import ReadConfig

load_config = ReadConfig()


def login(data):
    url = "{0}/login".format(load_config.get_value('API', "user_url"))

    response = http.post(url, data)
    print(response)


if __name__ == '__main__':
    global_variable._init()
    login({"mobile": "14000000010", "password": "123456"})
