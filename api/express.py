# -*- coding: utf-8 -*-
import sys
import requests
sys.path.append("../")
from utility import (common_time, db_conn)
from conf.host_conf import HostUrl

# 订单已发后，更新物流信息接口（运单号）
# 入参 in_param = {'order_number': 'R520102859534001'}
def update_express(in_param:dict):
    order_number = in_param["order_number"]
    # print(str(order_number))
    # 查询主单号
    df = db_conn.run_sql('selectMainByOrder', 'ruigucrmdev_sql',
                                 {'order': order_number})
    assert len(df) > 0, "数据库返回数据为空"
    if  df['orderStatus'][0] < 4:
        assert False, "订单状态" + str(df['orderStatus'][0]) + "不支持更新物流"
    assert len(df) == 1, "查询数据为空"
    # 更新订单的运单号
    express_no = "SF" + str(common_time.get_timestamp())
    url = HostUrl.host_api + "/v0.2/dealer/updateExpressNo"
    # print(url)
    data = {"main_order": df['os_main_order_number'][0],
            "express_no": express_no,
            "order_number": order_number,
            "express_code": 9999}
    response = requests.post(url=url, data=data)
    assert response.status_code == 200, "接口请求报错"
    assert response.json()['code'] == 200, "更新物流失败"
    print(response.json())
    # 查询数据库运单号
    df = db_conn.run_sql('selectExpressByOrder', 'ruigucrmdev_sql',
                                 {'order': order_number})
    assert len(df) == 1, "数据库物流查询失败"
    db_express_corp = df['express_corp'][0]
    db_express_no = df['express_no'][0]
    print(str(db_express_corp) + ", " + str(db_express_no))
    assert express_no == db_express_no, "接口更新物流单号失败，和数据库不一致"
    return response.json()

update_express({'order_number': 'R520102859534001'})
    

