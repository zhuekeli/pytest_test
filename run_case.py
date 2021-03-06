#!/usr/bin/python3
# coding=utf-8
import logging
import os

import pytest

from src.common.send_email import SendEmail

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    if not os.path.exists('logs'):
        os.mkdir('logs')
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename='logs/skoyi_store.log',
                        filemode='w')
    pytest.main(['-s', '-q', '--alluredir', './report', '--clean-alluredir'])
    SendEmail().send_email()

    os.system('allure serve -p 9091 report')
