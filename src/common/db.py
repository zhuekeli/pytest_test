import logging

import pymysql

from src.config.readConfig import ReadConfig

"""
mysql 工具类

"""

logger = logging.getLogger(__name__)
load_config = ReadConfig()


class DbUtil(object):
    """mysql util"""

    def __init__(self, database: str):
        self.host = load_config.get_value('DB', 'host')
        self.port = int(load_config.get_value('DB', 'port'))
        self.database = database
        self.password = load_config.get_value('DB', 'password')
        self.username = load_config.get_value('DB', 'username')
        self.charsets = 'utf8mb4'
        self.db = None
        self.cursor = None

    # 链接数据库
    def get_con(self):
        """ 获取conn """
        self.db = pymysql.Connect(
            host=self.host,
            port=self.port,
            user=self.username,
            passwd=self.password,
            db=self.database,
            charset=self.charsets
        )
        self.cursor = self.db.cursor()

    # 关闭链接
    def close(self):
        self.cursor.close()
        self.db.close()

    # 主键查询数据
    def get_one(self, sql, parameters):
        res = None
        try:
            self.get_con()
            self.cursor.execute(sql, parameters)
            res = self.cursor.fetchone()
            self.close()
        except Exception as e:
            print("查询失败！" + str(e))
        return res

    # 查询列表数据
    def get_all(self, sql, parameters):
        res = None
        try:
            self.get_con()
            self.cursor.execute(sql, parameters)
            res = self.cursor.fetchall()
            self.close()
        except Exception as e:
            print("查询失败！" + str(e))
        return res

    # 插入数据
    def execute(self, sql, parameters):
        count = 0
        try:
            self.get_con()
            count = self.cursor.execute(sql, parameters)
            self.db.commit()
            self.close()
        except Exception as e:
            print("操作失败！" + str(e))
            self.db.rollback()
        return count
