#!/usr/bin/python3
# coding=utf-8
import json
import os
import unittest

from common.httpSet import HttpMethod
from common.logger import Logger
from common.readTestData import ReadTestData
from config.readConfig import ReadConfig
from common.operationJson import OperationJson
from common.getRunLine import get_run_line

proDir = os.path.split(os.path.realpath(__file__))[0]
file_name = os.path.join(proDir, "../../resources/tenant_db.json")


class TestCreateDBandGetList(unittest.TestCase):
    def setUp(self):
        self.data = ReadTestData(file_name)
        self.hea_data = ReadTestData()
        self.http = HttpMethod()
        self.config = ReadConfig()
        self.log = Logger()
        self.json = OperationJson(file_name)
        self.sheet = 'app_test_case'
        self.row = list(range(12, 20))
        self.log.info(message="----------测试开始----------", name="test03_CreateDBandGetList.py")

    def tearDown(self):
        self.log.info(message="----------测试结束----------", name="test03_CreateDBandGetList.py")

    def test01_get_db_list(self):
        """获取Tenant DB列表：Tenant DB列表为空"""
        self.log.info(message="test01_get_db_list", name="test03_CreateDBandGetList.py", line=get_run_line())
        # 设置请求数据
        method = self.data.get_method(self.sheet, self.row[0])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[0])
        headers = self.hea_data.get_header(self.sheet, self.row[0])
        expect = self.data.get_expect_result(self.sheet, self.row[0])
        self.log.info(message="第一步: 获取请求数据")
        self.log.info(message="请求方法：%s" % method)
        self.log.info(message="请求接口：%s" % url)
        self.log.info(message="期望结果：%s" % expect)

        # 发送请求
        status_code, res_json = self.http.http_method(method=method, url=url, headers=headers)
        dict_json = json.loads(res_json)  # 把json数据转换成字典对象
        self.log.info(message="第二步:发送请求，获取返回数据：")
        self.log.info(message="%s" % res_json)
        self.log.info(message="第三步：断言")

        # 断言
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        self.assertFalse(dict_json["status"], msg='>>>创建DB失败，实际返回结果：%s' % dict_json)
        self.assertEqual(dict_json["err"]["code"], expect["err"]["code"],
                         msg=">>>断言失败，实际返回结果：%s" % dict_json["err"]["code"])
        self.assertEqual(dict_json["err"]["message"], expect["err"]["message"],
                         msg=">>>断言失败，实际返回结果：%s" % dict_json["err"]["message"])

    def test02_create_db(self):
        """创建Tenant DB，不创建auto live"""
        self.log.info(message="test02_create_db", name="test03_CreateDBandGetList.py", line=get_run_line())
        # 设置请求数据
        method = self.data.get_method(self.sheet, self.row[1])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[1])
        data = self.data.get_request_data(self.sheet, self.row[1])
        headers = self.hea_data.get_header(self.sheet, self.row[1])
        self.log.info(message="第一步: 获取请求数据")
        self.log.info(message="请求方法：%s" % method)
        self.log.info(message="请求接口：%s" % url)
        self.log.info(message="请求数据：%s" % data)

        # 发送请求
        status_code, res_json = self.http.http_method(method=method, url=url, data=data, headers=headers)
        dict_json = json.loads(res_json)  # 把json数据转换成字典对象
        self.log.info(message="第二步:发送请求，获取返回数据：")
        self.log.info(message="%s" % res_json)
        if dict_json["status"]:
            db_id = dict_json["tenant_db_id"]  # 提取tenant_db_id
            self.log.info(message="提取tenant_db_id：%s" % db_id)
            self.json.write_data(db_id, "db_id")  # 把tenant_db_id写入json文件
            self.log.info(message="并把tenant_db_id写入json文件")

        # 断言
        self.log.info(message="第三步：断言")
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        self.assertTrue(dict_json["status"], msg='>>>创建DB失败，实际返回结果：%s' % dict_json)

    def test03_create_db(self):
        """创建成功，并创建auto live"""
        self.log.info(message="test03_create_db", name="test03_CreateDBandGetList.py", line=get_run_line())
        # 设置请求数据
        method = self.data.get_method(self.sheet, self.row[2])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[2])
        data = self.data.get_request_data(self.sheet, self.row[2])
        headers = self.hea_data.get_header(self.sheet, self.row[2])
        self.log.info(message="第一步: 获取请求数据")
        self.log.info(message="请求方法：%s" % method)
        self.log.info(message="请求接口：%s" % url)
        self.log.info(message="请求数据：%s" % data)

        # 发送请求
        status_code, res_json = self.http.http_method(method=method, url=url, data=data, headers=headers)
        dict_json = json.loads(res_json)  # 把json数据转换成字典对象
        self.log.info(message="第二步:发送请求，获取返回数据：")
        self.log.info(message="%s" % res_json)
        self.log.info(message="第三步：断言")

        # 断言
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        self.assertTrue(dict_json["status"], msg='>>>创建DB失败，实际返回结果：%s' % dict_json)

    def test04_create_db(self):
        """创建失败：缺少tenant name"""
        self.log.info(message="test04_create_db", name="test03_CreateDBandGetList.py", line=get_run_line())
        # 设置请求数据
        method = self.data.get_method(self.sheet, self.row[3])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[3])
        data = self.data.get_request_data(self.sheet, self.row[3])
        headers = self.hea_data.get_header(self.sheet, self.row[3])
        expect = self.data.get_expect_result(self.sheet, self.row[3])
        self.log.info(message="第一步: 获取请求数据")
        self.log.info(message="请求方法：%s" % method)
        self.log.info(message="请求接口：%s" % url)
        self.log.info(message="请求数据：%s" % data)
        self.log.info(message="期望结果：%s" % expect)

        # 发送请求
        status_code, res_json = self.http.http_method(method=method, url=url, data=data, headers=headers)
        dict_json = json.loads(res_json)  # 把json数据转换成字典对象
        self.log.info(message="第二步:发送请求，获取返回数据：")
        self.log.info(message="%s" % res_json)
        self.log.info(message="第三步：断言")

        # 断言
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        self.assertFalse(dict_json["status"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
        self.assertEqual(dict_json["err"]["code"], expect["err"]["code"],
                         msg=">>>断言失败，实际返回结果：%s" % dict_json["err"]["code"])
        self.assertEqual(dict_json["err"]["message"], expect["err"]["message"],
                         msg=">>>断言失败，实际返回结果：%s" % dict_json["err"]["message"])

    def test05_create_db(self):
        """创建失败：缺少db name"""
        self.log.info(message="test05_create_db", name="test03_CreateDBandGetList.py", line=get_run_line())
        # 设置请求数据
        method = self.data.get_method(self.sheet, self.row[4])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[4])
        data = self.data.get_request_data(self.sheet, self.row[4])
        headers = self.hea_data.get_header(self.sheet, self.row[4])
        expect = self.data.get_expect_result(self.sheet, self.row[4])
        self.log.info(message="第一步: 获取请求数据")
        self.log.info(message="请求方法：%s" % method)
        self.log.info(message="请求接口：%s" % url)
        self.log.info(message="请求数据：%s" % data)
        self.log.info(message="期望结果：%s" % expect)

        # 发送请求
        status_code, res_json = self.http.http_method(method=method, url=url, data=data, headers=headers)
        dict_json = json.loads(res_json)  # 把json数据转换成字典对象
        self.log.info(message="第二步:发送请求，获取返回数据：")
        self.log.info(message="%s" % res_json)
        self.log.info(message="第三步：断言")

        # 断言
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        self.assertFalse(dict_json["status"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
        self.assertEqual(dict_json["err"]["code"], expect["err"]["code"],
                         msg=">>>断言失败，实际返回结果：%s" % dict_json["err"]["code"])
        self.assertEqual(dict_json["err"]["message"], expect["err"]["message"],
                         msg=">>>断言失败，实际返回结果：%s" % dict_json["err"]["message"])

    def test06_create_db(self):
        """创建失败：tenant name已被占用"""
        self.log.info(message="test06_create_db", name="test03_CreateDBandGetList.py", line=get_run_line())
        # 设置请求数据
        method = self.data.get_method(self.sheet, self.row[5])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[5])
        data = self.data.get_request_data(self.sheet, self.row[5])
        headers = self.hea_data.get_header(self.sheet, self.row[5])
        expect = self.data.get_expect_result(self.sheet, self.row[5])
        self.log.info(message="第一步: 获取请求数据")
        self.log.info(message="请求方法：%s" % method)
        self.log.info(message="请求接口：%s" % url)
        self.log.info(message="请求数据：%s" % data)
        self.log.info(message="期望结果：%s" % expect)

        # 发送请求
        status_code, res_json = self.http.http_method(method=method, url=url, data=data, headers=headers)
        dict_json = json.loads(res_json)  # 把json数据转换成字典对象
        self.log.info(message="第二步:发送请求，获取返回数据：")
        self.log.info(message="%s" % res_json)
        self.log.info(message="第三步：断言")

        # 断言
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        self.assertFalse(dict_json["status"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
        self.assertEqual(dict_json["err"]["code"], expect["err"]["code"],
                         msg=">>>断言失败，实际返回结果：%s" % dict_json["err"]["code"])
        self.assertEqual(dict_json["err"]["message"], expect["err"]["message"],
                         msg=">>>断言失败，实际返回结果：%s" % dict_json["err"]["message"])

    def test07_create_db(self):
        """创建失败：db name已被占用"""
        self.log.info(message="test07_create_db", name="test03_CreateDBandGetList.py", line=get_run_line())
        # 设置请求数据
        method = self.data.get_method(self.sheet, self.row[6])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[6])
        data = self.data.get_request_data(self.sheet, self.row[6])
        headers = self.hea_data.get_header(self.sheet, self.row[6])
        expect = self.data.get_expect_result(self.sheet, self.row[6])
        self.log.info(message="第一步: 获取请求数据")
        self.log.info(message="请求方法：%s" % method)
        self.log.info(message="请求接口：%s" % url)
        self.log.info(message="请求数据：%s" % data)
        self.log.info(message="期望结果：%s" % expect)

        # 发送请求
        status_code, res_json = self.http.http_method(method=method, url=url, data=data, headers=headers)
        dict_json = json.loads(res_json)  # 把json数据转换成字典对象
        self.log.info(message="第二步:发送请求，获取返回数据：")
        self.log.info(message="%s" % res_json)

        # 断言
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        self.assertFalse(dict_json["status"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
        self.assertEqual(dict_json["err"]["code"], expect["err"]["code"],
                         msg=">>>断言失败，实际返回结果：%s" % dict_json["err"]["code"])
        self.assertEqual(dict_json["err"]["message"], expect["err"]["message"],
                         msg=">>>断言失败，实际返回结果：%s" % dict_json["err"]["message"])

    def test08_get_db_list(self):
        """获取Tenant DB列表"""
        self.log.info(message="test08_get_db_list", name="test03_CreateDBandGetList.py", line=get_run_line())
        # 设置请求数据
        method = self.data.get_method(self.sheet, self.row[7])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[7])
        headers = self.hea_data.get_header(self.sheet, self.row[7])
        self.log.info(message="第一步: 获取请求数据")
        self.log.info(message="请求方法：%s" % method)
        self.log.info(message="请求接口：%s" % url)

        # 发送请求
        status_code, res_json = self.http.http_method(method=method, url=url, headers=headers)
        dict_json = json.loads(res_json)  # 把json数据转换成字典对象
        self.log.info(message="第二步:发送请求，获取返回数据：")
        self.log.info(message="%s" % res_json)
        self.log.info(message="第三步：断言")

        # 断言
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        self.assertTrue(dict_json["status"], msg='创建DB失败，实际返回结果：%s' % dict_json)
        for key in ["_id", 'tenant_name', "db", 'info', 'active_status']:
            self.assertIn(key, dict_json["results"][0], msg="%s字段不存在" % key)
        self.assertEqual(dict_json["results"][0]["tenant_name"], "auto_tenant_name",
                         msg=">>>断言失败，实际返回结果：%s" % dict_json["results"][0]["tenant_name"])
        for key in ["_id", 'tenant_name', "db", 'info', 'active_status']:
            self.assertIn(key, dict_json["results"][1], msg="%s字段不存在" % key)
        self.assertEqual(dict_json["results"][1]["tenant_name"], "auto_live_tenant_name",
                         msg=">>>断言失败，实际返回结果：%s" % dict_json["results"][1]["tenant_name"])


if __name__ == "__main__":
    unittest.main()
