# -*- coding: utf-8 -*-
import sys
import requests
sys.path.append("../")
from conf.host_conf import (HostUrl)
from utility import (common_encrypt, common_time, common_str)
import jsonpath

def user_login(in_param:dict):
    mname    = in_param["mname"]
    password = in_param["password"]
    
    # 获取 access_token
    url = HostUrl.host_auth + '/authorization/gettoken'
    data = {'_client_tag': 'ruigushop',
          '_client_type': 'ios',
          '_client_uuid': 'C859FF66-822F-4AC6-8D4E-C179CA9AEBC7',
          '_client_version': '2.1.6',
          '_sign_once': common_time.get_timestamp(),
          'rg_id': 'web',
          'rg_ver': 9999}
    response = requests.post(url=url, data=common_encrypt.get_sign(data))
    assert response.status_code == 200, "服务请求失败"
    access_token = response.json()['data']['access_token']


    # 登录
    headers = {"authorization": str(access_token)}
    di = {'_sign_once': common_time.get_timestamp(),
          'lat': '31.335251', 
          'lng': '121.515155',
          'mobile': mname,
          'password': password,
          'net': 'WIFI',
          'operator': 'China Unicom',
          'rg_id': 'web',
          'rg_ver': 9999}
    url = HostUrl.host_gate + '/api-service/v0.2/new_login'
    # print(url)
    # print(common_encrypt.get_sign(di))
    response = requests.post(url=url, data=common_encrypt.get_sign(di), headers=headers)
    # print(response.json())
    assert response.status_code == 200, "服务请求失败"
    assert response.json()['code'] == 200, 'new_login 请求失败'
    out_param = {"mname": in_param["mname"],
                 "user_id": response.json()['data']['user_info']['id'],
                 "token": response.json()['data']['user_info']['token'],
                 "access_token": response.json()['data']['token_info']['access_token'],
                 "customer_type": response.json()['data']['user_info']['customer_type']}
    return out_param

def mp_login(user:str, password:str):
    url = HostUrl.host_erpweb + "/nologin/do_login"
    data = {"username": user, "password": password, "image_captcha": 1}
    response = requests.post(url=url, data=data)
    assert response.status_code == 200, "服务请求失败"
    assert response.json()["code"] == 200, "MP 登录失败"
    return response.headers.get("Set-Cookie")
     
print(user_login({"mname": "cjz", "password": "1"}))
# mp_login("admin", "Ruigushop@1")