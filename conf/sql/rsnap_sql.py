# -*- coding: utf-8 -*-
dict_sql = {
'selectOutFlow': ['mysql_r_snap', '''
select a.* FROM snap_out_flow a WHERE a.id = '#{id}'
'''],
'selectPayable':['mysql_r_snap','''
select * FROM snap_payable a WHERE a.source_id = #{source_id}           
'''],
'selectFakeData': ['mysql_r_snap', '''
SELECT * FROM fake_data WHERE id = #{data_id}
'''],
'selectSettleflow': ['mysql_r_snap', '''
select * from snap_settle_flow where settle_no = '#{settle_number}'
'''],
'selectIntoflow': ['mysql_r_snap', '''
select * from snap_into_flow a where a.id = #{id}
'''],
'deleteOutFlow': ['mysql_r_snap', '''
delete FROM snap_out_flow WHERE id = #{id}
'''],
'deletePayable': ['mysql_r_snap', '''
delete FROM snap_payable WHERE source_id = #{source_id}
'''],
'updataFakeData': ['mysql_r_snap', '''
UPDATE fake_data SET response_body = '#{body_data}' WHERE id = #{id}
'''],
'deleteSettleFlow': ['mysql_r_snap', '''
delete from snap_settle_flow where settle_no = '#{settle_number}'
'''],
'deleteIntoFlow': ['mysql_r_snap', '''
delete from snap_into_flow where id = '#{id}'
'''],
}
"""dict_sql = {
'selectOutFlow': ['mysql_r_snap', '''
select a.* from snap_out_flow a where a.supplier_id = '#{supplier_id}'
'''],
'selectPayable': ['mysql_r_snap', '''
select * from snap_payable a where a.source_id = #{id}
'''],
'selectFakedata': ['mysql_r_snap', '''
select * from fake_data a where a.id = #{id}
'''],
'selectIntoflow': ['mysql_r_snap', '''
select * from snap_into_flow a where a.source_id = #{id}
'''],
'selectSettleflow': ['mysql_r_snap', '''
select * from snap_settle_flow where settle_no = '#{settle_number}'
'''],
'deleteOutFlow': ['mysql_r_snap', '''
delete from snap_out_flow where id = #{id}
'''],
'deletePayable': ['mysql_r_snap', '''
delete from snap_payable where source_id = #{id}
'''],
'deleteSettleFlow': ['mysql_r_snap', '''
delete from snap_settle_flow where settle_no = '#{settle_number}'
'''],
'deleteIntoFlow': ['mysql_r_snap', '''
delete from snap_into_flow where id = '#{id}'
'''],
'deleteAftersaledetail': ['mysql_r_snap', '''
delete from snap_after_sale_detail where payable_id = '#{payable_id}'
'''],
'updataFakeData': ['mysql_r_snap', '''
UPDATE fake_data SET class_name = 'MpClient', method_name = 'getSaleOrder', method_type = 'POST', response_body = '{"code":200,"result":true,"data":[{"aftersales_no":"AS28111818183090511", "system_order_no":"R12009227221322233"}]}', description = '获取售后单号对应的销售单号(直接查取)' WHERE id = 7'
''']
}"""

