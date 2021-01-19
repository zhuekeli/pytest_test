# -*- coding: utf-8 -*-

import pandas as pd
import sys
sys.path.append("../")

# 读取 Excel 文件
# 入参 file Excel 文件名 sheet Sheet文件名 sid 导入数据标 
def excel_data(file:str, sheet:str, sid:str):
    file = "../data/" + file
    try:
        df = pd.read_excel(file, sheet_name=sheet)
        df['sid'] = df['sid'].astype(str)
        df_sid = df[df["sid"] == sid]
        # 删除 SID 列的标记
        df_sid = df_sid.drop(columns = "sid")
        for i in range(len(df_sid)):
            print(df_sid.iloc[i])
            # save_to_mysql(df_sid, conn, sheet)
    except:
        print("文件读取失败: " + file)

excel_data("mysql_ruigucrmdev.xlsx", "think_member", "S2")