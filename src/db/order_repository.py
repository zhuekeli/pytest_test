from src.common.sql_template import SqlTemplate


class OrderRepository(object):
    def __init__(self):
        self.store_db = SqlTemplate('skoyi_store_jinyong')

    def get_order(self, order_number):
        """
        查询订单信息
        :param order_number:
        :return:
        """
        sql = "select * from order_sale where order_number = %"
        data = self.store_db.get_one(sql, [order_number])
        return data


if __name__ == '__main__':
    print(OrderRepository().get_order(1))
