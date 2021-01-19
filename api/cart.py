# -*- codi""ng: utf-8 -*-
import sys
import requests
sys.path.append('../')
from utility import (common_str, commom_time, common_encrypt, db_conn)
from conf.host_conf import (HostUrl)
from api.login import (user_login)
import json
import jsonpath

# 鋭锢商城 添加购物车商品
def cart_add(goods:dict, user:dict):
    url = HostUrl.host_gate + "/cart-service/external/goods/add"
    headers = {"authorization": user["access_token"]}
    data = {"rg_ver": 9999,
            "rg_id": "web",
            "order_type": user["customer_type"],
            "operator": "China Unicom",
            "num": goods["min_order"],
            "net": "WIFI",
            "lng": "121.515175",
            "lat": "31.335278",
            "group": "",
            "goods_id": goods["goods_id"],
            "_sign_once": commom_time.get_timestamp()}
    response = requests.post(url=url, data=common_encrypt.get_sign(data), headers=headers)
    assert response.status_code == 200, "服务请求失败"
    return response.json()

# 鋭锢商城 查询购物车商品
# 入参 in_param = {
#    "id": 4860,
#    "token": "******"}
def cart_list(in_param:dict):
    # 查询数据库 返回 order_type
    df = db_conn.run_sql("selectTokenById", "ruigucrmdev_sql", {"id": in_param["user_id"]})
    assert len(df) == 1, "数据库返回结果为空"
    # 查询购物车列表
    url = HostUrl.host_gate + "/cart-service/external/cart/list"
    headers = {"authorization": in_param["token"]}
    print(headers)
    data = {"_sign_once": commom_time.get_timestamp(),
            "lng": "121.515155",
            "user_id": df["id"][0],
            "net": "WIFI",
            "lat": "31.335251",
            "operator": "China Unicom",
            "group": 4,
            "ordertype": df["order_type"][0],
            "select_goods_ids": "",
            "rg_ver": 9999,
            "rg_id": "web"
            }
    url =  url + "?" + common_str.dict_str(common_encrypt.get_sign(data))
    response = requests.get(url=url, headers=headers)
    assert response.status_code == 200, "购物车列表查询失败"
    print(json.dumps(response.json()))
    li_cart_sku = jsonpath.jsonpath(response.json(),
       '''$..data.goods_data[?(@.group_type=="NORMAL")].goods_list[*].goods.id''')
    # print(li_cart_sku)
    return li_cart_sku

# 鋭锢商城，清空购物车商品
# 入参 in_param = {
#    "access_token": "******",
#    "goods_ids": "1,2,3,456"} 待删除的商品列表
def cart_remv(in_param:dict):
    url = HostUrl.host_gate + "/cart-service/external/goods/remove"
    headers = {"authorization": in_param["access_token"]}
    data = {"_sign_once": commom_time.get_timestamp(),
            "lng": "121.515155",
            "goods_ids": in_param['goods_ids'],
            "net": "WIFI",
            "lat": "31.335251",
            "operator": "China Unicom",
            "group": "",
            "rg_ver": 9999,
            "rg_id": "web"
            }
    response = requests.post(url=url, data=common_encrypt.get_sign(data), headers=headers)
    assert response.status_code == 200, "服务请求报错"
    print(response.json())

# 查询购物车商品
data = user_login({'mname': 'cjz', 'password': '1'})
print(data)
cart_data = {"user_id": data["user_id"],
             "token": data["access_token"]}
cart_goods_id = cart_list(cart_data)
if cart_goods_id:
    li_cart_sku = common_str.list_str(cart_goods_id, ',')
    cart_data = {"goods_ids": li_cart_sku,
                  "access_token": data["access_token"]}
    cart_remv(cart_data)

