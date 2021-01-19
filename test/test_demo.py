# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 18:24:12 2020

@author: caojinzhu
"""

import sys
import requests
sys.path.append('../')
from utility import (common_str, commom_time, common_encrypt, db_conn)
from conf.host_conf import HostUrl 

# print (commom_time.get_timestamp())
# print (commom_time.get_timestamp('2020-11-16 22:00:00'))

# print(common_str.dict_str(data))
# print(common_encrypt.get_sha1(common_str.dict_str(data)))
# _sign = common_encrypt.get_base64(common_encrypt.get_sha1(common_str.dict_sortstr(data)))
# data['_sign'] = str(_sign)
# print(common_str.dict_str(data))

# 获取 access_token
url = HostUrl.host_auth + '/authorization/gettoken'
data = {'_client_tag': 'ruigushop',
      '_client_type': 'ios',
      '_client_uuid': 'C859FF66-822F-4AC6-8D4E-C179CA9AEBC7',
      '_client_version': '2.1.6',
      '_sign_once': commom_time.get_timestamp(),
      'rg_id': 'web',
      'rg_ver': 9999}
response = requests.post(url=url, data=common_encrypt.get_sign(data))
assert response.status_code == 200, 'Response Code: ' + str(response.status_code)
access_token = response.json()['data']['access_token']
print("access_token = " + str(access_token))

# 登录
headers = {"authorization": str(access_token)}
di = {'_sign_once': commom_time.get_timestamp(),
      'lat': '31.335251', 
      'lng': '121.515155',
      'mobile': 'cjz',
      'password': '1',
      'net': 'WIFI',
      'operator': 'China Unicom',
      'rg_id': 'web',
      'rg_ver': 9999}
url = HostUrl.host_gate + '/api-service/v0.2/new_login'
print(url)
# print(common_encrypt.get_sign(di))
response = requests.post(url=url, data=common_encrypt.get_sign(di), headers=headers)
print(response.json())
assert response.json()['code'] == 200, 'new_login 请求失败'
if response.json()['code'] == 200:
    api_return_token = response.json()['data']['user_info']['token']
# 查询数据库获取 TOKEN
dict_param = {'mname': 'cjz'}
df = db_conn.run_sql('selectTokenByMname', 'ruigucrmdev_sql', dict_param)
assert len(df) > 0
if len(df) > 0:
    # print(str(df.iloc[0]) + '\n' + str(df[df.columns[1]][0]))
    db_return_token = str(df[df.columns[1]][0])
# print(str(api_return_token) + "\n" + str(db_return_token))
assert api_return_token != db_return_token, '接口和数据库的数据不一致'

# 
