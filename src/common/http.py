import json

import requests

from src.common import global_variable
from src.config.application_config import ApplicationConfig

config = ApplicationConfig()


def get(url, param=None):
    headers = get_global_header()

    req = requests.get(url, params=param, headers=headers)
    return json.loads(req.text)


def post(url, body=None):
    headers = get_global_header()

    req = requests.post(url, json=body, headers=headers)
    return json.loads(req.text)


def delete(url, body=None):
    headers = get_global_header()
    req = requests.delete(url, json=body, headers=headers)
    return json.loads(req.text)


def get_global_header():
    headers = {
        "Authorization": global_variable.get_token(),
        "x-store-id": global_variable.get_store_id(),
        "x-user-id": str(global_variable.get_user_id())
    }
    return headers
