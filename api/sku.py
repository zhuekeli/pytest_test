# -*- coding: utf-8 -*-
import sys
import requests
sys.path.append("../")
from conf.host_conf import HostUrl
from utility import (common_str)

# 商品搜索，返回商品详情信息
def sku_plist(sku_code:str, user:dict):
    url = HostUrl.host_node + "/goods/plist"
    data = {"user_id": user["user_id"],
            "token": user["token"],
            "ordertype": user["customer_type"],
            "entityType": "1",
            "order": 1,
            "page": 1,
            "pagesize": 20,
            "province_code": "",
            "region_code": "",
            "city_code": "",
            "search_name": sku_code,
            "rg_ver": 9999,
            "rg_id": "web"}
    response = requests.post(url=url, data=data)
    assert response.status_code == 200, "服务请求失败"
    assert response.json()["code"] == 200
    return response.json()