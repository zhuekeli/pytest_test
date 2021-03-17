import json

import requests

from src.common import http
from src.config.application_config import ApplicationConfig

config = ApplicationConfig()


def clear_all_cache() -> None:
    """清除所有的缓存记录
    """
    url = '{}/clear/system-cache'.format(config.get_value('API', 'store_url'))
    http.delete(url)


def switch_store(store_id, customer_id, token) -> object:
    """用户登录指定店铺
     登录店铺
    """

    url = f'{config.get_value("API", "store_url")}/store-switch'

    data = {
        "referrer": 0,
        "sources": 0,
        "storeId": store_id
    }
    headers = {
        "Authorization": token,
        "x-store-id": store_id,
        "x-user-id": str(customer_id)
    }
    req = requests.post(url, json=data, headers=headers)
    return json.loads(req.text)
