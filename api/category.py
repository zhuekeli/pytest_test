from common import http, global_variable
from config.readConfig import ReadConfig

load_config = ReadConfig()


def choiceSecondCategory():
    url = '{0}/second/categories'.format(load_config.get_value('API', 'base_url'))
    response = http.get(url, param=None)
    print(response)


if __name__ == '__main__':
    global_variable._init()

    choiceSecondCategory()
