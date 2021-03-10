import logging

import pytest

from src.api import user
from src.common import global_variable
from src.config.readConfig import ReadConfig

config = ReadConfig()
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def reset():
    """
    1. 初始化 token
    """
    response = user.login({
        "mobile": config.get_value("BASE", "mobile"),
        "password": config.get_value("BASE", "password")
    })
    global_variable.set_value("token", response['data']['token'])
    global_variable.set_value("user_id", response['data']['userId'])
