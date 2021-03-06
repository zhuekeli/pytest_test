#!/usr/bin/python3
# coding=utf-8
import logging

from src.api import user
from src.common import global_variable
from src.common.operationJson import OperationJson
from src.config.readConfig import ReadConfig

config = ReadConfig()
logger = logging.getLogger(__name__)


class ResetEnv:
    def __init__(self):
        self.op_json = OperationJson()

    def init_data(self) -> None:
        """
        1. 初始化 token
        """
        response = user.login({
            "mobile": config.get_value("BASE", "mobile"),
            "password": config.get_value("BASE", "password")
        })
        global_variable.set_value("token", response['data']['token'])

    def clean_all(self):
        """初始化测试环境"""
        return True


if __name__ == "__main__":
    r = ResetEnv()
