import sys
import sqlite3
from PyQt6 import uic, QtCore
from PyQt6 import QtWidgets as qtw
from PyQt6.QtSql import QSqlDatabase

import config

Form, Window = uic.loadUiType("MainForm.ui")
Form_filtr, Window_filtr = uic.loadUiType("filtr.ui")
Form_exit, Window_exit = uic.loadUiType("ex_aht.ui")
db_name = 'database.db'
cache = {"FOs": [], "regions": [], "cities": [], "universities": []}


def get_data(db_name, table=None, query="SELECT * FROM {}"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    query = query.format(table) or query
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data


def show_grntirub():
    data = get_data(db_name, 'grntirub')
    form.GrntiViewWidget.setRowCount(len(data))
    form.GrntiViewWidget.setColumnCount(len(data[0]))
    for i in range(len(data)):
        for j in range(len(data[0])):
            item = qtw.QTableWidgetItem(str(data[i][j]))
            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
            form.GrntiViewWidget.setItem(i, j, item)

    form.GrntiViewWidget.setHorizontalHeaderLabels(config.GRNTI_HEADERS)
    for column, width in enumerate(config.GRNTI_COLUMN_WIDTH):
        form.GrntiViewWidget.setColumnWidth(column, width)

    form.GrntiViewWidget.setSortingEnabled(True)
    form.label_3.setText('Информация о рубриках ГРНТИ')


def show_Tp_nir():
    data = get_data(db_name, 'Tp_nir')
    form.NirViewWidget.setRowCount(len(data))
    form.NirViewWidget.setColumnCount(len(data[0]))
    for i in range(len(data)):
        for j in range(len(data[0])):
            if j == 7:
                item = qtw.QTableWidgetItem(str(data[i][j]))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
                form.NirViewWidget.setItem(i, j, item)
            else:
                item = qtw.QTableWidgetItem(str(data[i][j]))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
                form.NirViewWidget.setItem(i, j, item)
    
    form.NirViewWidget.setHorizontalHeaderLabels(config.TP_NIR_HEADERS)
    for column, width in enumerate(config.NP_NIR_COLUMN_WIDTH):
        form.NirViewWidget.setColumnWidth(column, width)

    form.label_1.setText('Информация о НИР')


def show_Tp_fv():
    data = get_data(db_name, 'Tp_fv')
    form.FinancialViewWidget.setRowCount(len(data))
    form.FinancialViewWidget.setColumnCount(len(data[0]))
    for i in range(len(data)):
        for j in range(len(data[0])):
            if j in (2, 3):
                item = qtw.QTableWidgetItem(str(data[i][j]))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
                form.FinancialViewWidget.setItem(i, j, item)
            else:
                item = qtw.QTableWidgetItem(str(data[i][j]))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
                form.FinancialViewWidget.setItem(i, j, item)

    form.FinancialViewWidget.setHorizontalHeaderLabels(config.TP_FV_HEADERS)
    for column, width in enumerate(config.TP_FV_COLUMN_WIDTH):
        form.FinancialViewWidget.setColumnWidth(column, width)

    form.FinancialViewWidget.setSortingEnabled(True)
    form.label_2.setText('Информация о финансировании')


def show_VUZ():
    data = get_data(db_name, 'VUZ')
    form.VuzTableView.setRowCount(len(data))
    form.VuzTableView.setColumnCount(len(data[0]))
    for i in range(len(data)):
        for j in range(len(data[0])):
            item = qtw.QTableWidgetItem(str(data[i][j]))
            if item:
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
                form.VuzTableView.setItem(i, j, item)
                
    form.VuzTableView.setHorizontalHeaderLabels(config.VUZ_HEADERS)
    for column, width in enumerate(config.TP_FV_COLUMN_WIDTH):
        form.VuzTableView.setColumnWidth(column, width)

    form.VuzTableView.setSortingEnabled(True)
    form.label_4.setText('Информация о ВУЗах')


def connect_db(db_name):
    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName(db_name)
    if not db.open():
        print('Не удалось подключиться к базе')
        return False
    return db


###сработало
def filter_by_FO():
    global cache
    FO = form_filtr.comboBoxFO.currentText()
    if not cache['FOs']:
        FOs = get_data(db_name, query="SELECT DISTINCT region FROM VUZ")
    cache['FOs'] = [FO[0] for FO in FOs]
    if FO not in cache['FOs']:
        return
    
    regions = get_data(
        db_name,
        query=f"SELECT DISTINCT oblname FROM VUZ  WHERE region = '{FO}'")
    if not cache['regions']:
        cache['regions'] = [region[0] for region in regions]
    form_filtr.comboBoxRegion.clear()
    form_filtr.comboBoxRegion.addItems(cache['regions'])


def filter_by_region():
    global cache
    region = form_filtr.comboBoxRegion.currentText()
    if region not in cache['regions']:
        return
    
    cities = get_data(
        db_name, 
        query=f"SELECT DISTINCT city FROM VUZ WHERE oblname = '{region}'")
    if not cache['cities']:
        cache['cities'] = [city[0] for city in cities]
    form_filtr.comboBoxCity.clear()
    form_filtr.comboBoxCity.addItems(cache['cities'])
        


def filter_by_city():
    global cache
    city = form_filtr.comboBoxCity.currentText()
    if city not in cache['cities']:
        return

    universities = get_data(
        db_name, 
        query=f"SELECT DISTINCT z2 FROM VUZ WHERE city = '{city}'")
    if not cache['universities']:
        cache['universities'] = [university[0] for university in universities]
    form_filtr.comboBoxUniversity.clear()
    form_filtr.comboBoxUniversity.addItems(cache['universities'])


def sort_selected():
    item = form.comboBoxSort.currentText()
    if item == "Сортировка по каждому столбцу":
        form.NirViewWidget.setSortingEnabled(True)
    elif item == "Сортировка по Убыванию Кода":
        form.NirViewWidget.setSortingEnabled(False)
        form.NirViewWidget.sortItems(0, QtCore.Qt.SortOrder.DescendingOrder)
        # Тут надо реализовать сортировку по сумме кодов
    elif item == "Сортировка по Увеличению Кода":
        form.NirViewWidget.setSortingEnabled(False)
        form.NirViewWidget.sortItems(0, QtCore.Qt.SortOrder.AscendingOrder)
    else:
        form.NirViewWidget.setSortingEnabled(False)


def close_all():
    window.close()
    window_exit.close()
    window_filtr.close()



if not connect_db(db_name):
    sys.exit(-1)
else:
    print('Connection OK')

app = qtw.QApplication([])
window = Window()
window_filtr = Window_filtr()
form_filtr = Form_filtr()
form_filtr.setupUi(window_filtr)
form = Form()
form.setupUi(window)
window_exit = Window_exit()
form_exit = Form_exit()
form_exit.setupUi(window_exit)
show_Tp_nir()
show_Tp_fv()
show_grntirub()
show_VUZ()

list_fed_n = ['']
list_fed = get_data(db_name, query="SELECT DISTINCT region FROM VUZ")
for i in range(len(list_fed)):
    list_fed_n.append(list_fed[i][0])
form_filtr.comboBoxFO.addItems(list_fed_n)
form_filtr.comboBoxFO.currentTextChanged.connect(filter_by_FO)
form_filtr.comboBoxRegion.currentTextChanged.connect(filter_by_region)
form_filtr.comboBoxCity.currentTextChanged.connect(filter_by_city)
form.comboBoxSort.currentTextChanged.connect(sort_selected)
form.filterButton.clicked.connect(window_filtr.show)
form_filtr.cancelButton.clicked.connect(window_filtr.close)
window.show()
form.exitButton.clicked.connect(window_exit.show)
form_exit.agreeButton.clicked.connect(close_all)
form_exit.cancelButton.clicked.connect(window_exit.close)
exit(app.exec())
