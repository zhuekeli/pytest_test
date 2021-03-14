from src.common.db_util import DbUtil

db = DbUtil('skoyi_store_jinyong')


def get_product_scan_code(store_id):
    """
     查询数据库获取商品扫描码
    :param store_id:  店铺 id
    :return:
    """
    sql = "select scan_code from store_product_scan_code where store_id = %s "
    data = db.get_all(sql, [store_id])
    print(data)


def get_product_inventory_quantity(store_id, prod_code):
    """
    查询商品库存.
    :param store_id:
    :param prod_code:
    :return: 返回商品库存
    """
    sql = "select quantity from store_inventory_product where store_id = %s and prod_code = %s"
    data = db.get_one(sql, [store_id, prod_code])
    return data[0]


def get_store_category(store_id):
    """
    查询店铺分类列表
    :param store_id:
    :return: 返回店铺分类Id列表
    """
    sql = "select category_id from store_category where store_id = %s"
    data = db.get_all(sql, [store_id])
    category_list = []
    for category_id in data:
        category_list.append(category_id[0])
    return category_list


if __name__ == '__main__':
    get_product_scan_code(1)
    print(get_product_inventory_quantity(2, '000002-00018'))
    get_store_category(2)
