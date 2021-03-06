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
from common.callShellFile import CallShell

proDir = os.path.split(os.path.realpath(__file__))[0]
file_name = os.path.join(proDir, "../../resources/content_live.json")


class TestCreateLiveChannel(unittest.TestCase):
    def setUp(self):
        self.data = ReadTestData(file_name)
        self.hea_data = ReadTestData()
        self.http = HttpMethod()
        self.config = ReadConfig()
        self.log = Logger()
        self.stream = CallShell()
        self.json = OperationJson(file_name)
        self.sheet = 'cmb_test_case'
        self.row = list(range(69, 86))
        self.log.info(message="----------测试开始----------", name="test07_CreateLiveChannel.py")

    def tearDown(self):
        self.log.info(message="----------测试结束----------", name="test07_CreateLiveChannel.py")

    def test01_live_channel_list(self):
        """获取Live Channel列表：为空"""
        self.log.info(message="test01_live_channel_list", name="test06_CreateLiveTube.py", line=get_run_line())
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

    def test02_cre_live_channel(self):
        """默认profile和默认out_type的Live Tube，创建Live channel"""
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

        # 提取channel_name，并且进行推流
        if dict_json["status"]:
            channel_name = dict_json["channel_name"]
            self.json.write_data(channel_name, "channel_name_default")
            inbound_url = dict_json["inbound_url"]
            self.log.info(message="推流地址:%s" % inbound_url)
            # 调用推流函数
            self.stream.call_ffmpeg(inbound_url)

        # 断言
        self.log.info(message="第三步：断言")
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        self.assertTrue(dict_json["status"], msg=">>>断言失败，实际返回结果：%s" % dict_json)

    def test03_cre_live_channel(self):
        """默认profile和设定out_type的Live Tube，创建Live channel"""
        self.log.info(message="test03_cre_live_channel", name="test06_CreateLiveTube.py", line=get_run_line())
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

        # # 推流
        # if dict_json["status"]:
        #     inbound_url = dict_json["inbound_url"]
        #     self.logs.info(message="推流地址:%s" % inbound_url)
        #     self.stream.call_ffmpeg(inbound_url)

        # 断言
        self.log.info(message="第三步：断言")
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        self.assertTrue(dict_json["status"], msg=">>>断言失败，实际返回结果：%s" % dict_json)

    def test04_monitor_live_channel(self):
        """监控Live Channel信息"""
        self.log.info(message="test04_live_channel_info", name="test06_CreateLiveTube.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[3])
        data = self.data.get_param(self.sheet, self.row[3])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[3]) + data
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
        self.assertTrue(dict_json["is_ready"])

    def test05_monitor_live_channel(self):
        """监控Live Channel信息：不存在"""
        self.log.info(message="test05_live_channel_info", name="test06_CreateLiveTube.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[4])
        data = self.data.get_param(self.sheet, self.row[4])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[4]) + data
        headers = self.hea_data.get_header(self.sheet, self.row[4])
        expect = self.data.get_expect_result(self.sheet, self.row[4])
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

    def test06_live_channel_list(self):
        """获取所有Live Channel列表"""
        self.log.info(message="test06_live_channel_list", name="test06_CreateLiveTube.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[5])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[5])
        headers = self.hea_data.get_header(self.sheet, self.row[5])
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

    @unittest.skip
    def test07_live_channel_list(self):
        pass

    @unittest.skip
    def test08_live_channel_list(self):
        pass

    @unittest.skip
    def test09_live_channel_list(self):
        pass

    def test10_live_channel_info(self):
        """获取Live Channel详情"""
        self.log.info(message="test04_live_channel_info", name="test06_CreateLiveTube.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[9])
        data = self.data.get_param(self.sheet, self.row[9])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[9]) + data
        headers = self.hea_data.get_header(self.sheet, self.row[9])
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
        self.assertFalse(dict_json["is_tsArchive"])
        self.assertFalse(dict_json["is_ended"])
        for key in ["_id", "live_tube_id", "channel_name", "channel_title", "is_tsArchive", "is_ended", "created_time",
                    "playbackURL", "source_url", "updated", "status"]:
            self.assertIn(key, dict_json, msg="%s字段不在返回数据里" % key)
        for key in ["isVod", "hls_version", "hlsURL", "hlsURL_cdn"]:
            self.assertIn(key, dict_json["playbackURL"]["hlsOutput"][0], msg="%s字段不在返回数据里" % key)

    def test11_live_channel_info(self):
        """获取Live Channel详情：不存在"""
        self.log.info(message="test05_live_channel_info", name="test06_CreateLiveTube.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[10])
        data = self.data.get_param(self.sheet, self.row[10])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[10]) + data
        headers = self.hea_data.get_header(self.sheet, self.row[10])
        expect = self.data.get_expect_result(self.sheet, self.row[10])
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

    def test12_end_live_channel(self):
        """结束Live Channel"""
        self.log.info(message="test04_live_channel_info", name="test06_CreateLiveTube.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[11])
        data = self.data.get_param(self.sheet, self.row[11])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[11]) + data
        headers = self.hea_data.get_header(self.sheet, self.row[11])
        self.log.info(message="第一步: 获取请求数据")
        self.log.info(message="请求方法：%s" % method)
        self.log.info(message="接口地址：%s" % url)

        # 发送请求
        status_code, res_json = self.http.http_method(method=method, url=url, headers=headers)
        dict_json = json.loads(res_json)  # 把json数据转换成字典对象
        self.log.info(message="第二步:发送请求，获取返回数据：")
        self.log.info(message="%s" % res_json)

        # 检查是否结束成功
        if dict_json["status"]:
            check_data = self.check_live_channel()
            self.assertTrue(check_data["is_ended"], msg="Live Channel结束失败的！！")

        # 断言
        self.log.info(message="第三步：断言")
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        self.assertTrue(dict_json["status"], msg=">>>断言失败，实际返回结果：%s" % dict_json)

    def test13_end_live_channel(self):
        """获取Live Channel详情：不存在"""
        self.log.info(message="test05_live_channel_info", name="test06_CreateLiveTube.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[12])
        data = self.data.get_param(self.sheet, self.row[12])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[12]) + data
        headers = self.hea_data.get_header(self.sheet, self.row[12])
        expect = self.data.get_expect_result(self.sheet, self.row[12])
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

    def test14_delete_live_tube(self):
        """删除Live Tube"""
        self.log.info(message="test14_delete_live_tube", name="test06_CreateLiveTube.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[13])
        data = self.data.get_param(self.sheet, self.row[13])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[13]) + data
        headers = self.hea_data.get_header(self.sheet, self.row[13])
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

    def test15_delete_live_tube(self):
        """获取Live Tube详情：不存在"""
        self.log.info(message="test09_live_tube_info", name="test06_CreateLiveTube.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[14])
        data = self.data.get_param(self.sheet, self.row[14])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[14]) + data
        headers = self.hea_data.get_header(self.sheet, self.row[14])
        expect = self.data.get_expect_result(self.sheet, self.row[14])
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

    def test16_delete_live_channel(self):
        """删除Live Channel"""
        self.log.info(message="test16_delete_live_channel", name="test06_CreateLiveTube.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[15])
        data = self.data.get_param(self.sheet, self.row[15])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[15]) + data
        headers = self.hea_data.get_header(self.sheet, self.row[15])
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

    def test17_delete_live_channel(self):
        """获取Live Tube详情：不存在"""
        self.log.info(message="test17_delete_live_channel", name="test06_CreateLiveTube.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[16])
        data = self.data.get_param(self.sheet, self.row[16])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[16]) + data
        headers = self.hea_data.get_header(self.sheet, self.row[16])
        expect = self.data.get_expect_result(self.sheet, self.row[16])
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

    def check_live_channel(self):
        method = self.data.get_method(self.sheet, self.row[9])
        data = self.data.get_param(self.sheet, self.row[9])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[9]) + data
        headers = self.hea_data.get_header(self.sheet, self.row[9])
        # 发送请求
        status_code, res_json = self.http.http_method(method=method, url=url, headers=headers)
        dict_json = json.loads(res_json)  # 把json数据转换成字典对象
        return dict_json


if __name__ == "__main__":
    unittest.main()
