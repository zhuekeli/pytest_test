from src.common.db import DbUtil

db = DbUtil()


def get_product_scan_code(store_id):
    """
     查询数据库获取商品扫描码
    :param store_id:  店铺 id
    :return:
    """
    sql = "select scan_code from store_product_scan_code where store_id = %s "
    data = db.get_all(sql, [store_id])
    print(data)


if __name__ == '__main__':
    get_product_scan_code(1)
