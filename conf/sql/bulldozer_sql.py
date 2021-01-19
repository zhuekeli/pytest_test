# -*- coding: utf-8 -*-

dict_sql = {
'selectOutBound': ['mysql_bulldozer', '''
select b.outbound_no, b.state, b.sent_state from out_order a, outbound_order b
where a.order_no = b.out_order_no and a.sm_order_no = '#{sm_order}'
'''],
'selectOutBoundSku': ['mysql_bulldozer', '''
select a.sku_code, a.quantity, a.sent_quantity from outbound_order_item a
where a.outbound_no = '#{outbound_no}'
'''],
'selectPresaleStock': ['mysql_bulldozer', '''
select a.version, a.start_pre_Time, a.warehouse_code
from bulldozer.pre_sale_stock a where a.pre_sale_status = 1 and a.sku_code = '#{sku_code}'
''']
}