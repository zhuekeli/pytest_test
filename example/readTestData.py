#!/usr/bin/python3
# coding=utf-8
from common.operationExcelSheet import OperationExcel
from common.operationJson import OperationJson
from config.readConfig import ReadConfig

false = False
true = True


class ReadTestData:
    def __init__(self, file_name=None):
        self.open_excel = OperationExcel()
        self.set_excel = ReadConfig()
        if file_name:
            self.open_json = OperationJson(file_name)
        else:
            self.open_json = OperationJson()

    def get_module(self, sheet_name, row):
        cell = self.set_excel.get_excel('module')
        module = self.open_excel.from_ab_get_data(sheet_name, cell, row)
        return module

    def get_api_name(self, sheet_name, row):
        cell = self.set_excel.get_excel('api_name')
        case_id = self.open_excel.from_ab_get_data(sheet_name, cell, row)
        return case_id

    def get_case_id(self, sheet_name, row):
        cell = self.set_excel.get_excel('case_id')
        case_id = self.open_excel.from_ab_get_data(sheet_name, cell, row)
        return case_id

    def get_case_name(self, sheet_name, row):
        cell = self.set_excel.get_excel('case_name')
        case_title = self.open_excel.from_ab_get_data(sheet_name, cell, row)
        return case_title

    def get_url(self, sheet_name, row):
        cell = self.set_excel.get_excel('url')
        url = self.open_excel.from_ab_get_data(sheet_name, cell, row)
        return url

    def get_premise(self, sheet_name, row):
        cell = self.set_excel.get_excel('premise')
        premise = self.open_excel.from_ab_get_data(sheet_name, cell, row)
        return premise

    def get_header(self, sheet_name, row):
        cell = self.set_excel.get_excel('header')
        headers_key = self.open_excel.from_ab_get_data(sheet_name, cell, row)
        headers = self.open_json.key_get_data(headers_key)
        return headers

    def get_method(self, sheet_name, row):
        cell = self.set_excel.get_excel('method')
        method = self.open_excel.from_ab_get_data(sheet_name, cell, row)
        return method

    def get_request_data(self, sheet_name, row):
        cell = self.set_excel.get_excel('data')
        request_key = self.open_excel.from_ab_get_data(sheet_name, cell, row)
        request_data = self.open_json.key_get_data(request_key)
        return request_data

    def get_param(self, sheet_name, row):
        cell = self.set_excel.get_excel('param')
        param = self.open_excel.from_ab_get_data(sheet_name, cell, row)
        request_param = self.open_json.key_get_data(param)
        return request_param

    def get_check(self, sheet_name, row):
        cell = self.set_excel.get_excel('check')
        check = self.open_excel.from_ab_get_data(sheet_name, cell, row)
        return check

    def get_expect_result(self, sheet_name, row):
        cell = self.set_excel.get_excel('expected')
        expect_result = self.open_excel.from_ab_get_data(sheet_name, cell, row)
        expect_result_dict = eval(expect_result)
        return expect_result_dict

    def get_return_data(self, sheet_name, row):
        cell = self.set_excel.get_excel('return')
        return_data = self.open_excel.from_ab_get_data(sheet_name, cell, row)
        return return_data

    def get_rely_data(self, sheet_name, row):
        cell = self.set_excel.get_excel('rely')
        data = self.open_excel.from_ab_get_data(sheet_name, cell, row)
        rely_data = self.open_json.key_get_data(data)
        return rely_data


if __name__ == "__main__":
    file_name = "../resources/content_vod.json"
    a = ReadTestData(file_name)
    b = a.get_param('cmb_test_case', 48)
    print(type(b))
    print(b)
