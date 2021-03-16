#!/usr/bin/env/python3
# -*- coding:utf-8 -*-
"""
"""
import logging

import allure
import requests

from src.common import allure_title, allure_step
from src.common.data_process import DataProcess

logger = logging.getLogger(__name__)


class BaseRequest(object):
    session = None

    @classmethod
    def get_session(cls):
        if cls.session is None:
            cls.session = requests.Session()
        return cls.session

    @classmethod
    def send_request(cls, case: dict):
        """处理case数据，转换成可用数据发送请求
        :param case: 读取出来的每一行用例内容，可进行解包
        return: 响应结果， 预期结果
        """
        cls._rep_expr_case_data(case)

        logger.info(
            f"用例进行处理前数据: \n "
            f"接口路径: {case['path']} \n "
            f"请求参数: {case['request_data']}  \n "
            f"预期结果: {case['expect']}")
        # allure报告 用例标题
        allure_title(case['code'])
        allure.dynamic.description(case['title'])
        # 处理url、header、data、file、的前置方法
        url = DataProcess.handle_path(case['path'])
        allure_step('请求地址', url)
        data = DataProcess.handle_data(case['request_data'])
        allure_step('请求参数', data)
        # 发送请求
        res = cls.send_api(url, case['method'], case['request_type'], None, data)
        allure_step('响应耗时(s)', res.elapsed.total_seconds())
        allure_step('响应内容', res.json())
        # 响应后操作
        DataProcess.save_response(case['code'], res.json())
        return res.json(), case['expect'], None

    @classmethod
    def send_api(cls, url, method, request_type, header=None, data=None, file=None) -> object:
        """
        :param method: 请求方法
        :param url: 请求url
        :param request_type: 入参关键字， params(查询参数类型，明文传输，一般在url?参数名=参数值), data(一般用于form表单类型参数)
        json(一般用于json类型请求参数)
        :param data: 参数数据，默认等于None
        :param file: 文件对象
        :param header: 请求头
        :return: 返回res对象
        """
        session = cls.get_session()

        if request_type == 'params':
            res = session.request(method=method, url=url, params=data, headers=header)
        elif request_type == 'data':
            res = session.request(method=method, url=url, data=data, files=file, headers=header)
        elif request_type == 'json':
            res = session.request(method=method, url=url, json=data, files=file, headers=header)
        else:
            raise ValueError('可选关键字为params, json, data')
        logger.info(f'\n最终请求地址:{res.url}\n请求方法:{method}\n请求头:{header}\n请求参数:{data}\n上传文件:{file}\n响应数据:{res.json()}')
        return res

    @staticmethod
    def _rep_expr_case_data(case_dict: dict):
        """对输入的 case 数据进行预处理"""
        for key in case_dict:
            case_dict[key] = DataProcess.exp_data(case_dict[key])
