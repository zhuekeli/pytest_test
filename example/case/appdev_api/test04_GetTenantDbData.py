#!/usr/bin/python3
# coding=utf-8
import json
import os
import unittest

from common.httpSet import HttpMethod
from common.logger import Logger
from common.readTestData import ReadTestData
from config.readConfig import ReadConfig
from common.getRunLine import get_run_line

proDir = os.path.split(os.path.realpath(__file__))[0]
file_name = os.path.join(proDir, "../../resources/tenant_db.json")


class TestGetTenantDbData(unittest.TestCase):
    def setUp(self):
        self.data = ReadTestData(file_name)
        self.hea_data = ReadTestData()
        self.http = HttpMethod()
        self.config = ReadConfig()
        self.log = Logger()
        self.sheet = 'app_test_case'
        self.row = list(range(20, 26))
        self.log.info(message="----------测试开始----------", name="test04_GetTenantDbData.py")

    def tearDown(self):
        self.log.info(message="----------测试结束----------", name="test04_GetTenantDbData.py")

    def test01_get_db_data(self):
        """通过name获取Tenant DB信息"""
        self.log.info(message="test01_get_db_data", name="test04_GetTenantDbData.py", line=get_run_line())
        # 设置请求数据
        method = self.data.get_method(self.sheet, self.row[0])
        data = self.data.get_param(self.sheet, self.row[0])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[0]) + data
        headers = self.hea_data.get_header(self.sheet, self.row[0])
        self.log.info(message="第一步: 获取请求数据")
        self.log.info(message="请求方法：%s" % method)
        self.log.info(message="接口地址：%s" % url)

        # 发送请求
        status_code, res_json = self.http.http_method(method=method, url=url, headers=headers)
        dict_json = json.loads(res_json)  # 把json数据转换成字典对象
        self.log.info(message="第二步:发送请求，获取返回数据：")
        self.log.info(message="%s" % res_json)

        # 断言
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        for key in ['_id', 'tenant_name', 'db', 'info', 'active_status', 'status']:
            self.assertIn(key, dict_json, msg=">>>返回数据里面没有该字段：%s" % key)
        self.assertTrue(dict_json["status"], msg='>>>获取DB信息失败，实际返回结果：%s' % dict_json)
        self.assertEqual(dict_json["tenant_name"], data, msg='>>>断言失败，实际返回结果：%s' % dict_json["tenant_name"])
        self.assertEqual(dict_json["db"], "auto_tenant_db", msg='>>>断言失败，实际返回结果：%s' % dict_json["db"])

    def test02_get_db_data(self):
        """通过name获取Tenant DB信息失败：name不存在"""
        self.log.info(message="test02_get_db_data", name="test04_GetTenantDbData.py", line=get_run_line())
        # 设置请求数据
        method = self.data.get_method(self.sheet, self.row[1])
        data = self.data.get_param(self.sheet, self.row[1])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[1]) + data
        headers = self.hea_data.get_header(self.sheet, self.row[1])
        expect = self.data.get_expect_result(self.sheet, self.row[1])
        self.log.info(message="第一步: 获取请求数据")
        self.log.info(message="请求方法：%s" % method)
        self.log.info(message="请求接口：%s" % url)
        self.log.info(message="期望结果：%s" % expect)

        # 发送请求
        status_code, res_json = self.http.http_method(method=method, url=url, headers=headers)
        dict_json = json.loads(res_json)  # 把json数据转换成字典对象
        self.log.info(message="第二步:发送请求，获取返回数据：")
        self.log.info(message="%s" % res_json)
        self.log.info(message="第三步:断言")

        # 断言
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        self.assertFalse(dict_json["status"], msg='>>>断言失败，实际返回结果：%s' % dict_json)
        self.assertEqual(dict_json["err"]["code"], expect["err"]["code"],
                         msg=">>>断言失败，实际返回结果：%s" % dict_json["err"]["code"])
        self.assertEqual(dict_json["err"]["message"], expect["err"]["message"],
                         msg=">>>断言失败，实际返回结果：%s" % dict_json["err"]["message"])

    def test03_get_db_data(self):
        """通过db获取Tenant DB信息"""
        self.log.info(message="test03_get_db_data", name="test04_GetTenantDbData.py", line=get_run_line())
        # 设置请求数据
        method = self.data.get_method(self.sheet, self.row[2])
        data = self.data.get_param(self.sheet, self.row[2])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[2]) + data
        headers = self.hea_data.get_header(self.sheet, self.row[2])
        self.log.info(message="第一步: 获取请求数据")
        self.log.info(message="请求方法：%s" % method)
        self.log.info(message="请求接口：%s" % url)

        # 发送请求
        status_code, res_json = self.http.http_method(method=method, url=url, headers=headers)
        dict_json = json.loads(res_json)  # 把json数据转换成字典对象
        self.log.info(message="第二步:发送请求，获取返回数据：")
        self.log.info(message="%s" % res_json)
        self.log.info(message="第三步:断言")

        # 断言
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        self.assertTrue(dict_json["status"], msg='>>>断言失败，实际返回结果：%s' % dict_json)

    def test04_get_db_data(self):
        """通过db获取Tenant DB信息失败：db不存在"""
        self.log.info(message="test03_get_db_data", name="test04_GetTenantDbData.py", line=get_run_line())
        # 设置请求数据
        method = self.data.get_method(self.sheet, self.row[3])
        data = self.data.get_param(self.sheet, self.row[3])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[3]) + data
        headers = self.hea_data.get_header(self.sheet, self.row[3])
        expect = self.data.get_expect_result(self.sheet, self.row[3])
        self.log.info(message="第一步: 获取请求数据")
        self.log.info(message="请求方法：%s" % method)
        self.log.info(message="请求接口：%s" % url)
        self.log.info(message="期望结果：%s" % expect)

        # 发送请求
        status_code, res_json = self.http.http_method(method=method, url=url, headers=headers)
        dict_json = json.loads(res_json)  # 把json数据转换成字典对象
        self.log.info(message="第二步:发送请求，获取返回数据：")
        self.log.info(message="%s" % res_json)
        self.log.info(message="第三步:断言")

        # 断言
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        self.assertFalse(dict_json["status"], msg='>>>断言失败，实际返回结果：%s' % dict_json)
        self.assertEqual(dict_json["err"]["code"], expect["err"]["code"],
                         msg=">>>断言失败，实际返回结果：%s" % dict_json["err"]["code"])
        self.assertEqual(dict_json["err"]["message"], expect["err"]["message"],
                         msg=">>>断言失败，实际返回结果：%s" % dict_json["err"]["message"])

    def test05_delete_db(self):
        """删除Tenant DB成功"""
        self.log.info(message="test05_delete_db", name="test04_GetTenantDbData.py", line=get_run_line())
        # 设置请求数据
        method = self.data.get_method(self.sheet, self.row[4])
        data = self.data.get_param(self.sheet, self.row[4])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[4]) + data
        headers = self.hea_data.get_header(self.sheet, self.row[4])
        self.log.info(message="第一步: 获取请求数据")
        self.log.info(message="请求方法：%s" % method)
        self.log.info(message="请求接口：%s" % url)

        # 发送请求
        status_code, res_json = self.http.http_method(method=method, url=url, headers=headers)
        dict_json = json.loads(res_json)  # 把json数据转换成字典对象
        self.log.info(message="第二步:发送请求，获取返回数据：")
        self.log.info(message="%s" % res_json)
        self.log.info(message="第三步:断言")

        # 断言
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        self.assertTrue(dict_json["status"], msg='>>>断言失败，实际返回结果：%s' % dict_json)

    def test06_delete_db(self):
        """删除Tenant DB失败：DB不存在"""
        self.log.info(message="test03_get_db_data", name="test04_GetTenantDbData.py", line=get_run_line())
        # 设置请求数据
        method = self.data.get_method(self.sheet, self.row[5])
        data = self.data.get_param(self.sheet, self.row[5])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[5]) + data
        headers = self.hea_data.get_header(self.sheet, self.row[5])
        expect = self.data.get_expect_result(self.sheet, self.row[5])
        self.log.info(message="第一步: 获取请求数据")
        self.log.info(message="请求方法：%s" % method)
        self.log.info(message="请求接口：%s" % url)
        self.log.info(message="期望结果：%s" % expect)

        # 发送请求
        status_code, res_json = self.http.http_method(method=method, url=url, headers=headers)
        dict_json = json.loads(res_json)  # 把json数据转换成字典对象
        self.log.info(message="第二步:发送请求，获取返回数据：")
        self.log.info(message="%s" % res_json)
        self.log.info(message="第三步:断言")

        # 断言
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        self.assertFalse(dict_json["status"], msg='>>>断言失败，实际返回结果：%s' % dict_json)
        self.assertEqual(dict_json["err"]["code"], expect["err"]["code"],
                         msg=">>>断言失败，实际返回结果：%s" % dict_json["err"]["code"])
        self.assertEqual(dict_json["err"]["message"], expect["err"]["message"],
                         msg=">>>断言失败，实际返回结果：%s" % dict_json["err"]["message"])


if __name__ == "__main__":
    unittest.main()
