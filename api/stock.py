# -*- coding: utf-8 -*-
import sys
sys.path.append("../")
from conf.host_conf import HostUrl
from utility import (redis_conn)
import requests
import json


# 设置商品的库存
# 入参，分别为 商品编码、仓库ID、库存数量
# in_param = {"263725633", 455, 80}
def set_stock(sku_code:str, storage_id:int, num:int):
    url = HostUrl.host_stock + "/stock/setStockCount"
    headers = {"Content-Type": "application/json"}
    # 连接 REDIS，查询库存类型
    stock_type = redis_conn.redis_get("redis_246", 
           "hget Stock-Service:goods:storage:stockType " + str(storage_id))
    data = [{"sku_code": sku_code,
            "count": num,
            "stock_type": stock_type,
            "storage_id": storage_id}]
    print(json.dumps(data))
    response = requests.post(url=url, data=json.dumps(data), headers=headers)
    assert response.status_code == 200, "服务请求报错"
    # print(response.json())
    return response.json()

set_stock("263703404", 455, 100)