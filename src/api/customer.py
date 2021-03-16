import json

import requests

from src.config.application_config import ApplicationConfig

load_config = ApplicationConfig()


def login_store(store_id, customer_id):
    """
    登录指定店铺
    :param store_id:  店铺 id
    :param customer_id: 客户 id
    :return:
    """
    # 获取 token
    url = '{}/dev/token?userId={}'.format(load_config.get_value('BASE', 'user_url'), customer_id)
    resp = requests.post(url)
    resp_obj = json.loads(resp.text)

    if resp_obj['result']:
        token = resp_obj['data']['token']
        headers = {
            "Authorization": token,
            "x-store-id": store_id,
            "x-user-id": str(customer_id),
        }
        login_store_url = '{}/store-switch'.format(load_config.get_value('BASE', 'store_url'))
        body = {
            'storeId': store_id,
            'sources': 0
        }
        requests.post(login_store_url, data=body, headers=headers)
