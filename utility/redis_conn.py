# -*- coding: utf-8 -*-
import sys
sys.path.append("../")
import configparser
import redis


def redis_con(conf:str):
    cf = configparser.ConfigParser()
    cf.read(r"../conf/redis_conf.ini")
    host = cf.get(conf, "host")
    port = cf.get(conf, "port")
    if cf.has_option(conf, "password"):
        password = cf.get(conf, "password")
        conn = redis.Redis(host=host, port=port, password=password, 
                            decode_responses=True)
        
    else:
        conn = redis.Redis(host=host, port=port, decode_responses=True)
    return conn

      
def redis_get(conf:str, command:str):
    conn = redis_con(conf)
    if command.startswith("hget"):
        command = command.replace("hget", "").strip()
        key = command[0 : command.find(" ")]
        value = command[command.find(" ") + 1 : len(command)]
        # print(key + ":" + str(value))
        return conn.hget(name=key, key=value)
    elif command.startswith("get"):
        key = command.replace("get", "").strip()
        # print(key)
        return conn.get(key)
    elif command.startswith("hgetall"):
        key = command.replace("hgetall", "").strip()
        return conn.hgetall(key)
   
def redis_del(conf:str, command:str):
    conn = redis_con(conf)
    if command.startswith("hdel"):
       command = command.replace("hdel", "").strip()
       key = command[0 : command.find(" ")]
       field = command[command.find(" ") + 1 : len(command)]
       # print(key + ":" + field)
       return conn.hdel(key, field)
    elif command.startswith("del"):
        command = command.replace("del","").strip()
        key = command[command.find(" ") + 1 : len(command)] 
        #print(key)
        return conn.delete(key)

    
print(redis_get("redis_246", "hget Stock-Service:goods:storage:stockType 455"))