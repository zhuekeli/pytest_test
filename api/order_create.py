# -*- coding: utf-8 -*-
import sys
sys.path.append("../")
from conf.host_conf import HostUrl
from utility import (common_time, common_encrypt, common_str)
import requests
import json

# 预检接口
def pre_create(lisku:list, user:dict):
    url = HostUrl.host_gate + "/order-service/order/preCreate"
    headers = {"authorization": user["access_token"]}
    # 拼接预检的商品数
    goods = []
    for i in range(len(    )):
        di_good = {"goods_id": lisku[i]["goods_id"], 
                   "count": lisku[i]["min_order"]}
        goods.append(di_good)
    data = {"rg_ver": 9999,
            "rg_id": "web",
            "order_type": "4",
            "operator": "China Unicom",
            "net": "WIFI",
            "lng": "4.9E-324",
            "lat": "4.9E-324",
            "goods": json.dumps(goods),
            "coupon_version": "2",
            "additional_param": "",
            "_sign_once": common_time.get_timestamp()
            }
    response = requests.post(url=url, data=common_encrypt.get_sign(data), headers=headers)
    # print(response.status_code)
    assert response.status_code == 200, "服务请求失败"
    return response.json()

# 创建订单
def create(create_token:str, user:dict):
    url = HostUrl.host_gate + "/order-service/order/create"
    headers = {"authorization": user["access_token"]}
    data = {"rg_ver": 9999,
            "rg_id": "web",
            "operator": "China Unicom",
            "net": "WIFI",
            "lng": "4.9E-324",
            "lat": "4.9E-324",
            "delivery_time": "2020-12-06",
            "create_token": create_token,
            "additional_param": "",
            "_sign_once": common_time.get_timestamp()}
    # print(common_encrypt.get_sign(data))
    response = requests.post(url=url, data=common_encrypt.get_sign(data), headers=headers)
    assert response.status_code == 200, "服务请求失败"
    print(response.json())
    return response.json()

# 推送订单
def polling(order_number:str, user:dict):
    url = HostUrl.host_gate + "/order-service/pay/pollingOrder"
    headers = {"authorization": user["access_token"]}
    data = {"rg_ver": 9999,
            "rg_id": "web",
            "order_no": order_number,
            "operator": "China Unicom",
            "net": "WIFI",
            "lng": "4.9E-324",
            "lat": "4.9E-324",
            "_sign_once": common_time.get_timestamp()}
    response = requests.post(url=url, data=common_encrypt.get_sign(data), headers=headers)
    assert response.status_code == 200, "服务请求失败"
    print(response.json())
    return response.json()
    
# create("123", "123")