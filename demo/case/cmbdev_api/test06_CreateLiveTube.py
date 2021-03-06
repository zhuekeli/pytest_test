#!/usr/bin/python3
# coding=utf-8
import os
import unittest
import json

from common.httpSet import HttpMethod
from common.logger import Logger
from common.operationJson import OperationJson
from common.readTestData import ReadTestData
from config.readConfig import ReadConfig
from common.getRunLine import get_run_line

proDir = os.path.split(os.path.realpath(__file__))[0]
file_name = os.path.join(proDir, "../../resources/content_live.json")


class TestCreateLiveTube(unittest.TestCase):
    def setUp(self):
        self.data = ReadTestData(file_name)
        self.hea_data = ReadTestData()
        self.http = HttpMethod()
        self.config = ReadConfig()
        self.log = Logger()
        self.json = OperationJson(file_name)
        self.sheet = 'cmb_test_case'
        self.row = list(range(60, 69))
        self.log.info(message="----------测试开始----------", name="test06_CreateLiveTube.py")

    def tearDown(self):
        self.log.info(message="----------测试结束----------", name="test06_CreateLiveTube.py")

    def test01_live_tube_list(self):
        """获取Live Tube列表：为空"""
        self.log.info(message="test01_live_tube_list", name="test06_CreateLiveTube.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[0])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[0])
        headers = self.hea_data.get_header(self.sheet, self.row[0])
        expect = self.data.get_expect_result(self.sheet, self.row[0])
        self.log.info(message="第一步: 获取请求数据")
        self.log.info(message="请求方法：%s" % method)
        self.log.info(message="接口地址：%s" % url)
        self.log.info(message="期望结果：%s" % expect)

        # 发送请求
        status_code, res_json = self.http.http_method(method=method, url=url, headers=headers)
        dict_json = json.loads(res_json)  # 把json数据转换成字典对象
        self.log.info(message="第二步:发送请求，获取返回数据：")
        self.log.info(message="%s" % res_json)

        # 断言
        self.log.info(message="第三步：断言")
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        self.assertFalse(dict_json["status"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
        self.assertEqual(dict_json["err"]["code"], expect["err"]["code"],
                         msg=">>>断言失败，实际返回结果：%s" % dict_json["err"]["code"])
        self.assertEqual(dict_json["err"]["message"], expect["err"]["message"],
                         msg=">>>断言失败，实际返回结果：%s" % dict_json["err"]["message"])

    def test02_cre_live_tube(self):
        """默认的profile和默认的out_type，创建Live tube"""
        self.log.info(message="test02_cre_live_tube", name="test06_CreateLiveTube.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[1])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[1])
        data = self.data.get_request_data(self.sheet, self.row[1])
        headers = self.hea_data.get_header(self.sheet, self.row[1])
        self.log.info(message="第一步: 获取请求数据")
        self.log.info(message="请求方法：%s" % method)
        self.log.info(message="接口地址：%s" % url)
        self.log.info(message="发送数据：%s" % data)

        # 发送请求
        status_code, res_json = self.http.http_method(method=method, url=url, data=data, headers=headers)
        dict_json = json.loads(res_json)  # 把json数据转换成字典对象
        self.log.info(message="第二步:发送请求，获取返回数据：")
        self.log.info(message="%s" % res_json)

        # 提取live_tube_id
        if dict_json["status"]:
            live_tube_id = dict_json["live_tube_id"]
            self.json.write_data(live_tube_id, "live_tube_id_1")
            self.json.write_data(live_tube_id, "default_live_channel", "live_tube_id")

        # 断言
        self.log.info(message="第三步：断言")
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        self.assertTrue(dict_json["status"], msg=">>>断言失败，实际返回结果：%s" % dict_json)

    def test03_cre_live_tube(self):
        """默认的profile和设定的out_type，创建Live tube"""
        self.log.info(message="test03_cre_live_tube", name="test06_CreateLiveTube.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[2])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[2])
        data = self.data.get_request_data(self.sheet, self.row[2])
        headers = self.hea_data.get_header(self.sheet, self.row[2])
        self.log.info(message="第一步: 获取请求数据")
        self.log.info(message="请求方法：%s" % method)
        self.log.info(message="接口地址：%s" % url)
        self.log.info(message="发送数据：%s" % data)

        # 发送请求
        status_code, res_json = self.http.http_method(method=method, url=url, data=data, headers=headers)
        dict_json = json.loads(res_json)  # 把json数据转换成字典对象
        self.log.info(message="第二步:发送请求，获取返回数据：")
        self.log.info(message="%s" % res_json)

        # 提取live_tube_id
        if dict_json["status"]:
            live_tube_id = dict_json["live_tube_id"]
            self.json.write_data(live_tube_id, "set_live_channel", "live_tube_id")

        # 断言
        self.log.info(message="第三步：断言")
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        self.assertTrue(dict_json["status"], msg=">>>断言失败，实际返回结果：%s" % dict_json)

    def test04_live_tube_list(self):
        """获取所有Live Tube列表"""
        self.log.info(message="test04_live_tube_list", name="test06_CreateLiveTube.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[3])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[3])
        headers = self.hea_data.get_header(self.sheet, self.row[3])
        self.log.info(message="第一步: 获取请求数据")
        self.log.info(message="请求方法：%s" % method)
        self.log.info(message="接口地址：%s" % url)

        # 发送请求
        status_code, res_json = self.http.http_method(method=method, url=url, headers=headers)
        dict_json = json.loads(res_json)  # 把json数据转换成字典对象
        self.log.info(message="第二步:发送请求，获取返回数据：")
        self.log.info(message="%s" % res_json)

        # 断言
        self.log.info(message="第三步：断言")
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        self.assertTrue(dict_json["status"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
        self.assertFalse(dict_json["hasPrevious"])
        self.assertFalse(dict_json["hasNext"])
        self.assertEqual(dict_json["total_count"], 2)
        self.assertEqual(len(dict_json["results"]), dict_json["total_count"])

    def test05_live_tube_list(self):
        """获取Live Tube列表：设置返回数量为1"""
        self.log.info(message="test05_live_tube_list", name="test06_CreateLiveTube.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[4])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[4])
        data = self.data.get_param(self.sheet, self.row[4])
        headers = self.hea_data.get_header(self.sheet, self.row[4])
        self.log.info(message="第一步: 获取请求数据")
        self.log.info(message="请求方法：%s" % method)
        self.log.info(message="接口地址：%s" % url)
        self.log.info(message="请求参数：%s" % data)

        # 发送请求
        status_code, res_json = self.http.http_method(method=method, url=url, data=data, headers=headers)
        dict_json = json.loads(res_json)  # 把json数据转换成字典对象
        self.log.info(message="第二步:发送请求，获取返回数据：")
        self.log.info(message="%s" % res_json)

        # 提取next_id
        if dict_json["status"]:
            next_id = dict_json["next"]
            self.json.write_data(next_id, "next_id", "next")

        # 断言
        self.log.info(message="第三步：断言")
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        self.assertTrue(dict_json["status"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
        self.assertFalse(dict_json["hasPrevious"])
        self.assertTrue(dict_json["hasNext"])
        self.assertEqual(dict_json["total_count"], 2)
        self.assertNotEqual(len(dict_json["results"]), dict_json["total_count"])

    def test06_live_tube_list(self):
        """获取Live Tube列表：返回下一页"""
        self.log.info(message="test05_live_tube_list", name="test06_CreateLiveTube.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[5])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[5])
        data = self.data.get_param(self.sheet, self.row[5])
        headers = self.hea_data.get_header(self.sheet, self.row[5])
        self.log.info(message="第一步: 获取请求数据")
        self.log.info(message="请求方法：%s" % method)
        self.log.info(message="接口地址：%s" % url)
        self.log.info(message="请求参数：%s" % data)

        # 发送请求
        status_code, res_json = self.http.http_method(method=method, url=url, data=data, headers=headers)
        dict_json = json.loads(res_json)  # 把json数据转换成字典对象
        self.log.info(message="第二步:发送请求，获取返回数据：")
        self.log.info(message="%s" % res_json)

        # 提取previous_id
        if dict_json["status"]:
            previous_id = dict_json["previous"]
            self.json.write_data(previous_id, "previous_id", "previous")

        # 断言
        self.log.info(message="第三步：断言")
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        self.assertTrue(dict_json["status"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
        self.assertTrue(dict_json["hasPrevious"])
        self.assertFalse(dict_json["hasNext"])
        self.assertEqual(dict_json["total_count"], 2)
        self.assertNotEqual(len(dict_json["results"]), dict_json["total_count"])

    def test07_live_tube_list(self):
        """获取Live Tube列表：返回上一页"""
        self.log.info(message="test05_live_tube_list", name="test06_CreateLiveTube.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[6])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[6])
        data = self.data.get_param(self.sheet, self.row[6])
        headers = self.hea_data.get_header(self.sheet, self.row[6])
        self.log.info(message="第一步: 获取请求数据")
        self.log.info(message="请求方法：%s" % method)
        self.log.info(message="接口地址：%s" % url)
        self.log.info(message="请求参数：%s" % data)

        # 发送请求
        status_code, res_json = self.http.http_method(method=method, url=url, data=data, headers=headers)
        dict_json = json.loads(res_json)  # 把json数据转换成字典对象
        self.log.info(message="第二步:发送请求，获取返回数据：")
        self.log.info(message="%s" % res_json)

        # 断言
        self.log.info(message="第三步：断言")
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        self.assertTrue(dict_json["status"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
        self.assertFalse(dict_json["hasPrevious"])
        self.assertTrue(dict_json["hasNext"])
        self.assertEqual(dict_json["total_count"], 2)
        self.assertNotEqual(len(dict_json["results"]), dict_json["total_count"])

    def test08_live_tube_info(self):
        """获取Live Tube详情"""
        self.log.info(message="test08_live_tube_info", name="test06_CreateLiveTube.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[7])
        data = self.data.get_param(self.sheet, self.row[7])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[7]) + data
        headers = self.hea_data.get_header(self.sheet, self.row[7])
        self.log.info(message="第一步: 获取请求数据")
        self.log.info(message="请求方法：%s" % method)
        self.log.info(message="接口地址：%s" % url)

        # 发送请求
        status_code, res_json = self.http.http_method(method=method, url=url, headers=headers)
        dict_json = json.loads(res_json)  # 把json数据转换成字典对象
        self.log.info(message="第二步:发送请求，获取返回数据：")
        self.log.info(message="%s" % res_json)

        # 断言
        self.log.info(message="第三步：断言")
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        self.assertTrue(dict_json["status"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
        for key in ["_id", "source_type", "profile", "created_time", "owner", "channel_profile", "port", "autorestart",
                    "is_default", "enableAdInsert", "channel_archiving", "out_type", "status"]:
            self.assertIn(key, dict_json, msg="%s字段不在返回数据里" % key)

    def test09_live_tube_info(self):
        """获取Live Tube详情：不存在"""
        self.log.info(message="test09_live_tube_info", name="test06_CreateLiveTube.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[8])
        data = self.data.get_param(self.sheet, self.row[8])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[8]) + data
        headers = self.hea_data.get_header(self.sheet, self.row[8])
        expect = self.data.get_expect_result(self.sheet, self.row[8])
        self.log.info(message="第一步: 获取请求数据")
        self.log.info(message="请求方法：%s" % method)
        self.log.info(message="接口地址：%s" % url)
        self.log.info(message="期望结果：%s" % expect)

        # 发送请求
        status_code, res_json = self.http.http_method(method=method, url=url, headers=headers)
        dict_json = json.loads(res_json)  # 把json数据转换成字典对象
        self.log.info(message="第二步:发送请求，获取返回数据：")
        self.log.info(message="%s" % res_json)

        # 断言
        self.log.info(message="第三步：断言")
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        self.assertFalse(dict_json["status"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
        self.assertEqual(dict_json["err"]["code"], expect["err"]["code"],
                         msg=">>>断言失败，实际返回结果：%s" % dict_json["err"]["code"])
        self.assertEqual(dict_json["err"]["message"], expect["err"]["message"],
                         msg=">>>断言失败，实际返回结果：%s" % dict_json["err"]["message"])


if __name__ == "__main__":
    unittest.main()
