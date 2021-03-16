#!/usr/bin/env/ python3
# -*- coding:utf-8 -*-
"""
用于数据驱动测试
1. 从 get_case 中读取数据，自动执行测试
"""
import allure

from src.common.base_requests import BaseRequest
from src.common.data_process import DataProcess


@allure.parent_suite("数据驱动测试")
def test_auto(get_case):
    """自动执行脚本驱动测试
    :param get_case
    {
    'name':
    }
    """
    allure.dynamic.suite(get_case['suite_name'])
    response, expect, sql = BaseRequest.send_request(get_case)
    # 断言操作
    DataProcess.assert_result(response, expect)
