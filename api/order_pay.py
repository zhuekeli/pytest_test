# -*- coding: utf-8 -*-
import sys
sys.path.append("../")
from utility import (db_conn, common_time)
from conf.host_conf import HostUrl
import requests

# 订单支付
# 参数 订单号 R1****** 或 主单号 R0******
# 参数 支付渠道 1 支付宝 2 微信 3 银联 6 余额 7 白条 10 富条
def sellorder(order:str, pay_type:int):
    # 查询订单状态
    df = db_conn.run_sql("selectSubOrder", "ruigucrmdev_sql", {"order": order})
    # 订单未付款
    if len(df) == 1 and df["orderStatus"][0] == 1:
        # 查询订单待支付金额
        main_order = df["os_main_order_number"][0]
        df = db_conn.run_sql("selectPaidMoney", "orderdb_sql", {"order": main_order})
        total_money = df["payMoney"][0]
        url = HostUrl.host_order + "/pay/payNewCallback"
        data = {"order_no": main_order,
                "total_money": total_money,
                "trade_no": "PAY" + str(common_time.get_timestamp()),
                "pay_type": pay_type,
                "pay_no": main_order,
                "pay_account": 2}
        response = requests.post(url=url, data=data)
        assert response.status_code == 200, "服务请求失败"
        # print(response.json())
        return response.json()
        

# 配件支付

sellorder("R120120775401001", 6)