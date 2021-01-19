# -*- coding: utf-8 -*-
import sys
import requests
sys.path.append('../')
from utility import (common_time, common_encrypt)
from api import (login)
from conf.host_conf import HostUrl
from utility import db_conn

# 创建出库单
# 参数 {"order": "R120112557940001"}
def createsmorder(order:str):
    # 查询订单的状态 正在发货
    df = db_conn.run_sql("selectSubOrder", "ruigucrmdev_sql", 
                         {"order": order})
    # print(df)
    # assert len(df) == 1 and df["orderStatus"][0] == 3, "订单状态错误"
    # 查询出库单状态
    df = db_conn.run_sql("selectSmOrder", "ruigucrmdev_sql",
                         {"order": order})
    if len(df) == 0:
        url = HostUrl.host_erpapi + "/dc/create_out_order"
        headers = {"Content-Type": "application/json"}
        timestamp = common_time.get_timestamp()
        sign = common_encrypt.get_erpsign(["RUIGU_FIN", str(timestamp), 
             "8f60c8102d29fcd525162d02eed4566b", "111111"])
        data = {"signature": sign,
                "timestamp": timestamp,
                "nonce": "111111",
                "key": "RUIGU_FIN",
                "order_number": order}
        response = requests.post(url=url, json=data, headers=headers)
        assert response.status_code == 200, "服务请求失败"
        print(response.json())
    else:
        print("已创建出库单 " + df["smOrderId"][0])

# 出库单推送 ODS
# 参数 {"order": "R120112557940001"}
def order_pushods(order:str):
    # 查询订单的状态 正在发货
    df = db_conn.run_sql("selectSubOrder", "ruigucrmdev_sql", 
                         {"order": order})
    # print(df)
    assert len(df) == 1 and df["orderStatus"][0] == 3, "OMS订单状态错误" # 订单状态正在发货
    # 查询出库单状态
    df = db_conn.run_sql("selectSmOrder", "ruigucrmdev_sql",
                         {"order": order})
    if len(df) == 1 and df["status"][0] == 0:
        # 修改 is_push_wms = 2 已推送 TMS 创建包裹不支持修改状态
        # db_conn.run_sql("", "updateSmOrderPushTMS", {"order": order})
        assert len(df) == 1 and df["is_push_wms"][0] == 2, "TMS回写状态错误" # TMS状态回调成功
        data = {"id": df["smOrderId"][0]}
        url = HostUrl.host_erpweb + "/warehouse/sent_notification"
        headers = {"Cookie": login.mp_login("admin", "Ruigushop@1")}
        response = requests.post(url=url, data=data, headers=headers)
        assert response.status_code == 200, "服务请求失败"
        print(response.text)
    else:
        print("出库单已推送 ODS " + str(df["status"][0]))
    
# 出库单推TMS，模拟定时任务（每隔2分钟）执行
def push_tms():
    url = HostUrl.host_erpweb + "/sys_monitor/start_manual"
    headers= {"Cookie": login.mp_login("admin", "Ruigushop@1")}
    data = {"task_name": "app\Console\Tasks\PushTmsSmOrderTask"}
    response = requests.post(url=url, data=data, headers=headers)
    print(response.status_code)
    assert response.status_code == 200, "服务请求失败"
   
# 创建出库单
# createsmorder("R120121157650001")

# 推送 TMS
# push_tms()

# 推送出库单
order_pushods("R120121157650001")