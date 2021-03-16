import random

from src.common import http, global_variable
from src.config.application_config import ApplicationConfig

load_config = ApplicationConfig()


def choice_random_second_category():
    url = '{0}/second/categories'.format(load_config.get_value('API', 'base_url'))
    resp = http.get(url, param=None)
    index = random.randint(0, len(resp['data']))
    return resp['data'][index]


if __name__ == '__main__':
    global_variable.init()
    cate = choice_random_second_category()
    print(cate)
