#!/usr/bin/python3
# coding=utf-8
import os
import unittest
import json

from urllib import request
from common.httpSet import HttpMethod
from common.logger import Logger
from common.operationJson import OperationJson
from common.readTestData import ReadTestData
from config.readConfig import ReadConfig
from common.getRunLine import get_run_line
from common.callShellFile import CallShell

proDir = os.path.split(os.path.realpath(__file__))[0]
file_name = os.path.join(proDir, "../../resources/get_play_url.json")


class TestPlaybackUrl(unittest.TestCase):
    def setUp(self):
        self.data = ReadTestData(file_name)
        self.hea_data = ReadTestData()
        self.http = HttpMethod()
        self.config = ReadConfig()
        self.log = Logger()
        self.stream = CallShell()
        self.json = OperationJson(file_name)
        self.sheet = 'sdk_test_case'
        self.row = list(range(2, 10))
        self.log.info(message="----------测试开始----------", name="test_PlaybackURL.py")

    def tearDown(self):
        self.log.info(message="----------测试结束----------", name="test_PlaybackURL.py")

    def test01_generate_token(self):
        """生成vod hls output playback token"""
        self.log.info(message="test01_generate_token", name="test_PlaybackURL.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[0])
        data = self.data.get_request_data(self.sheet, self.row[0])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[0])
        headers = self.hea_data.get_header(self.sheet, self.row[0])
        self.log.info(message="第一步: 获取请求数据")
        self.log.info(message="请求方法：%s" % method)
        self.log.info(message="请求接口：%s" % url)
        self.log.info(message="发送数据：%s" % data)

        # 发送请求
        status_code, res_json = self.http.http_method(method=method, url=url, data=data, headers=headers)
        dict_json = json.loads(res_json)  # 把json数据转换成字典对象
        self.log.info(message="第二步:发送请求，获取返回数据：")
        self.log.info(message="%s" % res_json)

        # 提取playback_token
        if dict_json["status"]:
            playback_token = dict_json["playback_token"]
            self.json.write_data(playback_token, "play_token_hls", "playback_token")

        # 断言
        self.log.info(message="第三步：断言")
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        self.assertTrue(dict_json["status"], msg=">>>断言失败，实际返回结果：%s" % dict_json)

    def test02_get_playback_url(self):
        """获取vod hls playback url"""
        self.log.info(message="test02_get_playback_url", name="test_PlaybackURL.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[1])
        data = self.data.get_request_data(self.sheet, self.row[1])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[1])
        headers = self.hea_data.get_header(self.sheet, self.row[1])
        self.log.info(message="第一步: 获取请求数据")
        self.log.info(message="请求方法：%s" % method)
        self.log.info(message="请求接口：%s" % url)
        self.log.info(message="发送数据：%s" % data)

        # 发送请求
        status_code, res_json = self.http.http_method(method=method, url=url, data=data, headers=headers)
        dict_json = json.loads(res_json)  # 把json数据转换成字典对象
        self.log.info(message="第二步:发送请求，获取返回数据：")
        self.log.info(message="%s" % res_json)

        # 提取playback_url
        if dict_json["status"]:
            playback_url = dict_json["playback_url"]
            self.log.info("VOD HLS播放地址：%s" % playback_url)
            # 判断播放地址是否有效L
            try:
                with request.urlopen(playback_url) as link:
                    self.assertEqual(link.status, 200, msg="VOD HLS播放地址是无效的")
                    self.log.info("VOD HLS播放地址是有效的")
            except Exception as e:
                self.log.error(message="VOD HLS播放地址是无效的：%s" % e)

        # 断言
        self.log.info(message="第三步：断言")
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        self.assertTrue(dict_json["status"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
        self.assertEqual(dict_json["playback_url"][-4:], "m3u8")

    def test03_generate_token(self):
        """生成vod mp4 output playback token"""
        self.log.info(message="test03_generate_tokenl", name="test_PlaybackURL.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[2])
        data = self.data.get_request_data(self.sheet, self.row[2])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[2])
        headers = self.hea_data.get_header(self.sheet, self.row[2])
        self.log.info(message="第一步: 获取请求数据")
        self.log.info(message="请求方法：%s" % method)
        self.log.info(message="请求接口：%s" % url)
        self.log.info(message="发送数据：%s" % data)

        # 发送请求
        status_code, res_json = self.http.http_method(method=method, url=url, data=data, headers=headers)
        dict_json = json.loads(res_json)  # 把json数据转换成字典对象
        self.log.info(message="第二步:发送请求，获取返回数据：")
        self.log.info(message="%s" % res_json)

        # 提取playback_token
        if dict_json["status"]:
            playback_token = dict_json["playback_token"]
            self.json.write_data(playback_token, "play_token_mp4", "playback_token")

        # 断言
        self.log.info(message="第三步：断言")
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        self.assertTrue(dict_json["status"], msg=">>>断言失败，实际返回结果：%s" % dict_json)

    def test04_get_playback_url(self):
        """获取vod hls playback url"""
        self.log.info(message="test04_get_playback_url", name="test_PlaybackURL.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[3])
        data = self.data.get_request_data(self.sheet, self.row[3])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[3])
        headers = self.hea_data.get_header(self.sheet, self.row[3])
        self.log.info(message="第一步: 获取请求数据")
        self.log.info(message="请求方法：%s" % method)
        self.log.info(message="请求接口：%s" % url)
        self.log.info(message="发送数据：%s" % data)

        # 发送请求
        status_code, res_json = self.http.http_method(method=method, url=url, data=data, headers=headers)
        dict_json = json.loads(res_json)  # 把json数据转换成字典对象
        self.log.info(message="第二步:发送请求，获取返回数据：")
        self.log.info(message="%s" % res_json)

        # 提取playback_url
        if dict_json["status"]:
            playback_url = dict_json["playback_url"]
            self.log.info("VOD MP4播放地址：%s" % playback_url)
            # 判断播放地址是否有效
            try:
                with request.urlopen(playback_url) as link:
                    self.assertEqual(link.status, 200, msg="VOD MP4播放地址是无效的")
                    self.log.info("VOD MP4播放地址是有效的")
            except Exception as e:
                self.log.error(message="VOD MP4播放地址是无效的：%s" % e)

        # 断言
        self.log.info(message="第三步：断言")
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        self.assertTrue(dict_json["status"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
        self.assertEqual(dict_json["playback_url"][-3:], "mp4")

    def test05_generate_token(self):
        """生成vod mp4 output playback token"""
        self.log.info(message="test05_generate_token", name="test_PlaybackURL.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[4])
        data = self.data.get_request_data(self.sheet, self.row[4])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[4])
        headers = self.hea_data.get_header(self.sheet, self.row[4])
        self.log.info(message="第一步: 获取请求数据")
        self.log.info(message="请求方法：%s" % method)
        self.log.info(message="请求接口：%s" % url)
        self.log.info(message="发送数据：%s" % data)

        # 发送请求
        status_code, res_json = self.http.http_method(method=method, url=url, data=data, headers=headers)
        dict_json = json.loads(res_json)  # 把json数据转换成字典对象
        self.log.info(message="第二步:发送请求，获取返回数据：")
        self.log.info(message="%s" % res_json)

        # 提取playback_token
        if dict_json["status"]:
            playback_token = dict_json["playback_token"]
            self.json.write_data(playback_token, "play_token_dash", "playback_token")

        # 断言
        self.log.info(message="第三步：断言")
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        self.assertTrue(dict_json["status"], msg=">>>断言失败，实际返回结果：%s" % dict_json)

    def test06_get_playback_url(self):
        """获取vod hls playback url"""
        self.log.info(message="test06_get_playback_url", name="test_PlaybackURL.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[5])
        data = self.data.get_request_data(self.sheet, self.row[5])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[5])
        headers = self.hea_data.get_header(self.sheet, self.row[5])
        self.log.info(message="第一步: 获取请求数据")
        self.log.info(message="请求方法：%s" % method)
        self.log.info(message="请求接口：%s" % url)
        self.log.info(message="发送数据：%s" % data)

        # 发送请求
        status_code, res_json = self.http.http_method(method=method, url=url, data=data, headers=headers)
        dict_json = json.loads(res_json)  # 把json数据转换成字典对象
        self.log.info(message="第二步:发送请求，获取返回数据：")
        self.log.info(message="%s" % res_json)

        # 提取playback_url
        if dict_json["status"]:
            playback_url = dict_json["playback_url"]
            self.log.info("VOD DASH播放地址：%s" % playback_url)
            # 判断播放地址是否有效
            try:
                with request.urlopen(playback_url) as link:
                    self.assertEqual(link.status, 200, msg="VOD DASH播放地址是无效的")
                    self.log.info("VOD DASH播放地址是有效的")
            except Exception as e:
                self.log.error(message="VOD DASH播放地址是无效的：%s" % e)

        # 断言
        self.log.info(message="第三步：断言")
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        self.assertTrue(dict_json["status"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
        self.assertEqual(dict_json["playback_url"][-3:], "mpd")

    def test07_generate_token(self):
        """生成playback token失败：media不存在"""
        self.log.info(message="test08_get_playback_url", name="test_PlaybackURL.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[6])
        data = self.data.get_request_data(self.sheet, self.row[6])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[6])
        headers = self.hea_data.get_header(self.sheet, self.row[6])
        expect = self.data.get_expect_result(self.sheet, self.row[6])
        self.log.info(message="第一步: 获取请求数据")
        self.log.info(message="请求方法：%s" % method)
        self.log.info(message="请求接口：%s" % url)
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

    def test08_get_playback_url(self):
        """获取playback url失败：playback token已使用"""
        self.log.info(message="test08_get_playback_url", name="test_PlaybackURL.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[7])
        data = self.data.get_request_data(self.sheet, self.row[7])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[7])
        headers = self.hea_data.get_header(self.sheet, self.row[7])
        expect = self.data.get_expect_result(self.sheet, self.row[7])
        self.log.info(message="第一步: 获取请求数据")
        self.log.info(message="请求方法：%s" % method)
        self.log.info(message="请求接口：%s" % url)
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


if __name__ == "__main__":
    unittest.main()
