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
    def _get_cursor(self):
        """ 获取conn """
        self.db = pymysql.Connect(
            host=self.host,
            port=self.port,
            user=self.username,
            passwd=self.password,
            db=self.database,
            charset=self.charsets
        )
        return self.db.cursor(cursor=pymysql.cursors.DictCursor)

    # 关闭链接
    def close(self):
        self.cursor.close()
        self.db.close()

    # 主键查询数据
    def get_one(self, sql, args=None):
        """
        用于执行查询操作

        :param sql: sql 语句
        :param args:  tuple、list or dict
        :return:  查询的数据 dict 类型 {}

        If args is a list or tuple, %s can be used as a placeholder in the query.
        If args is a dict, %(name)s can be used as a placeholder in the query.
        """
        res = None
        try:
            self.cursor = self._get_cursor()
            self.cursor.execute(sql, args)
            res = self.cursor.fetchone()
            self.close()
        except Exception as e:
            print("查询失败！" + str(e))
        return res

    # 查询列表数据
    def get_all(self, sql, args=None):
        """
        用于执行查询操作

        :param sql: sql 语句
        :param args:  tuple、list or dict
        :return:  查询的数据  tuple 类型，元素是 dict 类型 ({}), 查不到返回空的 tuple

        If args is a list or tuple, %s can be used as a placeholder in the query.
        If args is a dict, %(name)s can be used as a placeholder in the query.
        """
        res = ()
        try:
            self.cursor = self._get_cursor()
            self.cursor.execute(sql, args)
            res = self.cursor.fetchall()

            self.close()
        except Exception as e:
            print("查询失败！" + str(e))
        return res

    # 插入数据
    def execute(self, sql, args=None):
        """
        用于执行更新、插入、删除操作

        :param sql: sql 语句
        :param args:  tuple、list or dict
        :return:  返回受影响的行数

        If args is a list or tuple, %s can be used as a placeholder in the query.
        If args is a dict, %(name)s can be used as a placeholder in the query.
        """
        count = 0
        try:
            self.cursor = self._get_cursor()
            count = self.cursor.execute(sql, args)
            self.db.commit()
            self.close()
        except Exception as e:
            print("操作失败！" + str(e))
            self.db.rollback()
        return count


if __name__ == '__main__':
    user_db = DbUtil('obm_user')
    sql1 = 'select * from user_info'
    print(user_db.get_all(sql1))

    one_sql = 'select * from user_info limit 1'
    print(user_db.get_one(one_sql))
