#!/usr/bin/python3
# coding=utf-8
import logging
import os

import pytest

from src.common import global_variable
from src.common.send_email import SendEmail

proDir = os.path.split(os.path.realpath(__file__))[0]
test_case_path = os.path.join(proDir, "src/case")
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    if not os.path.exists('logs'):
        os.mkdir('logs')
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename='logs/skoyi_store.log',
                        filemode='w')
    global_variable.init()
    pytest.main(['-s', '-q', '--alluredir', './report', '--clean-alluredir', 'src'])
    SendEmail().send_email()

    os.system('allure serve -p 9091 report')
