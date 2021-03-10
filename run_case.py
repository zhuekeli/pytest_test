#!/usr/bin/python3
# coding=utf-8
import logging
import os

import pytest

from src.common import global_variable

proDir = os.path.split(os.path.realpath(__file__))[0]
test_case_path = os.path.join(proDir, "src/case")
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename='logs/skoyi_store.log',
                        filemode='w')
    global_variable.init()
    pytest.main(['-s', '-q', '--alluredir', './report', '--clean-alluredir', 'src'])
    os.system('allure serve report')
