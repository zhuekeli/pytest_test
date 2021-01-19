# -*- coding: utf-8 -*-
import sys
sys.path.append("../")
from conf.host_conf import HostUrl
from utility import (db_conn, common_time)
import json
import requests

# 模拟订单的包裹发货，商品累计发货数量 <= 订单数量
# 参数 order 销售单 goods = {"263706920": "1", "263706921": "3"}
def create_package(order:str, goods:dict):
    # 根据销售单查询MP出库单号
    df = db_conn.run_sql("selectSmOrder", "ruigucrmdev_sql", {"order": order})
    if len(df) == 1:
        # 出库单
        sm_order = df["ruiguSmOrderId"][0]
        # 包裹对应商品信息，生成数据
        li_goods = []
        print(sm_order)
        for k in goods.keys():
            di_good = {"sku": k, "number": goods[k]}
            li_goods.append(di_good)
        print(li_goods)
        url = HostUrl.host_nagy + "/cheetah-transport/express/createPackage"
        url = url + "?access_token=sjdadjhdjakslf2oj832rfnf49urnfu4r823jifj092"
        headers = {"Content-Type": "application/json"}
        data = {"orderNumber": df["tms_order"][0],
                "smOrder": sm_order,
                "provider": "SDT",     # 德邦不支持合单发运
                "receiveProvince": "",
                "receiveCity": "",
                "receiveRegion": "",
                "sendProvince": "",
                "sendCity": "",
                "sendRegion": "",
                "boxCode": 'PK' + str(common_time.get_timestamp()),
                "boxSign": "1",
                "tailBoxSign": "1",
                "weight": "10",
                "volume": "1.5",
                "goodInfo": li_goods}
        print(url)
        print(data)
        response = requests.post(url=url, json=data, headers=headers)
        print(response.status_code)
        assert response.status_code == 200, "服务请求失败"
        print(response.text)

# 订单包裹发货，原箱 WOO单 -> 单个SKU 一个包裹
# 订单包裹发货，非原 WOO单 -> 多个SKU 一个或多个包裹
goods = {"140210488": "2", "140320523": "4"}
create_package("R120121441737001", goods)
