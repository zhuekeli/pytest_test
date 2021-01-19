# -*- coding: utf-8 -*-

dict_sql = {
'selectTokenById': ['mysql_ruigucrmdev', '''
select a.id, a.token, a.customer_type order_type from think_member a where a.id = #{id}
'''],
'selectTokenByMname': ['mysql_ruigucrmdev', '''
select a.id, a.token, a.customer_type order_type from think_member a where a.mname = '#{mname}'
'''],
'selectSubOrder': ['mysql_ruigucrmdev', '''
select a.os_main_order_number, a.orderNumber, a.orderStatus, a.deliverType
from ruigu_member_order a where a.orderNumber = '#{order}' or a.os_main_order_number = '#{order}'
'''],
'selectMainByOrder': ['mysql_ruigucrmdev', '''
select a.os_main_order_number, a.orderStatus from ruigu_member_order a where a.orderNumber = '#{order}'
'''],
'selectExpressByOrder': ['mysql_ruigucrmdev', '''
select b.express_corp, b.express_no from ruigu_member_order a, ruigu_to_dealer_order b
where a.order_id = b.member_order_id and a.orderNumber = '#{order}'
'''],
'selectSmOrder': ['mysql_ruigucrmdev', '''
select a.ruiguSmOrderId, a.smOrderId, a.status, a.tms_order, a.is_push_wms from ruigu_to_dc_sm_order a
where a.status != 4 and a.dealerOrderNumber = '#{order}' 
'''],
'updateOdPayTime':  ['mysql_ruigucrmdev', '''
update ruigu_member_order a
set a.payTime = date_format(date_sub(str_to_date(a.payTime, '%Y-%m-%d %H:%i:%s'), interval 15 minute), '%Y-%m-%d %H:%i:%s')
where a.orderNumber = '#{order}'
'''],
'updateOdReceiveTime':  ['mysql_ruigucrmdev', '''
update ruigu_member_order a set a.receiveTime = unix_timestamp(date_sub(from_unixtime(a.receiveTime), interval 7 day))
where a.orderNumber = '#{order}' and a.orderStatus = 5
'''],
'updateSmOrderPushTMS': ['mysql_ruigucrmdev', '''
update ruigu_to_dc_sm_order a set a.is_push_wms = 2
where a.dealerOrderNumber = '#{order}' and a.is_push_wms = 1                        
''']
}