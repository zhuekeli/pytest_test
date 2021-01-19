# -*- coding: utf-8 -*-

dict_sql = {
'selectPaidMoney': ['mysql_orderdb', '''
select sum(a.need_pay_amount - a.payed_amount) as payMoney from order_db.customer_order a
where a.main_number = '#{order}'
''']
}