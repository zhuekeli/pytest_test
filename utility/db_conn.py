    # -*- coding: utf-8 -*-
import sys
sys.path.append('../conf/sql')
sys.path.append('..')
from utility import common_str
import configparser
import pymysql
import pandas as pd

# 读取数据库配置
def get_dbconf(param=None):
    cf = configparser.ConfigParser()
    cf.read(r'..\conf\db_conf.ini')
    di = dict()
    di['host'] = cf.get(param, 'host')
    di['user'] = cf.get(param, 'user')
    di['password'] = cf.get(param, 'password')
    di['port'] = int(cf.get(param, 'port'))
    di['dbname'] = cf.get(param, 'db')
    return di

# 创建数据库连接 入参: 数据库连接名 如 mysql_ruigucrmdev
def get_condb(param=None):
    di_conf = get_dbconf(param)
    conn = pymysql.connect(
        host = di_conf['host'],
        port = di_conf['port'],
        user = di_conf['user'],
        password = di_conf['password'],
        db = di_conf['dbname'],
        charset = 'utf8'
        )
    return conn

# 执行SQL语句
def run_sql(sql_id=None, sql_path=None, dict_param=None):
    di_conf = __import__(sql_path).dict_sql
    conn = get_condb(di_conf[sql_id][0])
    # 获取执行的SQL语句
    sql_cmd = common_str.sql_cmd_replace(di_conf[sql_id][1].strip(), dict_param)
    if str(sql_cmd).upper().startswith('SELECT'):
        # print(sql_cmd)
        df = select_method(sql_cmd, conn)
        return df
    elif str(sql_cmd).upper().startswith('UPDATE'):
        update_method(sql_cmd, conn)
    elif str(sql_cmd).upper().startswith('INSERT'):
        insert_method(sql_cmd, conn)
    elif str(sql_cmd).upper().startswith('DELETE'):
        delete_method(sql_cmd, conn)
        
# 执行SELECT语句
def select_method(sql_cmd, conn):
    df = pd.read_sql(sql_cmd, conn)
    # 取第一行 第一列的数据
    # if len(df) > 0:
    #     print(str(df.iloc[0]) + '\n' + str(df[df.columns[0]][0]))
    return df

# 执行UPDATE语句
def update_method(sql_cmd, conn):
    try:
        cursor = conn.cursor()
        #print(sql_cmd)
        cursor.execute(sql_cmd)
        conn.commit()
        print('update ' + str(cursor.rowcount) + ' rows')
    except:
        conn.rollback()
        print('update fail')
    
    
# 执行INSERT语句
def insert_method(sql_cmd, conn):
    try:
        cursor = conn.cursor()
        #print(sql_cmd)
        cursor.execute(sql_cmd)
        conn.commit()
        print('insert ' + str(cursor.rowcount) + ' rows')
    except:
        conn.rollback()
        print('insert fail')

# 执行DELETE语句
def delete_method(sql_cmd, conn):
    try:
        cursor = conn.cursor()
        #print(sql_cmd)
        cursor.execute(sql_cmd)
        conn.commit()
        print('delete ' + str(cursor.rowcount) + ' rows')
    except:
        conn.rollback()
        print('delete fail')
        
        
# dict_param = {"num": 15, "order": "R120111763920001"}
# run_sql('updateOdPayTime', 'ruigucrmdev_sql', dict_param)

    