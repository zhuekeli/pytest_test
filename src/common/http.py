import json

import requests

from src.common import global_variable
from src.config.readConfig import ReadConfig

load_config = ReadConfig()


def get(url, param=None):
    token = global_variable.get_value('token')
    if token is None:
        token = load_config.get_token('token')
    headers = {
        "Authorization": token,
        "x-store-id": load_config.get_token('base_store_id'),
        "x-user-id": str(global_variable.get_value('user_id') or 0)
    }

    req = requests.get(url, params=param, headers=headers)
    return json.loads(req.text)


def post(url, body):
    token = global_variable.get_value("token")
    if token is None:
        token = load_config.get_token('token')
    headers = {
        "Authorization": token,
        "x-store-id": load_config.get_token('base_store_id'),
        "x-user-id": str(global_variable.get_value('user_id') or 0)
    }

    req = requests.post(url, json=body, headers=headers)
    return json.loads(req.text)
