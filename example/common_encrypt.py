# -*- coding: utf-8 -*-
import base64
import hashlib


# sha1 签名
def get_sha1(param: str):
    param = param + '&secret=Ruigu#Secert@!Info'
    sha = hashlib.sha1(param.encode('utf-8'))
    encrypts = sha.hexdigest()
    return encrypts


# base64
def get_base64(param: str):
    encrypts = base64.b64encode(param.encode("utf-8"))
    data = str(encrypts)[2:-1]
    return data


# MD5
def get_md5(param: str):
    param = param.encode("utf-8")
    m = hashlib.md5()
    m.update(param)
    return m.hexdigest()


# 获取签名
def get_sign(param: dict):
    data = ''
    for key in sorted(param.keys()):
        data += key + '=' + str(param[key]) + '&'
    if len(data) > 0:
        data = data[0:-1]
    # print(data)
    param['_sign'] = get_base64(get_sha1(data))
    return param


# MP签名
def get_erpsign(param: list):
    # list 排序
    # sparam = [str(x) for x in param]
    param = sorted(param)
    data = "".join(param)
    return get_md5(data)
