#!/usr/bin/env/ python3
# -*- coding:utf-8 -*-
"""
用于数据驱动测试
1. 从 excel 中读取数据，自动执行测试
"""
import allure

from src.common.base_requests import BaseRequest
from src.common.data_process import DataProcess


@allure.parent_suite("数据驱动测试")
def test_auto(get_case_from_yaml):
    allure.dynamic.suite(get_case_from_yaml['suite_name'])
    response, expect, sql = BaseRequest.send_request(get_case_from_yaml)
    # 断言操作
    DataProcess.assert_result(response, expect)
