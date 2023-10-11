import re
import sys
import sqlite3
from PyQt6 import uic, QtCore
from PyQt6 import QtWidgets as qtw
from PyQt6.QtSql import QSqlDatabase

import config

db_name = 'database.db'


def send_args_inside_func(func):
    def wrapper(*args, **kwargs):
        return lambda: func(*args, **kwargs)

    return wrapper


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

    def connect_db(self, db_name):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(db_name)
        if not db.open():
            print('Не удалось подключиться к базе')
            return False
        return db

    def sbros(self):
        self.form.comboBoxCity.clear()
        self.form.comboBoxRegion.clear()
        self.form.comboBoxUniversity.clear()


class MainWindow(Window):
    def __init__(self, ui, db_name) -> None:
        if not self.connect_db(db_name):
            sys.exit(-1)

        self.db_name = db_name
        tables = get_data(db_name,
                          query="SELECT * FROM sqlite_master WHERE type='table'")
        self.tables = [t[1] for t in tables]
        super().__init__(ui)

    def show_table(self, table, title='', headers=None, column_widths=None, data=None):
        # check if table exists in database
        self.form.ViewWidget.show()
        if not data:
            data = get_data(self.db_name, table)
        self.form.ViewWidget.setRowCount(len(data))
        self.form.ViewWidget.setColumnCount(len(data[0]))
        for i in range(len(data)):
            for j in range(len(data[0])):
                item = qtw.QTableWidgetItem(str(data[i][j]))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
                self.form.ViewWidget.setItem(i, j, item)
        if headers:
            self.form.ViewWidget.setHorizontalHeaderLabels(headers)
        if column_widths and len(column_widths) == len(data[0]):
            for column, width in enumerate(column_widths):
                self.form.ViewWidget.setColumnWidth(column, width)

        self.form.ViewWidget.setSortingEnabled(False)
        self.form.label.setText(title)  # 'Информация о рубриках ГРНТИ', 'Информация о НИР'

    def sort_selected(self):
        item = self.form.comboBoxSort.currentText()
        if item.endswith('Кода'):
            if item == "Сортировка по Убыванию Кода":
                order = QtCore.Qt.SortOrder.DescendingOrder
            elif item == "Сортировка по Увеличению Кода":
                order = QtCore.Qt.SortOrder.AscendingOrder
            self.form.ViewWidget.setSortingEnabled(False)
            data = get_data(
                db_name,
                query=f"""SELECT codvuz || rnw AS clmn,  {', '.join(get_headers('Tp_nir')[2:])} 
                        FROM Tp_nir 
                        ORDER BY codvuz, clmn""")
            headers = ['Код+РНВ'] + list(config.TP_NIR_HEADERS[2:])
            self.show_table('Tp_nir', 'Информация о НИР', data=data, headers=headers)
            self.form.ViewWidget.sortItems(0, order)
        else:
            sort_toggle = False if item == "Без сортировки" else True
            self.show_table('Tp_nir', 'Информация о НИР', headers=config.TP_NIR_HEADERS,
                            column_widths=config.TP_NIR_COLUMN_WIDTH)
            self.form.ViewWidget.setSortingEnabled(sort_toggle)

    def resfil_but(self):
        self.show_table('Tp_nir', 'Информация о НИР', config.TP_NIR_HEADERS, config.TP_NIR_COLUMN_WIDTH)
        self.form.resetFiltersButton.setEnabled(False)


