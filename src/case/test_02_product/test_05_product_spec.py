# 商品规格测试，测试新增，编辑，删除商品的规格

# 自建商品可以添加规格，从店铺中随机取出来一个自建商品，然后调用接口(POST /store/{storeId}/product/{prodCode}/tag) 给商品添加规格
# 验证，直接查询数据库store_product_spec看是否存在该商品的规格，或者直接调用接口查询，(GET /store/{storeId}/product/specs/{prodCode}?source=1)

# 自建商品删除规格, 从店铺中取出一个自建商品，可以是上述增加过规格的商品，然后查询该商品的规格(GET /store/{storeId}/product/specs/{prodCode})，然后调用接口进行删除规格 (DELETE /store/product/spec/{id})
# 验证，可以再次调用接口，进行查询该商品规格是否存在或者查询数据库进行验证
