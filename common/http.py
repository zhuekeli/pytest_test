import json

import requests

from common import global_variable
from config.readConfig import ReadConfig

load_config = ReadConfig()


def get(url, param):
    token = global_variable.get_value("token")
    if token is None:
        token = load_config.get_token("token")

    req = requests.get(url, params=param, headers={"Authorization": token})
    return json.loads(req.text)


def post(url, body):
    token = global_variable.get_value("token")
    if token is None:
        token = load_config.get_token('token')

    req = requests.post(url, json=body, headers={"Authorization": token})
    return json.loads(req.text)
