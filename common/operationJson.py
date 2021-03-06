#!/usr/bin/python3
# coding=utf-8
import json
import os

proDir = os.path.split(os.path.realpath(__file__))[0]
jsonPath = os.path.join(proDir, "../demo/resources/data.json")


class OperationJson:
    def __init__(self, file_name=None):
        if file_name:
            self.file_name = file_name
        else:
            self.file_name = jsonPath

    def open_json(self):
        """打开json文件
        :return:返回json文件数据
        """
        with open(self.file_name, 'r') as fp:
            data = json.load(fp)
            return data
            fp.close()

    def get_data(self, key):
        """通过key值获取数据
        :param key: 需要获取的值对应的key
        :return:
        """
        data = self.open_json()[key]
        return data

    def write_data(self, w_data, key1, key2=None):
        """修改json数据
        :param w_data: 修改后的数据
        :param key1: 要修改的键值1
        :param key2: 要修改的键值2
        :return:
        """
        data_dict = self.open_json()
        if key2 is None:
            data_dict[key1] = w_data
        else:
            data_dict[key1][key2] = w_data
        with open(self.file_name, 'w') as fp:
            fp.write(json.dumps(data_dict, ensure_ascii=False, sort_keys=False, indent=2))  # 对写入的json数据进行格式化
            fp.close()


if __name__ == "__main__":
    file_name = "../resources/content_vod.json"
    a = OperationJson()
    b = a.get_data("orc_token_header")
    print(type(b))
    print(b)
