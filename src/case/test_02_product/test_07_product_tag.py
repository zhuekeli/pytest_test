# 测试新增 删除商品的标签.

# 1.随机的从店铺中取出来一个商品，然后调接口新增一个标签 (POST /store/{storeId}/product/{prodCode}/tag)
# 验证，查询数据库中是否已经存在了该标签，查询 store_product 的tags字段

# 2. 拿到上述添加过标签的商品，然后调接口 删除该标签 (DELETE /store/{storeId}/product/{prodCode}/tag)
# 验证，查询数据库中该商品的tags字段，是否已经不包含已删除的商品标签了.
