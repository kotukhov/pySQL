import sqlite3
import config


def send_args_inside_func(func):
    def wrapper(*args, **kwargs):
        return lambda: func(*args, **kwargs)

    return wrapper


def get_headers(table, query=None):
    conn = sqlite3.connect(config.DB_NAME)
    cursor = conn.cursor()
    if query is not None:
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return data
    
    cursor.execute(f"SELECT * FROM {table}")
    cursor.fetchall()
    data = [descr[0] for descr in cursor.description]
    conn.close()
    return data


def query_change_db(query):
    """Запросы на изменения таблицы"""
    conn = sqlite3.connect(config.DB_NAME)
    cursor = conn.cursor()
    cursor.execute(query)
    if 'INSERT INTO' in query:
        index = cursor.lastrowid
        conn.commit()
        conn.close()
        return index

    conn.commit()
    conn.close()


def get_rows_from_table(index, model):
    """Получение данных строки в таблице (не из БД)"""
    rowIndex = index
    columnCount = model.columnCount()
    rowValues = []
    for columnIndex in range(columnCount):
        cellValue = model.data(model.index(rowIndex, columnIndex))
        rowValues.append(cellValue)
    return rowValues
