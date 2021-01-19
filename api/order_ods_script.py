# -*- coding: utf-8 -*-
import sys
sys.path.append("../")
from utility import (db_conn, common_time, common_encrypt, common_str)
from conf.host_conf import (HostUrl)
import requests

# 查询订单部分发货的数量
# 参数 order 子单编号 R1********，暂不支持 R3 R4 R5 订单拆单
def order_out_detail(order:str):
    # 根据订单查询出库单状态
    in_param = {"order": order}
    df = db_conn.run_sql("selectSmOrder", "ruigucrmdev_sql", in_param)
    assert len(df) == 1, order + ": 未关联有效的出库单"
    sm_order = df["smOrderId"][0]
    # 调用 MP 接口，查询部分出库状态
    url = HostUrl.host_erpapi + "/dc/get_sm_order_out_detail"
    headers = {"Content-Type": "application/json"}
    timestamp = common_time.get_timestamp()
    sign = common_encrypt.get_erpsign(["RUIGU_FIN", str(timestamp), 
         "8f60c8102d29fcd525162d02eed4566b", "111111"])
    data = {"signature": sign,
            "timestamp": timestamp,
            "nonce": "111111",
            "key": "RUIGU_FIN",
            "sm_order": sm_order}
    response = requests.post(url=url, json=data, headers=headers)
    assert response.status_code == 200, "服务请求失败"
    print(response.json())

# 查询ODS出库单，区分原装、非原装
# 参数 子单号 R1********
def ods_sm_order(order:str):
    # 根据订单查询出库单状态
    in_param = {"order": order}
    df = db_conn.run_sql("selectSmOrder", "ruigucrmdev_sql", in_param)
    assert len(df) == 1, order + ": 未关联有效的出库单"
    sm_order = df["ruiguSmOrderId"][0]
    # print(sm_order)
    # 根据出库单查询ODS单据
    df = db_conn.run_sql("selectOutBound", "bulldozer_sql",
                          {"sm_order": sm_order})
    assert len(df) > 0, "未找到关联的 ODS 出库单"
    # # 查询出库单关联的SKU
    for i in range(len(df)):
        out_bound = df["outbound_no"][i]
        out_bound_state = df["state"][i]
        # print(out_bound)
        dr = db_conn.run_sql("selectOutBoundSku", "bulldozer_sql",
                              {"outbound_no": out_bound})
        print(out_bound + " " + str(out_bound_state))
        for j in range(len(dr)):
            print("  " + dr["sku_code"][j] + ":" + 
                  str(dr["quantity"][j]) + ":" + str(dr["sent_quantity"][j]))

# 模拟ODS订单部分发货
# 参数 ODS 出库单号 WOO******
def woo_order_send(out_bound:str, s_type):
    url = HostUrl.host_nagy + "/bulldozer/test/outboundOrderSent"
    data = {"outboundOrderNo": out_bound,
            "fullSent": s_type, # 0 部分发货 1 全部发货
            "access_token": "sjdadjhdjakslf2oj832rfnf49urnfu4r823jifj092"}
    url = url + "?" + common_str.dict_str(data)
    reponse = requests.get(url=url)
    assert reponse.status_code == 200, "服务请求失败"
    print(reponse.json())

# 模拟ODS订单部分发货
# 参数 自营的子单号 R1********
def saleorder_send(order:str, s_type):
    # 根据订单查询出库单状态
    in_param = {"order": order}
    df = db_conn.run_sql("selectSmOrder", "ruigucrmdev_sql", in_param)
    assert len(df) == 1, order + ": 未关联有效的出库单"
    sm_order = df["smOrderId"][0]
    print(sm_order)
    # 根据出库单查询ODS单据
    df = db_conn.run_sql("selectOutBound", "bulldozer_sql",
                          {"sm_order": sm_order})
    print(df)
    assert len(df) == 1, "订单尚未拣货"
    out_bound = df["outbound_no"][0]
    # 模拟 ODS 部分发货场景
    url = HostUrl.host_nagy + "/bulldozer/test/outboundOrderSent"
    data = {"outboundOrderNo": out_bound,
            "fullSent": s_type, # 0 部分发货 1 全部发货
            "access_token": "sjdadjhdjakslf2oj832rfnf49urnfu4r823jifj092"}
    url = url + "?" + common_str.dict_str(data)
    reponse = requests.get(url=url)
    assert reponse.status_code == 200, "服务请求失败"
    print(reponse.json())

# 查询自营订单ODS出库明细
# order_out_detail("R120120162937001")
# 查询 ODS 出库单
# ods_sm_order("CUM202012151725280001000013") # 参数 销售单或领用单
# 模拟ODS发货
# saleorder_send("R120121555489001", 0) # 参数 销售单、发货方式（1 全部发货 0 部分发货）
woo_order_send("WOO202012151744564960000002", 1) # 参数 WOO单，发货方式，全部和部分