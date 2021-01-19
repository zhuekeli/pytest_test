# -*- coding: utf-8 -*-
import pytest
import sys
import json
sys.path.append("../")
from api import (login, sku, order_create, cart, stock)

# 全局变量
user = {"mname": "cjz", "password": "1"}
lisku = [
{"sku_code": "140210488", "dealer_id": 455},
{"sku_code": "252231377", "dealer_id": 455}]
create_token = "" # 订单预检接口返回 TOKEN
order_number = "" # 创建订单对应的主单号 R0   

@pytest.fixture()
def test_setup():
    print("开始执行用例： 创建商城订单")

# 用户登录
@pytest.mark.usefixtures("test_setup")
def test_userlogin():
    # 初始化用户、密码
    print("地推B端用户登录 " + "user=" + user["mname"] + ", password=" + user["password"])
    userinfo = login.user_login(user)
    for key in userinfo.keys():
        user[key] = userinfo[key]
    assert isinstance(userinfo, dict), "用户登录失败"
    print(user)

# 查找商品
@pytest.mark.dependency("test_userlogin")
def test_skuinfo():
    for i in range(len(lisku)):
        # 商品搜索，返回商品ID 起订量等
        sku_code = lisku[i]["sku_code"]
        response = sku.sku_plist(sku_code, user)
        assert len(response["data"]) == 1, "未找到商品 " + sku_code
        lisku[i]["goods_id"] = response["data"][0]["goods_id"]
        lisku[i]["min_order"] = response["data"][0]["min_order"]
    print(json.dumps(lisku))   

# 设置库存
@pytest.mark.dependency("test_skuinfo")
def test_skustock():
    for i in range(len(lisku)):
        response = stock.set_stock(lisku[i]["sku_code"], lisku[i]["dealer_id"], 1000)
        print(response)
        assert response["code"] == 200, lisku["sku_code"] + " 库存设置失败"

# 商品添加购物车
@pytest.mark.dependency("test_skustock")
def test_addcart():
    for i in range(len(lisku)):
       response = cart.cart_add(lisku[i], user)
       # print(response)
       assert response["code"] == 200, "商品添加购物车失败"

# 预检接口
@pytest.mark.dependency("test_addcart")
def test_precreate():
    response = order_create.pre_create(lisku, user)
    assert response["code"] == 200, "订单预检失败"
    global create_token
    create_token = response["data"]["create_token"]
    assert len(create_token) > 0, "预检接口请求失败"

# 创建订单
@pytest.mark.dependency("test_precreate")
def test_create():
    response = order_create.create(create_token, user)
    assert response["code"] == 200, "订单创建失败"
    global order_number
    order_number = response["data"]["order_number"]
    assert len(order_number) > 0, "订单创建失败，未返回订单号"
    print("order_number: " + order_number)

# 推送订单
@pytest.mark.dependency("test_create")
def test_pollingorder():
    response = order_create.polling(order_number, user)
    assert response["code"] == 200, "订单推送失败"

if __name__ == '__main__':
    pytest.main(["-s", "test_order.py"])
    
    
    
