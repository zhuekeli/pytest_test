#!/usr/bin/env/ python3
# -*- coding:utf-8 -*-
"""
用于数据驱动测试
从 excel 中读取数据，自动执行测试
"""
from src.common.base_requests import BaseRequest
from src.common.data_process import DataProcess


def test_main(cases):  # 不使用数据库功能
    # 发送请求
    response, expect, sql = BaseRequest.send_request(cases)
    # 断言操作
    DataProcess.assert_result(response, expect)
