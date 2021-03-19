# 测试修改商品销售单位
# 从店铺中随机获取一个店铺自建商品，然后调接口(PUT /store/{storeId}/product/{prodCode}/sale-unit)修改商品的销售单位
# 验证: 直接查询数据库中 该商品 的unit字段是否符合预期


# 测试修改商品库存单位

# 从店铺中随机获取一个商品，然后调接口 (PUT /store/{storeId}/product-unit/inventory) 修改库存单位
# 验证：直接查询数据库 表 store_inventory_product 的 unit字段，看其是否符合预期
