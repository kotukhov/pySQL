import sys
import sqlite3
from PyQt6 import uic, QtCore
from PyQt6 import QtWidgets as qtw
from PyQt6.QtSql import QSqlDatabase

import config

db_name = 'database.db'


def get_data(db_name, table=None, query="SELECT * FROM {}"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    query = query.format(table) or query
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data


class Window():
    def __init__(self, ui) -> None:
        # get all table names in self.tables
        Form, Window = uic.loadUiType(ui)
        self.window = Window()
        self.form = Form()
        self.form.setupUi(self.window)
        self.cache = {"FOs": [''], "regions": [''], "cities": [''], "universities": ['']}
        # window.show()

    def filter_by_FO(self):
        FO = self.form.comboBoxFO.currentText()
        if not self.cache['FOs']:
            FOs = get_data(db_name, query="SELECT DISTINCT region FROM VUZ")
            self.cache['FOs'] = [FO[0] for FO in FOs]
        if FO not in self.cache['FOs']:
            return
        self.FO = FO
        regions = get_data(
            db_name,
            query=f"SELECT DISTINCT oblname FROM VUZ  WHERE region = '{FO}'")
        self.cache['regions'] = [region[0] for region in regions]
        self.form.comboBoxRegion.clear()
        self.form.comboBoxRegion.addItems(self.cache['regions'])

    def filter_by_region(self):
        region = self.form.comboBoxRegion.currentText()
        if region not in self.cache['regions']:
            return
        self.region = region
        cities = get_data(
            db_name,
            query=f"SELECT DISTINCT city FROM VUZ WHERE oblname = '{region}'")
        self.cache['cities'] = [city[0] for city in cities]
        self.form.comboBoxCity.clear()
        self.form.comboBoxCity.addItems(self.cache['cities'])

    def filter_by_city(self):
        city = self.form.comboBoxCity.currentText()
        if city not in self.cache['cities']:
            return
        self.city = city
        universities = get_data(
            db_name,
            query=f"SELECT DISTINCT z2 FROM VUZ WHERE city = '{city}'")
        self.cache['universities'] = [university[0] for university in universities]
        self.form.comboBoxUniversity.clear()
        self.form.comboBoxUniversity.addItems(self.cache['universities'])

    def filter_by_university(self):
        university = self.form.comboBoxUniversity.currentText()
        if university not in self.cache['universities']:
            return
        self.university = university

    def apply_filter(self, main_window):

        def inner():
            data = get_data(main_window.db_name,
                            query=f"""SELECT Tp_nir.* 
                            FROM Tp_nir JOIN VUZ ON Tp_nir.codvuz = VUZ.codvuz
                            WHERE region = '{self.FO}' 
                            AND oblname = '{self.region}' 
                            AND city = '{self.city}'
                            AND Tp_nir.z2 = '{self.university}'""")
            main_window.show_table('Tp_nir', 'Информация о НИР',config.TP_NIR_HEADERS, config.TP_NIR_COLUMN_WIDTH, data)
            main_window.form.resetFiltersButton.setEnabled(True)
        return inner


    def connect_db(self, db_name):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(db_name)
        if not db.open():
            print('Не удалось подключиться к базе')
            return False
        return db


    def sort_selected():
        item = form.comboBoxSort.currentText()
        if item == "Сортировка по каждому столбцу":
            form.NirViewWidget.setSortingEnabled(True)
        elif item == "Сортировка по Убыванию Кода":
            form.tableWidget.setSortingEnabled(False)
            form.NirViewWidget.sortItems(0, QtCore.Qt.SortOrder.DescendingOrder)
            # Тут надо реализовать сортировку по сумме кодов
        elif item == "Сортировка по Увеличению Кода":
            form.tableWidget.setSortingEnabled(False)
            form.tableWidget.sortItems(0, QtCore.Qt.SortOrder.AscendingOrder)
        else:
            form.NtableWidget.setSortingEnabled(False)

    def sbros(self):
        self.form.comboBoxCity.clear()
        self.form.comboBoxRegion.clear()
        self.form.comboBoxUniversity.clear()


class MainWindow(Window):
    def __init__(self, ui, db_name) -> None:
        if not self.connect_db(db_name):
            sys.exit(-1)

        print('Connection OK')
        self.db_name = db_name
        tables = get_data(db_name,
                          query="SELECT * FROM sqlite_master WHERE type='table'")
        self.tables = [t[1] for t in tables]
        super().__init__(ui)

    def show_table(self, table, title='test', headers=None, column_widths=None, data=None):
        # check if table exists in database
        getattr(self.form, f"ViewWidget").show()
        if not data:
            data = get_data(self.db_name, table)
        getattr(self.form, f"ViewWidget").setRowCount(len(data))
        getattr(self.form, f"ViewWidget").setColumnCount(len(data[0]))
        for i in range(len(data)):
            for j in range(len(data[0])):
                item = qtw.QTableWidgetItem(str(data[i][j]))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
                getattr(self.form, f"ViewWidget").setItem(i, j, item)
        if headers:
            getattr(self.form, f"ViewWidget").setHorizontalHeaderLabels(headers)
        if column_widths and len(column_widths) == len(data[0]):
            for column, width in enumerate(column_widths):
                getattr(self.form, f"ViewWidget").setColumnWidth(column, width)

        getattr(self.form, f"ViewWidget").setSortingEnabled(True)
        getattr(self.form, f"label").setText(title)  # 'Информация о рубриках ГРНТИ', 'Информация о НИР'

    def resfil_but(self):
        self.show_table('Tp_nir', 'Информация о НИР', config.TP_NIR_HEADERS, config.TP_NIR_COLUMN_WIDTH)
        self.form.resetFiltersButton.setEnabled(False)

def close_all():
    main_window.window.close()
    filter_window.window.close()
    exit_window.window.close()


app = qtw.QApplication([])
main_window = MainWindow('MF.ui', db_name)
filter_window = Window('filtr.ui')
exit_window = Window('ex_aht.ui')


#
main_window.form.Niraction.triggered.connect(lambda: main_window.show_table(
    'Tp_nir', 'Информация о НИР',config.TP_NIR_HEADERS, config.TP_NIR_COLUMN_WIDTH))
main_window.form.Niraction.triggered.connect(main_window.form.horizontalFrame.show)
main_window.form.Vuzaction.triggered.connect(lambda: main_window.show_table(
    'VUZ', 'Информация о ВУЗах',config.VUZ_HEADERS, config.VUZ_COLUMN_WIDTH))
main_window.form.Vuzaction.triggered.connect(main_window.form.horizontalFrame.hide)
main_window.form.Grntiaction.triggered.connect(lambda: main_window.show_table(
    'grntirub', 'Информация о ГРНТИ',config.GRNTI_HEADERS, config.GRNTI_COLUMN_WIDTH))
main_window.form.Grntiaction.triggered.connect(main_window.form.horizontalFrame.hide)
main_window.form.Financialaction.triggered.connect(lambda: main_window.show_table(
    'Tp_fv', 'Информация о Финансировании',config.TP_FV_HEADERS, config.TP_FV_COLUMN_WIDTH))
main_window.form.Financialaction.triggered.connect(main_window.form.horizontalFrame.hide)

for FO in get_data(db_name, query="SELECT DISTINCT region FROM VUZ"):
    filter_window.cache['FOs'].append(FO[0])

filter_window.form.resetButton.clicked.connect(filter_window.sbros)
filter_window.form.comboBoxFO.addItems(filter_window.cache['FOs'])
filter_window.form.comboBoxFO.currentTextChanged.connect(filter_window.filter_by_FO)
filter_window.form.comboBoxRegion.currentTextChanged.connect(filter_window.filter_by_region)
filter_window.form.comboBoxCity.currentTextChanged.connect(filter_window.filter_by_city)
filter_window.form.comboBoxUniversity.currentTextChanged.connect(filter_window.filter_by_university)
filter_window.form.filterButton.clicked.connect(filter_window.apply_filter(main_window))
main_window.form.horizontalFrame.hide()
# form.comboBoxSort.currentTextChanged.connect(sort_selected)
main_window.form.filterButton.clicked.connect(filter_window.window.show)
filter_window.form.cancelButton.clicked.connect(filter_window.window.close)
main_window.window.showMaximized()
main_window.form.resetFiltersButton.setEnabled(False)

#main_window.form.resetFiltersButton.clicked.connect(lambda: main_window.show_table(
    #'Tp_nir', 'Информация о НИР',config.TP_NIR_HEADERS, config.TP_NIR_COLUMN_WIDTH))

main_window.form.resetFiltersButton.clicked.connect(main_window.resfil_but)

main_window.form.Exaction.triggered.connect(exit_window.window.show)




exit_window.form.agreeButton.clicked.connect(close_all)
exit_window.form.cancelButton.clicked.connect(exit_window.window.close)
exit(app.exec())
