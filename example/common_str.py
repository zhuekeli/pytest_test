# -*- coding: utf-8 -*-

# 字符串替换 入参: 字典对象 如 dict{id: 4860} #{id} -> 4860
def sql_cmd_replace(sql_cmd=None, di=None):
    # print(sql_cmd)
    for key in di.keys():
        sql_cmd = str(sql_cmd).replace('#{' + key + '}', str(di[key]))
    return sql_cmd


# 字典排序转字符串 key1=value1&keys=value2
def dict_sortstr(param: dict):
    data = ''
    for key in sorted(param.keys()):
        data += key + '=' + str(param[key]) + '&'
    if len(data) > 0:
        data = data[0:-1]
    return data


# 字典直接转字符串 key1=value1&keys=value2
def dict_str(param: dict):
    data = ''
    for key in param.keys():
        data += key + '=' + str(param[key]) + '&'
    if len(data) > 0:
        data = data[0:-1]
    return data


# list -> str 如 [1,2,3] -> 1,2,3
def list_str(param: list, deli: str):
    data = ''
    if len(param):
        for i in param:
            data = data + str(i) + deli
        if len(data) > 0:
            data = data[0:-1]
    return data


def dict_merge(di_s: dict, di_d: dict):
    for key in di_d.keys():
        di_s[key] = di_d[key]
    return di_s
