from src.common.sql_template import SqlTemplate


class SupplierRepository(object):
    def __init__(self):
        self.store_db = SqlTemplate('skoyi_store_jinyong')

    def get_supplier_info(self, supplier_id):
        """
        查询供应商信息
        :param supplier_id:
        :return:
        """
        sql = "select * from store_supplier where id = %"
        data = self.store_db.get_one(sql, [supplier_id])
        return data


if __name__ == '__main__':
    print(SupplierRepository().get_supplier_info(1))
