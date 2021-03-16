from src.common.sql_template import SqlTemplate


class StoreRepository(object):

    def __init__(self):
        self.user_db = SqlTemplate('obm_user')

    def clear_employer(self, store_id) -> None:
        """
        清除老板的信息，包括以下表：
        store_info
        user_store
        store_zone_config
        employer_info
        user_info

        :param store_id:
        :return:
        """
        select_boss_sql = 'select boss_id from store_info where id = %s'
        boss = self.user_db.get_one(select_boss_sql, store_id)
        if boss is not None:
            boss_id = boss['boss_id']

            # 清除店铺信息  store_info
            clear_store_info_sql = 'delete from store_info where id = %s'
            self.user_db.execute(clear_store_info_sql, store_id)

            # 删除店铺相关的用户信息 user_store
            clear_store_user_sql = 'delete from user_store where store_id = %s'
            self.user_db.execute(clear_store_user_sql, store_id)

            # 删除店铺的配置信息 store_zone_config
            clear_store_config_sql = 'delete from store_zone_config where store_id = %s'
            self.user_db.execute(clear_store_config_sql, store_id)

            # 清除老板信息 employer_info
            clear_employer_sql = 'delete from employer_info where id = %s'
            self.user_db.execute(clear_employer_sql, boss_id)

            # 清除用户信息 user_info
            clear_user_info_sql = 'delete from user_info where id = %s'
            self.user_db.execute(clear_user_info_sql, boss_id)

    def get_store_by_mobile(self, mobile: str):
        """
        :param mobile:  手机号
        :return: {"store_id": 1, "user_id":1}
        """
        select_store_sql = 'select id as store_id, boss_id as user_id  from store_info where phone = %s '
        return self.user_db.get_one(select_store_sql, mobile)

    def get_customer_id_list(self):
        """
        获取客户 id 列表
        :return:
        """
        customer_sql = 'select id from customer_info'
        id_tuples = self.user_db.get_all(customer_sql)
        res = []
        for id in id_tuples:
            res.append(id['id'])
        return res

    def get_user_by_id(self, user_id):
        select_user_sql = 'select * from user_info where id = %s'
        return self.user_db.get_one(select_user_sql, user_id)


if __name__ == '__main__':
    print(StoreRepository().get_store_by_mobile('18600000300'))
