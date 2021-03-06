from common import http
from config.readConfig import ReadConfig

load_config = ReadConfig()


def product_create(store_id, data):
    url = '{0}/store/{1}/product'.format(load_config.get_value('API', 'store_url'), store_id)
    return http.post(url, data)
