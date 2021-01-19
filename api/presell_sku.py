# -*- coding: utf-8 -*-
import sys
sys.path.append("../")
from conf.host_conf import HostUrl
from utility import (db_conn, common_time)
import requests

# 设置预售商品
def start(sku_code:str, warehouse:str):
    url = HostUrl.host_nagy + "/bulldozer/sync/pre-sale"
    url = url + "?" + "access_token=sjdadjhdjakslf2oj832rfnf49urnfu4r823jifj092"
    headers = {"Content-Type": "application/json"}
    data = {"applyId": "apply" + str(common_time.get_timestamp()),
            "quantity": 0,
            "skuCode": sku_code,
            "startTime": common_time.get_curdate(),
            "status": 1,
            "version": "version" + str(common_time.get_timestamp()),
            "warehouseCode": warehouse
            }
    print("version = " + data["version"])
    response = requests.post(url=url, json=data, headers=headers)
    assert response.status_code == 200, "服务请求失败"
    print(response.text)

# 关闭预售商品
def close(sku_code:str):
    # 查询商品对应的版本号
    df = db_conn.run_sql("selectPresaleStock", "bulldozer_sql", {"sku_code": sku_code})
    print(df)
    for i in range(len(df)):
        # 关闭预售商品
        url = HostUrl.host_nagy + "/bulldozer/sync/wms/put-storage"
        url = url + "?" + "access_token=sjdadjhdjakslf2oj832rfnf49urnfu4r823jifj092"
        headers = {"Content-Type": "application/json"}
        data = {"associatedNo": "apply" + str(common_time.get_timestamp()),
                "preSaleBeginTime": str(df["start_pre_Time"][i]),
                "preSaleEndTime": common_time.get_curtime(),
                "preSaleStatus": 0,
                "skuCode": sku_code,
                "stockQuantity": 0,
                "version": df["version"][0],
                "warehouseCode": df["warehouse_code"][i]
                }
        print(data)
        response = requests.post(url=url, json=data, headers=headers)
        assert response.status_code == 200, "服务请求失败"
        print(response.text)

# 推送预售订单 模拟 JOB 执行
def presell_push_ods():
    # 填充预售订单定时任务
    url = HostUrl.host_nagy + "/bulldozer/sync/fill-order-quantity"
    url = url + "?" + "access_token=sjdadjhdjakslf2oj832rfnf49urnfu4r823jifj092"
    headers = {"Content-Type": "application/json"}
    data = {}
    response = requests.post(url=url, json=data, headers=headers)
    assert response.status_code == 200, "服务请求失败"
    print(response.text)
    # 推送预售订单定时任务
    url = HostUrl.host_nagy + "/bulldozer/schedule/reProcessReadyDelayOrder"
    url = url + "?" + "access_token=sjdadjhdjakslf2oj832rfnf49urnfu4r823jifj092"
    response = requests.get(url=url)
    assert response.status_code == 200, "服务请求失败"
    print(response.text)

# 现货商品推送 ODS
def push_ods():
    # 推送预售订单定时任务
    url = HostUrl.host_nagy + "/bulldozer/schedule/reProcessReadyDelayOrder"
    url = url + "?" + "access_token=sjdadjhdjakslf2oj832rfnf49urnfu4r823jifj092"
    response = requests.get(url=url)
    assert response.status_code == 200, "服务请求失败"
    print(response.text)
    
# 设置预售商品
# start("261511010", "RG01")
# 关闭预售商品
# close("140320523")
# 推送预售订单
presell_push_ods()
# 推送现货订单
# push_ods() 