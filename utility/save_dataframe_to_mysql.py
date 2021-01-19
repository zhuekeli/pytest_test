from numpy import array_split


def _gen_save_values(li):
    li = map(lambda x: str(tuple(x)), li)
    st_values = ','.join(li)
    st_values = st_values.replace("'null'",  'null')
    return st_values


def _save_values_to_mysql(li, st_col, table, cursor, conn):
    st_values = _gen_save_values(li)
    sql_cmd = f'''
            INSERT INTO {table} {st_col}
            VALUES {st_values}
            '''
    cursor.execute(sql_cmd)
    conn.commit()


def save_to_mysql(df, conn, table_name, batch=5000):
    """
    :param df: the pandas.DataFrame you want to save.
    :param conn: pymysql.connector.
    :param table_name: the table_name in mysql database.
    :param  batch: how many rows do you want to save every batch
    :return: None
    """
    df = df.fillna('null')
    cursor = conn.cursor()
    st_col = str(tuple(df.columns.values)).replace("'", '')
    li_output = list(df.values)
    li_output = array_split(li_output, int(len(li_output) / batch) + 1)
    for li in li_output:
        _save_values_to_mysql(li, st_col, table_name, cursor, conn)
