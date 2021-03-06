#!/usr/bin/python3
# coding=utf-8
import json
import os
import unittest
import time

from common.httpSet import HttpMethod
from common.logger import Logger
from common.operationJson import OperationJson
from common.readTestData import ReadTestData
from config.readConfig import ReadConfig
from common.getRunLine import get_run_line

proDir = os.path.split(os.path.realpath(__file__))[0]
file_name = os.path.join(proDir, "../../resources/content_vod.json")
file_name1 = os.path.join(proDir, "../../resources/get_play_url.json")


class TestTranscodeAndListOut(unittest.TestCase):
    def setUp(self):
        self.data = ReadTestData(file_name)
        self.hea_data = ReadTestData()
        self.http = HttpMethod()
        self.config = ReadConfig()
        self.log = Logger()
        self.json = OperationJson(file_name)
        self.json1 = OperationJson(file_name1)
        self.sheet = 'cmb_test_case'
        self.row = list(range(38, 60))
        self.log.info(message="----------测试开始----------", name="test05_TranscodeAndListOut.py")

    def tearDown(self):
        self.log.info(message="----------测试结束----------", name="test05_TranscodeAndListOut.py")

    def test01_vod_out_list(self):
        """VOD Output列表为空"""
        self.log.info(message="test01_vod_out_list", name="test05_TranscodeAndListOut.py", line=get_run_line())
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

    def test02_vod_encode(self):
        """使用默认Profile进行转码"""
        self.log.info(message="test02_vod_encode", name="test05_TranscodeAndListOut.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[1])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[1])
        headers = self.hea_data.get_header(self.sheet, self.row[1])
        data = self.data.get_request_data(self.sheet, self.row[1])
        self.log.info(message="第一步: 获取请求数据")
        self.log.info(message="请求方法：%s" % method)
        self.log.info(message="接口地址：%s" % url)
        self.log.info(message="发送数据：%s" % data)

        # 发送请求
        status_code, res_json = self.http.http_method(method=method, data=data, url=url, headers=headers)
        dict_json = json.loads(res_json)  # 把json数据转换成字典对象
        self.log.info(message="第二步:发送请求，获取返回数据：")
        self.log.info(message="%s" % res_json)

        # 提取library_id
        if dict_json["status"]:
            library_id = dict_json["library"][0]
            w_library_id = [library_id]
            self.json.write_data(w_library_id, "trans_coding_info_1", "library_id")
            self.json.write_data(library_id, "library_id_1")
            # 把library_id写入get_play_url.json文件
            for i in ["get_play_token_hls", "get_play_token_mp4", "get_play_token_dash"]:
                self.json1.write_data(library_id, i, "media_id")

        # 断言
        self.log.info(message="第三步：断言")
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        self.assertTrue(dict_json["status"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
        self.assertIsInstance(dict_json["library"], list, msg="断言失败，实际返回结果：%s" % type(dict_json["library"]))

    def test03_vod_encode(self):
        """设定输出和Profile进行转码"""
        self.log.info(message="test03_vod_encode", name="test05_TranscodeAndListOut.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[2])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[2])
        headers = self.hea_data.get_header(self.sheet, self.row[2])
        data = self.data.get_request_data(self.sheet, self.row[2])
        self.log.info(message="第一步: 获取请求数据")
        self.log.info(message="请求方法：%s" % method)
        self.log.info(message="接口地址：%s" % url)
        self.log.info(message="发送数据：%s" % data)

        # 发送请求
        status_code, res_json = self.http.http_method(method=method, data=data, url=url, headers=headers)
        dict_json = json.loads(res_json)  # 把json数据转换成字典对象
        self.log.info(message="第二步:发送请求，获取返回数据：")
        self.log.info(message="%s" % res_json)

        # 提取library_id
        if dict_json["status"]:
            library_id = dict_json["library"][0]
            w_library_id = [library_id]
            self.json.write_data(w_library_id, "trans_coding_info_2", "library_id")
            self.json.write_data(library_id, "library_id_2")
            self.json.write_data(library_id, "library_id_source2")

        # 断言
        self.log.info(message="第三步：断言")
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        self.assertTrue(dict_json["status"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
        self.assertIsInstance(dict_json["library"], list, msg="断言失败，实际返回结果：%s" % type(dict_json["library"]))

    def test04_vod_encode(self):
        """启动转码失败：source_file_id错误"""
        self.log.info(message="test01_vod_out_list", name="test05_TranscodeAndListOut.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[3])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[3])
        headers = self.hea_data.get_header(self.sheet, self.row[3])
        data = self.data.get_request_data(self.sheet, self.row[3])
        expect = self.data.get_expect_result(self.sheet, self.row[3])
        self.log.info(message="第一步: 获取请求数据")
        self.log.info(message="请求方法：%s" % method)
        self.log.info(message="接口地址：%s" % url)
        self.log.info(message="发送数据：%s" % data)
        self.log.info(message="期望结果：%s" % expect)

        # 发送请求
        status_code, res_json = self.http.http_method(method=method, url=url, data=data, headers=headers)
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

    def test05_vod_out_list(self):
        """获取所有vod output列表"""
        self.log.info(message="test05_vod_out_list", name="test05_TranscodeAndListOut.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[4])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[4])
        headers = self.hea_data.get_header(self.sheet, self.row[4])
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
        self.assertFalse(dict_json["hasPrevious"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
        self.assertFalse(dict_json["hasNext"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
        self.assertIsInstance(dict_json["results"], list, msg="断言失败，实际返回结果：%s" % type(dict_json["results"]))
        self.assertEqual(dict_json["total_count"], 2, msg=">>>断言失败，实际返回结果：%s" % dict_json["total_count"])
        self.assertEqual(len(dict_json["results"]), dict_json["total_count"],
                         msg=">>>断言失败，实际返回结果：%s" % len(dict_json["results"]))
        for key in ["results", "previous", "hasPrevious", "next", "hasNext", "total_count", "status"]:
            self.assertIn(key, dict_json, msg="%s字段不在返回数据里面" % key)

    def test06_vod_out_list(self):
        """获取output列表：设置返回数量为1"""
        self.log.info(message="test06_vod_out_list", name="test05_TranscodeAndListOut.py", line=get_run_line())
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

        # 提取next_id
        if dict_json["status"]:
            next_id = dict_json["next"]
            self.json.write_data(next_id, "next_id", "next")

        # 断言
        self.log.info(message="第三步：断言")
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        self.assertTrue(dict_json["status"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
        self.assertFalse(dict_json["hasPrevious"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
        self.assertTrue(dict_json["hasNext"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
        self.assertIsInstance(dict_json["results"], list, msg="断言失败，实际返回结果：%s" % type(dict_json["results"]))
        self.assertEqual(dict_json["total_count"], 2, msg=">>>断言失败，实际返回结果：%s" % dict_json["total_count"])
        self.assertNotEqual(len(dict_json["results"]), dict_json["total_count"],
                            msg=">>>断言失败，实际返回结果：%s" % len(dict_json["results"]))
        for key in ["results", "previous", "hasPrevious", "next", "hasNext", "total_count", "status"]:
            self.assertIn(key, dict_json, msg="%s字段不在返回数据里面" % key)

    def test07_vod_out_list(self):
        """获取output列表：返回下一页"""
        self.log.info(message="test07_vod_out_list", name="test05_TranscodeAndListOut.py", line=get_run_line())
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

        # 提取previous_id
        if dict_json["status"]:
            previous_id = dict_json["previous"]
            self.json.write_data(previous_id, "previous_id", "previous")

        # 断言
        self.log.info(message="第三步：断言")
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        self.assertTrue(dict_json["status"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
        self.assertTrue(dict_json["hasPrevious"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
        self.assertFalse(dict_json["hasNext"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
        self.assertIsInstance(dict_json["results"], list, msg="断言失败，实际返回结果：%s" % type(dict_json["results"]))
        self.assertEqual(dict_json["total_count"], 2, msg=">>>断言失败，实际返回结果：%s" % dict_json["total_count"])
        self.assertNotEqual(len(dict_json["results"]), dict_json["total_count"],
                            msg=">>>断言失败，实际返回结果：%s" % len(dict_json["results"]))
        for key in ["results", "previous", "hasPrevious", "next", "hasNext", "total_count", "status"]:
            self.assertIn(key, dict_json, msg="%s字段不在返回数据里面" % key)

    def test08_vod_out_list(self):
        """获取output列表：返回上一页"""
        self.log.info(message="test07_vod_out_list", name="test05_TranscodeAndListOut.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[7])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[7])
        data = self.data.get_param(self.sheet, self.row[7])
        headers = self.hea_data.get_header(self.sheet, self.row[7])
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
        self.assertFalse(dict_json["hasPrevious"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
        self.assertTrue(dict_json["hasNext"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
        self.assertIsInstance(dict_json["results"], list, msg="断言失败，实际返回结果：%s" % type(dict_json["results"]))
        self.assertEqual(dict_json["total_count"], 2, msg=">>>断言失败，实际返回结果：%s" % dict_json["total_count"])
        self.assertNotEqual(len(dict_json["results"]), dict_json["total_count"],
                            msg=">>>断言失败，实际返回结果：%s" % len(dict_json["results"]))
        for key in ["results", "previous", "hasPrevious", "next", "hasNext", "total_count", "status"]:
            self.assertIn(key, dict_json, msg="%s字段不在返回数据里面" % key)

    def test09_monitor_encode(self):
        """查询VOD转码情况"""
        self.log.info(message="test07_vod_out_list", name="test05_TranscodeAndListOut.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[8])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[8])
        data = self.data.get_request_data(self.sheet, self.row[8])
        headers = self.hea_data.get_header(self.sheet, self.row[8])
        self.log.info(message="第一步: 获取请求数据")
        self.log.info(message="请求方法：%s" % method)
        self.log.info(message="接口地址：%s" % url)
        self.log.info(message="请求数据：%s" % data)

        # 发送请求
        status_code, res_json = self.http.http_method(method=method, url=url, data=data, headers=headers)
        dict_json = json.loads(res_json)  # 把json数据转换成字典对象
        self.log.info(message="第二步:发送请求，获取返回数据：")
        self.log.info(message="%s" % res_json)

        # 断言
        self.log.info(message="第三步：断言")
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        self.assertTrue(dict_json["status"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
        self.assertIsInstance(dict_json["results"], list, msg="断言失败，实际返回结果：%s" % type(dict_json["results"]))
        for key in ["library_id", "encode_status", "encode_progress"]:
            self.assertIn(key, dict_json["results"][0], msg="%s字段不在返回数据里面" % key)

    def test10_monitor_encode(self):
        """启查询VOD转码情况：media不存在"""
        self.log.info(message="test10_monitor_encode", name="test05_TranscodeAndListOut.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[9])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[9])
        headers = self.hea_data.get_header(self.sheet, self.row[9])
        data = self.data.get_request_data(self.sheet, self.row[9])
        expect = self.data.get_expect_result(self.sheet, self.row[9])
        self.log.info(message="第一步: 获取请求数据")
        self.log.info(message="请求方法：%s" % method)
        self.log.info(message="接口地址：%s" % url)
        self.log.info(message="发送数据：%s" % data)
        self.log.info(message="期望结果：%s" % expect)

        # 发送请求
        status_code, res_json = self.http.http_method(method=method, url=url, data=data, headers=headers)
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

    def test11_get_out_info(self):
        """获取VOD Output详情"""
        self.log.info(message="test11_get_out_info", name="test05_TranscodeAndListOut.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[10])
        data = self.data.get_param(self.sheet, self.row[10])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[10]) + data
        headers = self.hea_data.get_header(self.sheet, self.row[10])
        self.log.info(message="第一步: 获取请求数据")
        self.log.info(message="请求方法：%s" % method)
        self.log.info(message="接口地址：%s" % url)

        # 检查转码情况
        check_data = self.check_encode()
        if check_data["results"][0]["encode_status"] != 3:
            # 发送请求
            self.log.info("检查未转码完成的VOD Output详情信息")
            status_code, res_json = self.http.http_method(method=method, url=url, headers=headers)
            dict_json = json.loads(res_json)  # 把json数据转换成字典对象
            self.log.info(message="第二步:发送请求，获取未转码完成的VOD Output数据：")
            self.log.info(message="%s" % res_json)

            # 断言
            self.log.info(message="第三步：断言")
            self.assertEqual(status_code, 200, msg=">>>接口请求失败")
            self.assertTrue(dict_json["status"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
            self.assertNotEqual(dict_json["encode_status"], 4, msg=">>>断言失败，实际返回结果：%s" % dict_json["encode_status"])
            self.assertEqual(len(dict_json["playbackURL"]["hlsOutput"]), 1)
            self.assertEqual(len(dict_json["playbackURL"]["mp4Output"]), 0)
            self.assertEqual(len(dict_json["playbackURL"]["dashOutput"]), 0)
            key_list = ["_id", "source_file_id", "playbackURL", "type", "profile", "recordType",
                        "enableExternalPackager", "tsOutput", "kernel", "created_time", "encode_start_time", "owner",
                        "audiotracklist", "encode_status", "encode_progress", "enableEncryption", "status"]
            for key in key_list:
                self.assertIn(key, dict_json, msg="%s字段不在返回数据里面" % key)

            # 等待转码完成，检查转码完成后的VOD Output详情信息
            self.log.info(message="等待90秒,待VOD转码完成...")
            time.sleep(90)
            check_data = self.check_encode()
            if check_data["results"][0]["encode_status"] == 3:
                # 发送请求
                self.log.info("等待转码完成，检查转码完成后的VOD Output详情信息")
                status_code, res_json = self.http.http_method(method=method, url=url, headers=headers)
                dict_json = json.loads(res_json)  # 把json数据转换成字典对象
                self.log.info(message="第二步:发送请求，获取转码完成后的VOD Output数据：")
                self.log.info(message="%s" % res_json)

                # 断言
                self.log.info(message="第三步：断言")
                self.assertEqual(status_code, 200, msg=">>>接口请求失败")
                self.assertTrue(dict_json["status"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
                self.assertEqual(dict_json["encode_status"], 4, msg=">>>断言失败，实际返回结果：%s" % dict_json["encode_status"])
                self.assertEqual(len(dict_json["playbackURL"]["hlsOutput"]), 3)
                self.assertEqual(len(dict_json["playbackURL"]["mp4Output"]), 2)
                self.assertEqual(len(dict_json["playbackURL"]["dashOutput"]), 2)
                key_list = ["_id", "source_file_id", "playbackURL", "type", "profile", "recordType",
                            "enableExternalPackager", "tsOutput", "kernel", "created_time", "encode_start_time",
                            "owner",
                            "audiotracklist", "encode_status", "encode_progress", "process", "duration", "info",
                            "encode_finish_time", "upload_finish_time", "enableEncryption", "encoding_duration",
                            "upload_duration",
                            "status"]
                for key in key_list:
                    self.assertIn(key, dict_json, msg="%s字段不在返回数据里面" % key)
            else:
                self.log.error(message="VOD无法进行转码!!!", name="test05_TranscodeAndListOut.py", line=get_run_line())
        else:
            # 发送请求
            status_code, res_json = self.http.http_method(method=method, url=url, headers=headers)
            dict_json = json.loads(res_json)  # 把json数据转换成字典对象
            self.log.info(message="第二步:发送请求，获取返回数据：")
            self.log.info(message="%s" % res_json)

            # 断言
            self.log.info(message="第三步：断言")
            self.assertEqual(status_code, 200, msg=">>>接口请求失败")
            self.assertTrue(dict_json["status"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
            self.assertEqual(dict_json["encode_status"], 4, msg=">>>断言失败，实际返回结果：%s" % dict_json["encode_status"])
            self.assertEqual(len(dict_json["playbackURL"]["hlsOutput"]), 3)
            self.assertEqual(len(dict_json["playbackURL"]["mp4Output"]), 2)
            self.assertEqual(len(dict_json["playbackURL"]["dashOutput"]), 2)
            key_list = ["_id", "source_file_id", "playbackURL", "type", "profile", "recordType",
                        "enableExternalPackager", "tsOutput", "kernel", "created_time", "encode_start_time",
                        "owner",
                        "audiotracklist", "encode_status", "encode_progress", "process", "duration", "info",
                        "encode_finish_time", "upload_finish_time", "enableEncryption", "encoding_duration",
                        "upload_duration",
                        "status"]
            for key in key_list:
                self.assertIn(key, dict_json, msg="%s字段不在返回数据里面" % key)

    def test12_get_out_info(self):
        """获取VOD Output详情：media不存在"""
        self.log.info(message="test12_get_out_info", name="test05_TranscodeAndListOut.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[11])
        data = self.data.get_param(self.sheet, self.row[11])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[11]) + data
        headers = self.hea_data.get_header(self.sheet, self.row[11])
        expect = self.data.get_expect_result(self.sheet, self.row[11])
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

    def test13_source_list(self):
        """获取所有Source file列表"""
        self.log.info(message="test13_source_list", name="test05_TranscodeAndListOut.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[12])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[12])
        headers = self.hea_data.get_header(self.sheet, self.row[12])
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
        self.assertFalse(dict_json["hasPrevious"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
        self.assertFalse(dict_json["hasNext"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
        self.assertIsInstance(dict_json["results"], list, msg="断言失败，实际返回结果：%s" % type(dict_json["results"]))
        self.assertEqual(dict_json["total_count"], 2, msg=">>>断言失败，实际返回结果：%s" % dict_json["total_count"])
        self.assertEqual(len(dict_json["results"]), dict_json["total_count"],
                         msg=">>>断言失败，实际返回结果：%s" % len(dict_json["results"]))
        for key in ["results", "previous", "hasPrevious", "next", "hasNext", "total_count", "status"]:
            self.assertIn(key, dict_json, msg="%s字段不在返回数据里面" % key)

    def test14_source_list(self):
        """获取Source file列表：设置返回数量为1"""
        self.log.info(message="test14_source_list", name="test05_TranscodeAndListOut.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[13])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[13])
        data = self.data.get_param(self.sheet, self.row[13])
        headers = self.hea_data.get_header(self.sheet, self.row[13])
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
            self.json.write_data(next_id, "next_id_1", "next")

        # 断言
        self.log.info(message="第三步：断言")
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        self.assertTrue(dict_json["status"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
        self.assertFalse(dict_json["hasPrevious"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
        self.assertTrue(dict_json["hasNext"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
        self.assertIsInstance(dict_json["results"], list, msg="断言失败，实际返回结果：%s" % type(dict_json["results"]))
        self.assertEqual(dict_json["total_count"], 2, msg=">>>断言失败，实际返回结果：%s" % dict_json["total_count"])
        self.assertNotEqual(len(dict_json["results"]), dict_json["total_count"],
                            msg=">>>断言失败，实际返回结果：%s" % len(dict_json["results"]))
        for key in ["results", "previous", "hasPrevious", "next", "hasNext", "total_count", "status"]:
            self.assertIn(key, dict_json, msg="%s字段不在返回数据里面" % key)

    def test15_source_list(self):
        """获取output列表：返回下一页"""
        self.log.info(message="test07_vod_out_list", name="test05_TranscodeAndListOut.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[14])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[14])
        data = self.data.get_param(self.sheet, self.row[14])
        headers = self.hea_data.get_header(self.sheet, self.row[14])
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
            self.json.write_data(previous_id, "previous_id_1", "previous")

        # 断言
        self.log.info(message="第三步：断言")
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        self.assertTrue(dict_json["status"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
        self.assertTrue(dict_json["hasPrevious"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
        self.assertFalse(dict_json["hasNext"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
        self.assertIsInstance(dict_json["results"], list, msg="断言失败，实际返回结果：%s" % type(dict_json["results"]))
        self.assertEqual(dict_json["total_count"], 2, msg=">>>断言失败，实际返回结果：%s" % dict_json["total_count"])
        self.assertNotEqual(len(dict_json["results"]), dict_json["total_count"],
                            msg=">>>断言失败，实际返回结果：%s" % len(dict_json["results"]))
        for key in ["results", "previous", "hasPrevious", "next", "hasNext", "total_count", "status"]:
            self.assertIn(key, dict_json, msg="%s字段不在返回数据里面" % key)

    def test16_source_list(self):
        """获取output列表：返回上一页"""
        self.log.info(message="test16_source_list", name="test05_TranscodeAndListOut.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[15])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[15])
        data = self.data.get_param(self.sheet, self.row[15])
        headers = self.hea_data.get_header(self.sheet, self.row[15])
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
        self.assertFalse(dict_json["hasPrevious"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
        self.assertTrue(dict_json["hasNext"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
        self.assertIsInstance(dict_json["results"], list, msg="断言失败，实际返回结果：%s" % type(dict_json["results"]))
        self.assertEqual(dict_json["total_count"], 2, msg=">>>断言失败，实际返回结果：%s" % dict_json["total_count"])
        self.assertNotEqual(len(dict_json["results"]), dict_json["total_count"],
                            msg=">>>断言失败，实际返回结果：%s" % len(dict_json["results"]))
        for key in ["results", "previous", "hasPrevious", "next", "hasNext", "total_count", "status"]:
            self.assertIn(key, dict_json, msg="%s字段不在返回数据里面" % key)

    def test17_get_source_info(self):
        """获取Source file详情信息"""
        self.log.info(message="test17_get_source_info", name="test05_TranscodeAndListOut.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[16])
        data = self.data.get_param(self.sheet, self.row[16])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[16]) + data
        headers = self.hea_data.get_header(self.sheet, self.row[16])
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
        self.assertEqual(dict_json["vod_source_object"]["recordType"], "fileTransfer")
        self.assertEqual(dict_json["vod_source_object"]["originalfilename"], "sample.mp4")
        for key in ["_id", "path", "filename", "originalfilename", "filesize", "type", "recordType", "language"]:
            self.assertIn(key, dict_json["vod_source_object"], msg="%s字段不在返回数据里面" % key)

    def test18_get_source_info(self):
        """获取Source file详情信息：不存在"""
        self.log.info(message="test18_get_source_info", name="test05_TranscodeAndListOut.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[17])
        data = self.data.get_param(self.sheet, self.row[17])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[17]) + data
        headers = self.hea_data.get_header(self.sheet, self.row[17])
        expect = self.data.get_expect_result(self.sheet, self.row[17])
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

    def test19_delete_source(self):
        """删除VOD Source file"""
        self.log.info(message="test19_delete_source", name="test05_TranscodeAndListOut.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[18])
        data = self.data.get_param(self.sheet, self.row[18])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[18]) + data
        headers = self.hea_data.get_header(self.sheet, self.row[18])
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

        # 检查Source file是否删除成功
        if dict_json["status"]:
            check_data = self.check_library()
            self.assertEqual(check_data["source_file_id"], None,
                             msg="检查Source file是否删除成功不通过，实际返回：%s" % check_data["source_file_id"])

    def test20_delete_source(self):
        """获取Source file详情信息：不存在"""
        self.log.info(message="test20_delete_source", name="test05_TranscodeAndListOut.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[19])
        data = self.data.get_param(self.sheet, self.row[19])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[19]) + data
        headers = self.hea_data.get_header(self.sheet, self.row[19])
        expect = self.data.get_expect_result(self.sheet, self.row[19])
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

    def test21_delete_output(self):
        """删除VOD Output"""
        self.log.info(message="test21_delete_output", name="test05_TranscodeAndListOut.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[20])
        data = self.data.get_param(self.sheet, self.row[20])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[20]) + data
        headers = self.hea_data.get_header(self.sheet, self.row[20])
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

        # 检查VOD Output是否删除成功
        if dict_json["status"]:
            check_data = self.check_library()
            self.log.info(message="check_data数据：%s" % check_data)
            self.assertTrue(check_data["status"], msg="检查VOD Output是否删除成功不通过，实际返回：%s" % check_data)
            self.assertEqual(check_data["err"]["code"], 404, msg=">>>断言失败，实际返回结果：%s" % check_data["err"]["code"])
            self.assertEqual(check_data["err"]["message"], "Library doesn't exist",
                             msg=">>>断言失败，实际返回结果：%s" % check_data["err"]["message"])

    def test22_delete_output(self):
        """获取Source file详情信息：不存在"""
        self.log.info(message="test20_delete_source", name="test05_TranscodeAndListOut.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[21])
        data = self.data.get_param(self.sheet, self.row[21])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[21]) + data
        headers = self.hea_data.get_header(self.sheet, self.row[21])
        expect = self.data.get_expect_result(self.sheet, self.row[21])
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

    def check_encode(self):
        method = self.data.get_method(self.sheet, self.row[8])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[8])
        data = self.data.get_request_data(self.sheet, self.row[8])
        headers = self.hea_data.get_header(self.sheet, self.row[8])
        # 发送请求
        status_code, res_json = self.http.http_method(method=method, url=url, data=data, headers=headers)
        dict_json = json.loads(res_json)
        return dict_json

    def check_library(self):
        method = self.data.get_method(self.sheet, self.row[10])
        data = self.data.get_param(self.sheet, self.row[20])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[10]) + data
        headers = self.hea_data.get_header(self.sheet, self.row[10])
        # 发送请求
        status_code, res_json = self.http.http_method(method=method, url=url, headers=headers)
        dict_json = json.loads(res_json)
        return dict_json


if __name__ == "__main__":
    unittest.main()
