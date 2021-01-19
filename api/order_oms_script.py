# -*- coding: utf-8 -*-
import sys
import requests
sys.path.append('../')
from conf.host_conf import HostUrl
from utility import db_conn

# 修改订单的支付时间，自动审核
# 参数 {"order": "R120112557940001"} order 主单号 R0 或 子单号 RX
def order_audit(order:str):
    # 查询符合条件的子单 订单状态 2
    df = db_conn.run_sql("selectSubOrder", "ruigucrmdev_sql", 
                         {"order": order})
    for i in range(len(df)):
        if df["orderStatus"][i] == 2:
            # print(df["orderNumber"][i])
            # 修改订单的支付时间 15分钟以前
            db_conn.run_sql("updateOdPayTime", "ruigucrmdev_sql",
                            {"order": df["orderNumber"][i]})
            # 执行脚本审核订单
            url = HostUrl.host_api + "/v0.2/order/order_auto_pass"
            data = {"ordernumber": df["orderNumber"][i],
                    "rg_id": "web",
                    "rg_ver": 9999}
            response = requests.post(url=url, data=data)
            assert response.status_code == 200, "服务请求失败"
            print(response.json())


# 订单状态 正在发货 -> 已发货 物流配送
def order_common(order:str, script_param:str):    
    if script_param == "order_auto_send":
        # 查询符合条件的子单 订单状态 4 已发货
        df = db_conn.run_sql("selectSubOrder", "ruigucrmdev_sql", 
                         {"order": order})
        if len(df) == 1 and df["orderStatus"][0] == 3:
            url = HostUrl.host_api + "/v0.2/script/" + script_param
            response = requests.get(url)
            assert response.status_code == 200, "服务请求失败"
            # 执行脚本后，查询数据库订单状态 更新为 5
            dr = db_conn.run_sql("selectSubOrder", "ruigucrmdev_sql", 
                                  {"order": order})
            assert dr["orderStatus"] == 4, "订单状态更新失败 正在发货 -> 已发货"
        else:
            print("未找到正在发货的订单")
         
            
# 订单状态 已发货 -> 已收货 仅针对物流配送
# 参数 {"order": "R120112557940001"} order 主单号 R0 或 子单号 RX
def order_receive(order:str):
    # 查询符合条件的子单 订单状态 4 已发货
    df = db_conn.run_sql("selectSubOrder", "ruigucrmdev_sql", 
                         {"order": order})
    # print(df)
    for i in range(len(df)):
        if df["orderStatus"][i] == 4 and df["deliverType"][i] == 0:   # 订单状态 已收货
            print(df["orderNumber"][i] + " status=" + str(df["orderStatus"][i]))
            # 执行脚本审核订单
            url = HostUrl.host_api + "/v0.2/dev/shipped_to_receiving"
            data = {"orderNumber": df["orderNumber"][i],
                    "rg_id": "web",
                    "rg_ver": 9999,
                    "secret": "193EC93593CF2FA40BC9C2BF57D75732",
                    "third_flag": "false",
                    "coins_flag": "false"}
            response = requests.post(url=url, data=data)
            assert response.status_code == 200, "服务请求失败"
            # 查询数据库订单状态 5 已收货
            dr = db_conn.run_sql("selectSubOrder", "ruigucrmdev_sql", 
                         {"order": order})
            assert dr["orderStatus"][i] == 5, "订单状态更新失败"

# 订单状态 已收货 -> 已完成
# 参数 {"order": "R120112557940001"} order 主单号 R0 或 子单号 RX
def order_finish(order:str):
    # 查询符合条件的子单 订单状态 5 已收货
    df = db_conn.run_sql("selectSubOrder", "ruigucrmdev_sql", 
                         {"order": order})
    for i in range(len(df)):
        if df["orderStatus"][i] == 5:   # 订单状态 已收货
            print(df["orderNumber"][i])
            # 修改订单的收货时间 7 天之前
            db_conn.run_sql("updateOdReceiveTime", "ruigucrmdev_sql",
                            {"order": df["orderNumber"][i]})
            # 执行脚本审核订单
            url = HostUrl.host_api + "/v0.2/script/order_auto_accomplish"
            data = {"orderNumber": df["tms_order"][i],
                    "rg_id": "web",
                    "rg_ver": 9999}
            response = requests.post(url=url, data=data)
            assert response.status_code == 200, "服务请求失败"
            print(response.json())
            return response.json()
            
##########################################################################
# 订单状态 已付款 -> 已审核 自动审核
# order_audit("R120120469767001")

# 订单正发货 -> 已发货（物流配送订单）
# order_common("R120121454594001", "order_auto_send")

# 订单已发货 -> 已收货（物流配送订单）
order_receive("R120121454594001")

# 订单已收货 -> 已完成（收货7天，脚本更新订单状态）
# order_finish("R120120153805001")
