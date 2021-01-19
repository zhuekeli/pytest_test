# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 18:09:29 2020

@author: caojinzhu
"""

import datetime
import time


# 时间 -> 时间戳
# param 入参为空，返回当前时间的时间戳，否则返回指定时间的时间戳
def get_timestamp(param=None): 
    if param == None:
        return int(time.time())
    else:
        return int(time.mktime(time.strptime(param, '%Y-%m-%d %H:%M:%S')))
    
# 时间戳 ->时间
# param 入参: 时间戳
def get_timefromstamp(param=None): 
    if param == None:
        param = time.time()
    # timeArray = time.localtime(int(param))
    return str(datetime.datetime.today())

# 获取当天时间 时分秒均为 0
def get_curdate():
    date_time = datetime.date.today()
    return datetime.datetime.strftime(date_time, "%Y-%m-%d %H:%M:%S")

# 获取当前的时间
def get_curtime():
     date_time = datetime.datetime.today()
     return datetime.datetime.strftime(date_time, "%Y-%m-%d %H:%M:%S")

# 获取当前日期 %Y-%m-%d
def get_curday():
     date_time = datetime.datetime.today()
     return datetime.datetime.strftime(date_time, "%Y-%m-%d")
 
# print(get_curdate())