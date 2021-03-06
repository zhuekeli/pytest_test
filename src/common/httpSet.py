#!/usr/bin/python3
# coding=utf-8
import json
import requests

false = False
true = True


class HttpMethod:
    def __init__(self):
        self.log = Logger()

    def get_method(self, url, data=None, headers=None):
        try:
            res = requests.get(url=url, params=data, headers=headers)
            status_code = res.status_code
            res_json = res.json()
            return status_code, res_json  # 返回响应码，响应内容
        except Exception as e:
            self.log.error("Error:%s" % e)

    def post_method(self, url, files=None, data=None, headers=None):
        try:
            if files:
                res = requests.post(url=url, files=files, data=data, headers=headers)
            else:
                res = requests.post(url=url, data=json.dumps(data), headers=headers)
            status_code = res.status_code
            res_json = res.json()
            return status_code, res_json  # 返回响应码，响应内容
        except Exception as e:
            self.log.error("Error:%s" % e)

    def put_method(self, url, data=None, headers=None):
        try:
            res = requests.put(url=url, data=json.dumps(data), headers=headers)
            status_code = res.status_code
            res_json = res.json()
            return status_code, res_json  # 返回响应码，响应内容
        except Exception as e:
            self.log.error("Error:%s" % e)

    def delete_method(self, url, data=None, headers=None):
        try:
            res = requests.delete(url=url, data=json.dumps(data), headers=headers)
            status_code = res.status_code
            res_json = res.json()
            return status_code, res_json  # 返回响应码，响应内容
        except Exception as e:
            self.log.error("Error:%s" % e)

    def http_method(self, method, url, files=None, data=None, headers=None):
        """判断请求方法
        :param method: 请求方法
        :param url: 接口路径
        :param data: 请求数据
        :param headers: 请求头
        :return:
        """
        if method == 'get':
            status_code, res_json = self.get_method(url, data, headers)
        elif method == 'post':
            status_code, res_json = self.post_method(url, files, data, headers)
        elif method == 'put':
            status_code, res_json = self.put_method(url, data, headers)
        else:
            status_code, res_json = self.delete_method(url, data, headers)
        return status_code, json.dumps(res_json, ensure_ascii=False, sort_keys=False, indent=2)  # 对json数据进行格式化输出


if __name__ == "__main__":
    file_path = "../source/sample.mp4"
    h = HttpMethod()
    url = "http://172.16.1.201:3002/library/upload"
    data = {"type": "video", "source_file_id": "5d37ca73aeaa1fd50328bf93", "language": "ENG"}
    file = {"file": ("sample.mp4", open(file_path, 'rb'), "video/mp4")}
    print(file)
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1ZDM3YzUyOGFlYWExZmQ1MDMyOGJlZmUiLCJhdWQiOiJQYW5lbCIsImlzcyI6IlBhbmVsIiwidGVuYW50IjoiYXV0b190ZW5hbnRfbmFtZSIsImlhdCI6MTU2MzkzNzM3OSwiZXhwIjoxNTk1NDk0OTc5fQ.7RkYuCCheuScVILo_hoCHoRo-5BaYokq2PVlx5ama2M"}
    status_code, res_json = h.post_method(url=url, files=file, data=data, headers=headers)
    print(status_code)
    print(res_json)