class FilterWindow(Window):
    def __init__(self, ui) -> None:
        super().__init__(ui)
        self.meta = {"FO": [""], "Region": [""], "City": [""], "University": [""]}
        self.filtered_columns = dict(zip(["region", "oblname", "city", "VUZ.z2"],
                                         self.meta))
        self.query_template = """
        SELECT DISTINCT {select_column} 
        FROM Tp_nir JOIN VUZ ON Tp_nir.codvuz = VUZ.codvuz
        WHERE {column} = "{value}" """

        for data in get_data(db_name, query=f"SELECT DISTINCT {', '.join(self.filtered_columns)} FROM VUZ"):
            self.meta['FO'].append(data[0])
            self.meta['Region'].append(data[1])
            self.meta['City'].append(data[2])
            self.meta['University'].append(data[3])

        self.meta = {k: sorted(set(v)) for k, v in self.meta.items()}
        self.form.comboBoxFO.addItems(self.meta['FO'])
        self.form.comboBoxRegion.addItems(self.meta['Region'])
        self.form.comboBoxCity.addItems(self.meta['City'])
        self.form.comboBoxUniversity.addItems(self.meta['University'])

    def get_combobox_values(self, target_column):
        query = []
        for column, filter_level in self.filtered_columns.items():
            if column == target_column:
                break
            value = getattr(self.form, f"comboBox{filter_level}").currentText()
            if value:
                query.append(self.query_template.format(column=column,
                                                        value=value,
                                                        select_column=target_column))

        if query:
            query = "\nINTERSECT\n".join(set(query))
        else:
            query = f"SELECT DISTINCT {target_column} FROM VUZ JOIN Tp_nir ON Tp_nir.codvuz = VUZ.codvuz"

        return sorted([element[0] for element in get_data(db_name, query=query)])

    @send_args_inside_func
    def combobox_filter(self, target):
        data = self.get_combobox_values(target)
        filter_level = self.filtered_columns[target]
        self.meta[filter_level] = [""] + data
        getattr(self.form, f"comboBox{filter_level}").clear()
        getattr(self.form,
                f"comboBox{filter_level}").addItems(self.meta[filter_level])

    def get_grnti_code(self):
        code = self.form.lineEdit.text()
        if not code:
            return
        minimal_pattern = r"\d{2}\.\d{2}(\.\d{2})?"
        pattern = f"^{minimal_pattern}([;,]{minimal_pattern})?$"
        if re.match(pattern, code):
            return code
        # warning label for user

    @send_args_inside_func
    def apply_filter(self, window: MainWindow):
        query_template = "\n".join(["SELECT Tp_nir.*",
                                    "FROM Tp_nir JOIN VUZ ON Tp_nir.codvuz = VUZ.codvuz",
                                    "WHERE {column} = \"{value}\""])
        grnti = self.get_grnti_code()
        query = [query_template.format(column="f10", value=grnti)] if grnti else []
        for column, box_name in self.filtered_columns.items():
            value = getattr(self.form, f"comboBox{box_name}").currentText()
            if value:
                query.append(query_template.format(column=column, value=value))

        if not query:
            return

        data = get_data(window.db_name, query="\nINTERSECT\n".join(query))
        window.show_table('Tp_nir', 'Информация о НИР', config.TP_NIR_HEADERS,
                          config.TP_NIR_COLUMN_WIDTH, data)

    def reset_combo_boxes(self):
        self.form.lineEdit.clear()
        for box_name in list(self.meta)[::-1]:
            if getattr(self.form, f"comboBox{box_name}").currentIndex():
                getattr(self.form, f"comboBox{box_name}").setCurrentIndex(0)


def close_all():
    main_window.window.close()
    filter_window.window.close()
    exit_window.window.close()


def get_headers(table):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    cursor.fetchall()
    data = [descr[0] for descr in cursor.description]
    conn.close()
    return data


app = qtw.QApplication([])
main_window = MainWindow('MF.ui', db_name)
filter_window = FilterWindow('filtr.ui')
exit_window = Window('ex_aht.ui')

shadow_show_table = send_args_inside_func(main_window.show_table)
main_window.form.Niraction.triggered.connect(shadow_show_table(
    'Tp_nir', 'Информация о НИР', config.TP_NIR_HEADERS, config.TP_NIR_COLUMN_WIDTH))
main_window.form.Niraction.triggered.connect(main_window.form.horizontalFrame.show)
main_window.form.Vuzaction.triggered.connect(shadow_show_table(
    'VUZ', 'Информация о ВУЗах', config.VUZ_HEADERS, config.VUZ_COLUMN_WIDTH))
main_window.form.Vuzaction.triggered.connect(main_window.form.horizontalFrame.hide)
main_window.form.Grntiaction.triggered.connect(shadow_show_table(
    'grntirub', 'Информация о ГРНТИ', config.GRNTI_HEADERS, config.GRNTI_COLUMN_WIDTH))
main_window.form.Grntiaction.triggered.connect(main_window.form.horizontalFrame.hide)
main_window.form.Financialaction.triggered.connect(shadow_show_table(
    'Tp_fv', 'Информация о Финансировании', config.TP_FV_HEADERS, config.TP_FV_COLUMN_WIDTH))
main_window.form.Financialaction.triggered.connect(main_window.form.horizontalFrame.hide)

filter_window.form.comboBoxFO.currentTextChanged.connect(filter_window.combobox_filter("oblname"))
filter_window.form.comboBoxRegion.currentTextChanged.connect(filter_window.combobox_filter("city"))
filter_window.form.comboBoxCity.currentTextChanged.connect(filter_window.combobox_filter("VUZ.z2"))
filter_window.form.filterButton.clicked.connect(filter_window.apply_filter(main_window))
main_window.form.horizontalFrame.hide()
main_window.form.comboBoxSort.currentTextChanged.connect(main_window.sort_selected)
main_window.form.filterButton.clicked.connect(filter_window.window.show)
filter_window.form.cancelButton.clicked.connect(filter_window.window.close)
filter_window.form.resetButton.clicked.connect(filter_window.reset_combo_boxes)
main_window.window.showMaximized()
main_window.form.resetFiltersButton.setEnabled(False)

#main_window.form.resetFiltersButton.clicked.connect(lambda: main_window.show_table(
    #'Tp_nir', 'Информация о НИР',config.TP_NIR_HEADERS, config.TP_NIR_COLUMN_WIDTH))

main_window.form.resetFiltersButton.clicked.connect(main_window.resfil_but)

main_window.form.Exaction.triggered.connect(exit_window.window.show)

exit_window.form.agreeButton.clicked.connect(close_all)
exit_window.form.cancelButton.clicked.connect(exit_window.window.close)
exit(app.exec())