#!/usr/bin/python3
# coding=utf-8
import json
import os
import unittest

from common.httpSet import HttpMethod
from common.logger import Logger
from common.operationJson import OperationJson
from common.readTestData import ReadTestData
from config.readConfig import ReadConfig
from common.getRunLine import get_run_line

proDir = os.path.split(os.path.realpath(__file__))[0]
file_name = os.path.join(proDir, "../../resources/profile.json")


class TestProfile(unittest.TestCase):
    def setUp(self):
        self.data = ReadTestData(file_name)
        self.hea_data = ReadTestData()
        self.http = HttpMethod()
        self.config = ReadConfig()
        self.log = Logger()
        self.json = OperationJson(file_name)
        self.sheet = 'cmb_test_case'
        self.row = list(range(18, 32))
        self.log.info(message="----------测试开始----------", name="test03_ProcProfile.py")

    def tearDown(self):
        self.log.info(message="----------测试结束----------", name="test03_ProcProfile.py")

    def test01_cre_vod_profile(self):
        """创建vod profile"""
        self.log.info(message="test01_cre_vod_profile", name="test03_ProcProfile.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[0])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[0])
        data = self.data.get_request_data(self.sheet, self.row[0])
        headers = self.hea_data.get_header(self.sheet, self.row[0])
        self.log.info(message="第一步: 获取请求数据")
        self.log.info(message="请求方法：%s" % method)
        self.log.info(message="接口地址：%s" % url)
        self.log.info(message="请求头部：%s" % headers)
        self.log.info(message="发送数据：%s" % data)

        # 发送请求
        status_code, res_json = self.http.http_method(method=method, url=url, data=data, headers=headers)
        dict_json = json.loads(res_json)  # 把json数据转换成字典对象
        self.log.info(message="第二步:发送请求，获取返回数据：")
        self.log.info(message="%s" % res_json)

        # 提取profile_id
        if dict_json["status"]:
            profile_id = dict_json["proc_profile_id"]
            self.json.write_data(profile_id, "vod_profile_id")
            self.json.write_data(profile_id, "update_proc_profile", "_id")

        # 断言
        self.log.info(message="第三步：断言")
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        self.assertTrue(dict_json["status"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
        self.assertIn("proc_profile_id", dict_json)

    def test02_cre_live_profile(self):
        """创建live profile"""
        self.log.info(message="test02_cre_live_profile", name="test03_ProcProfile.py", line=get_run_line())
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

        # 提取profile_id
        if dict_json["status"]:
            profile_id = dict_json["proc_profile_id"]
            self.json.write_data(profile_id, "live_profile_id")

        # 断言
        self.log.info(message="第三步：断言")
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        self.assertTrue(dict_json["status"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
        self.assertIn("proc_profile_id", dict_json)

    def test03_cre_profile_fail(self):
        """创建profile失败：profile_name无效"""
        self.log.info(message="test03_cre_profile_fail", name="test03_ProcProfile.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[2])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[2])
        data = self.data.get_request_data(self.sheet, self.row[2])
        headers = self.hea_data.get_header(self.sheet, self.row[2])
        expect = self.data.get_expect_result(self.sheet, self.row[2])
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

    def test04_cre_profile_fail(self):
        """创建profile失败：profile_name已经存在"""
        self.log.info(message="test04_cre_profile_fail", name="test03_ProcProfile.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[3])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[3])
        data = self.data.get_request_data(self.sheet, self.row[3])
        headers = self.hea_data.get_header(self.sheet, self.row[3])
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

    def test05_get_profile_list(self):
        """获取所有profile列表"""
        self.log.info(message="test05_get_profile_list", name="test03_ProcProfile.py", line=get_run_line())
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
        for key in ["results", "previous", "hasPrevious", "next", "hasNext", "total_count", "status"]:
            self.assertIn(key, dict_json, msg=">>>返回数据里面没有该字段：%s" % key)
        cun = len(dict_json["results"])
        self.assertEqual(cun, 6, msg=">>>断言失败，实际返回结果：%s" % cun)
        self.assertEqual(dict_json["total_count"], cun, msg=">>>断言失败，实际返回结果：%s" % dict_json["total_count"])

    def test06_get_profile_list(self):
        """获取所有profile列表：设置返回数量为1"""
        self.log.info(message="test06_get_profile_list", name="test03_ProcProfile.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[5])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[5])
        data = self.data.get_param(self.sheet, self.row[5])
        headers = self.hea_data.get_header(self.sheet, self.row[5])
        self.log.info(message="第一步: 获取请求数据")
        self.log.info(message="请求方法：%s" % method)
        self.log.info(message="接口地址：%s" % url)

        # 发送请求
        status_code, res_json = self.http.http_method(method=method, url=url, data=data, headers=headers)
        dict_json = json.loads(res_json)  # 把json数据转换成字典对象
        self.log.info(message="第二步:发送请求，获取返回数据：")
        self.log.info(message="%s" % res_json)

        # 提取获取下一页的数据next_id
        if dict_json["status"]:
            next_id = dict_json["next"]
            self.json.write_data(next_id, "next_id", "next")

        # 断言
        self.log.info(message="第三步：断言")
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        self.assertTrue(dict_json["status"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
        for key in ["results", "previous", "hasPrevious", "next", "hasNext", "total_count", "status"]:
            self.assertIn(key, dict_json, msg=">>>返回数据里面没有该字段：%s" % key)
        cun = len(dict_json["results"])
        self.assertEqual(cun, 1, msg=">>>断言失败，实际返回结果：%s" % cun)
        self.assertFalse(dict_json["hasPrevious"], msg=">>>断言失败，实际返回结果：%s" % dict_json["hasPrevious"])
        self.assertTrue(dict_json["hasNext"], msg=">>>断言失败，实际返回结果：%s" % dict_json["hasNext"])
        self.assertEqual(dict_json["total_count"], 6, msg=">>>断言失败，实际返回结果：%s" % dict_json["total_count"])

    def test07_get_profile_list(self):
        """获取所有profile列表：返回下一页"""
        self.log.info(message="test07_get_profile_list", name="test03_ProcProfile.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[6])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[6])
        data = self.data.get_param(self.sheet, self.row[6])
        headers = self.hea_data.get_header(self.sheet, self.row[6])
        self.log.info(message="第一步: 获取请求数据")
        self.log.info(message="请求方法：%s" % method)
        self.log.info(message="接口地址：%s" % url)

        # 发送请求
        status_code, res_json = self.http.http_method(method=method, url=url, data=data, headers=headers)
        dict_json = json.loads(res_json)  # 把json数据转换成字典对象
        self.log.info(message="第二步:发送请求，获取返回数据：")
        self.log.info(message="%s" % res_json)

        # 提取获取下一页的数据previous_id
        if dict_json["status"]:
            previous_id = dict_json["next"]
            self.json.write_data(previous_id, "previous_id", "previous")

        # 断言
        self.log.info(message="第三步：断言")
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        self.assertTrue(dict_json["status"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
        for key in ["results", "previous", "hasPrevious", "next", "hasNext", "total_count", "status"]:
            self.assertIn(key, dict_json, msg=">>>返回数据里面没有该字段：%s" % key)
        cun = len(dict_json["results"])
        self.assertEqual(cun, 1, msg=">>>断言失败，实际返回结果：%s" % cun)
        self.assertTrue(dict_json["previous"], msg=">>>断言失败，实际返回结果：%s" % dict_json["previous"])
        self.assertTrue(dict_json["hasNext"], msg=">>>断言失败，实际返回结果：%s" % dict_json["hasNext"])
        self.assertEqual(dict_json["total_count"], 6, msg=">>>断言失败，实际返回结果：%s" % dict_json["total_count"])

    def test08_get_profile_list(self):
        """获取所有profile列表：返回上一页"""
        self.log.info(message="test08_get_profile_list", name="test03_ProcProfile.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[7])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[7])
        data = self.data.get_param(self.sheet, self.row[7])
        headers = self.hea_data.get_header(self.sheet, self.row[7])
        self.log.info(message="第一步: 获取请求数据")
        self.log.info(message="请求方法：%s" % method)
        self.log.info(message="接口地址：%s" % url)

        # 发送请求
        status_code, res_json = self.http.http_method(method=method, url=url, data=data, headers=headers)
        dict_json = json.loads(res_json)  # 把json数据转换成字典对象
        self.log.info(message="第二步:发送请求，获取返回数据：")
        self.log.info(message="%s" % res_json)

        # 断言
        self.log.info(message="第三步：断言")
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        self.assertTrue(dict_json["status"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
        for key in ["results", "previous", "hasPrevious", "next", "hasNext", "total_count", "status"]:
            self.assertIn(key, dict_json, msg=">>>返回数据里面没有该字段：%s" % key)
        cun = len(dict_json["results"])
        self.assertEqual(cun, 1, msg=">>>断言失败，实际返回结果：%s" % cun)
        self.assertTrue(dict_json["previous"], msg=">>>断言失败，实际返回结果：%s" % dict_json["previous"])
        self.assertTrue(dict_json["hasNext"], msg=">>>断言失败，实际返回结果：%s" % dict_json["hasNext"])
        self.assertEqual(dict_json["total_count"], 6, msg=">>>断言失败，实际返回结果：%s" % dict_json["total_count"])

    def test09_get_profile_info(self):
        """读取vod profile的详情信息"""
        self.log.info(message="test09_get_profile_info", name="test03_ProcProfile.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[8])
        data = self.data.get_param(self.sheet, self.row[8])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[8]) + data
        headers = self.hea_data.get_header(self.sheet, self.row[8])
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
        for key in ["_id", "profile_name", "profile_type", "is_default", "is_user", "is_video_out", "is_audio_out",
                    "is_transcode", "video_frame_rate", "transcode_video_info", "is_facialDetect_out",
                    "is_thumbnail_out", "is_use", "status"]:
            self.assertIn(key, dict_json, msg=">>>返回数据里面没有该字段：%s" % key)

    def test10_get_profile_info(self):
        """读取信息失败：profile_id不存在"""
        self.log.info(message="test10_get_profile_info", name="test03_ProcProfile.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[9])
        data = self.data.get_param(self.sheet, self.row[9])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[9]) + data
        headers = self.hea_data.get_header(self.sheet, self.row[9])
        expect = self.data.get_expect_result(self.sheet, self.row[9])
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

    def test11_update_profile(self):
        """更新profile"""
        self.log.info(message="test11_update_profile", name="test03_ProcProfile.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[10])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[10])
        data = self.data.get_request_data(self.sheet, self.row[10])
        headers = self.hea_data.get_header(self.sheet, self.row[10])
        self.log.info(message="第一步: 获取请求数据")
        self.log.info(message="请求方法：%s" % method)
        self.log.info(message="接口地址：%s" % url)
        self.log.info(message="发送数据：%s" % data)

        # 发送请求
        status_code, res_json = self.http.http_method(method=method, url=url, data=data, headers=headers)
        dict_json = json.loads(res_json)  # 把json数据转换成字典对象
        self.log.info(message="第二步:发送请求，获取返回数据：")
        self.log.info(message="%s" % res_json)

        # 断言
        self.log.info(message="第三步：断言")
        self.assertEqual(status_code, 200, msg=">>>接口请求失败")
        self.assertTrue(dict_json["status"], msg=">>>断言失败，实际返回结果：%s" % dict_json)

        # 检验profile是否更新成功
        if dict_json["status"]:
            check_data = self.check_profile()
            self.assertTrue(check_data["status"], msg="检验profile是否更新成功不通过")
            self.assertEqual(check_data["profile_name"], data["profile_name"])
            self.assertEqual(check_data["is_audio_out"], data["is_audio_out"])
            self.assertEqual(check_data["video_frame_rate"], data["video_frame_rate"])
            self.assertEqual(check_data["transcode_video_info"]["codec"], data["transcode_video_info"]["codec"])

    def test12_update_profile(self):
        """更新profile失败：profile_id不存在"""
        self.log.info(message="test11_update_profile", name="test03_ProcProfile.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[11])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[11])
        data = self.data.get_request_data(self.sheet, self.row[11])
        headers = self.hea_data.get_header(self.sheet, self.row[11])
        expect = self.data.get_expect_result(self.sheet, self.row[11])
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

    def test13_delete_profile(self):
        """删除profile"""
        self.log.info(message="test13_delete_profile", name="test03_ProcProfile.py", line=get_run_line())
        # 获取测试数据
        method = self.data.get_method(self.sheet, self.row[12])
        data = self.data.get_param(self.sheet, self.row[12])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[12]) + data
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

        # 检验profile是否删除
        if dict_json["status"]:
            check_data = self.check_profile()
            self.assertFalse(check_data["status"], msg="检验profile是否删除不通过")
            self.assertEqual(check_data["err"]["code"], 404)
            self.assertEqual(check_data["err"]["message"], "Record not found")

    def test14_delete_profile(self):
        """删除profile"""
        self.log.info(message="test14_delete_profile", name="test03_ProcProfile.py", line=get_run_line())
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
        self.assertFalse(dict_json["status"], msg=">>>断言失败，实际返回结果：%s" % dict_json)
        self.assertEqual(dict_json["err"]["code"], 404, msg='>>>断言失败，实际返回结果：%s' % dict_json["err"]["code"])
        self.assertEqual(dict_json["err"]["message"], "Profile doesn't exist",
                         msg='>>>断言失败，实际返回结果：%s' % dict_json["err"]["message"])

    def check_profile(self):
        method = self.data.get_method(self.sheet, self.row[8])
        data = self.data.get_param(self.sheet, self.row[8])
        url = self.config.get_base_url() + self.data.get_url(self.sheet, self.row[8]) + data
        headers = self.hea_data.get_header(self.sheet, self.row[8])
        # 发送请求
        status_code, res_json = self.http.http_method(method=method, url=url, headers=headers)
        dict_json = json.loads(res_json)  # 把json数据转换成字典对象
        return dict_json


if __name__ == "__main__":
    unittest.main()
