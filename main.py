import sys
import sqlite3
from PyQt6 import uic, QtCore
from PyQt6 import QtWidgets as qtw
from PyQt6.QtSql import QSqlDatabase

import config

Form, Window = uic.loadUiType("MainForm.ui")
Form_filtr, Window_filtr = uic.loadUiType("filtr.ui")
Form_aht, Window_aht = uic.loadUiType("ex_aht.ui")
db_name = 'database.db'

def get_data(db_name, table):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table}")
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
window_aht = Window_aht()
form_aht = Form_aht()
form_aht.setupUi(window_aht)
show_Tp_nir()
show_Tp_fv()
show_grntirub()
show_VUZ()


list_fed_n = ['']
conn = sqlite3.connect(db_name)
cursor = conn.cursor()
cursor.execute("SELECT DISTINCT region FROM VUZ")
list_fed = cursor.fetchall()
conn.close()
for i in range(len(list_fed)):
    list_fed_n.append(list_fed[i][0])
form_filtr.comboBox.addItems(list_fed_n)
conn.close()



###сработало
def filtr():
    list_1_n = ['']
    list_2_n = ['']
    list_3_n = ['']
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT region FROM VUZ")
    list_1 = cursor.fetchall()
    region = form_filtr.comboBox.currentText()
    for i in range(len(list_1)):
        list_1_n.append(list_1[i][0])
    #print(list_1_n)
    for j in range(len(list_1_n)):
        if region == list_1_n[j]:
            cursor.execute(f"SELECT DISTINCT oblname FROM VUZ  WHERE region = '{region}'")
            list_2 = cursor.fetchall()
            #print(list_2)
            for k in range(len(list_2)):
                list_2_n.append(list_2[k][0])
            form_filtr.comboBox_2.clear()
            form_filtr.comboBox_2.addItems(list_2_n)



def filtr_2():
    oblname = form_filtr.comboBox_2.currentText()
    print(oblname)
    for x in range(len(list_2_n)):
        if oblname == list_2_n[x]:
            cursor.execute(f"SELECT DISTINCT city FROM VUZ  WHERE oblname = '{oblname}'")
            list_3 = cursor.fetchall()
            for p in range(len(list_3)):
                list_3_n.append(list_3[p][0])
            print(list_3_n)
            form_filtr.comboBox_3.clear()
            form_filtr.comboBox_3.addItems(list_3_n)

    conn.close()


def sort_selected():
    item = form.comboBox.currentText()
    if item == "Сортировка по каждому столбцу":
        form.NirViewWidget.setSortingEnabled(True)
    elif item == "Сортировка по Убыванию Кода":
        form.NirViewWidget.setSortingEnabled(False)
        #form.tableView_1.setSort('codvuz') # Тут надо реализовать сортировку по сумме кодов

        form.NirViewWidget.sortItems(1, QtCore.Qt.DescendingOrder)
    elif item == "Сортировка по Увеличению Кода":
        form.NirViewWidget.setSortingEnabled(False)
        form.NirViewWidget.sortItems(1, QtCore.Qt.AscendingOrder)
    else:
        form.NirViewWidget.setSortingEnabled(False)


#form_filtr.comboBox_2.currentTextChanged.connect(filtr)
form_filtr.comboBox.currentTextChanged.connect(filtr)
form.comboBoxSort.currentTextChanged.connect(sort_selected)
form.filterButton.clicked.connect(window_filtr.show)

def closeall():
    window.close()
    window_aht.close()
    window_filtr.close()



form_filtr.cancelButton.clicked.connect(window_filtr.close)
window.show()
form.exitButton.clicked.connect(window_aht.show)
form_aht.agreeButton.clicked.connect(closeall)
form_aht.cancelButton.clicked.connect(window_aht.close)
app.exec()