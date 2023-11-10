import sqlite3
import config
import windows


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


def query_change_db(query=None, socr_naming=False, fact=False):
    """Запросы на изменения таблицы"""
    conn = sqlite3.connect(config.DB_NAME)
    cursor = conn.cursor()
   
    if query != None:
        cursor.execute(query)

        if 'INSERT INTO' in query:
            index = cursor.lastrowid
            conn.commit()
            conn.close()
            return index
        
        conn.commit()
        conn.close()

    if socr_naming and fact:
        for i in range(len(windows.planfact)):
            query = f"""UPDATE Tp_fv SET z18 = z18 + {windows.planfact[i]} WHERE z2 = '{windows.socr_naming_list[i]}';"""
            cursor.execute(query)
            conn.commit()
        conn.close()
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
