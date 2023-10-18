import sqlite3
import sys
from PyQt6 import uic, QtCore
from PyQt6 import QtWidgets as qtw
from PyQt6.QtSql import QSqlDatabase

import config
import helpers


def connect_db(db_name):
    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName(db_name)
    if not db.open():
        print('Не удалось подключиться к базе')
        return False
    return db


class Window:
    def __init__(self, ui) -> None:
        # get all table names in self.tables
        Form, Window = uic.loadUiType(ui)
        self.window = Window()
        self.form = Form()
        self.last_query = ""
        self.form.setupUi(self.window)
        self.cache = {"FOs": [''], "regions": [''], "cities": [''], "universities": ['']}
        # window.show()

    def get_data(self, table=None, query="SELECT * \nFROM {}", log=True):
        conn = sqlite3.connect(config.DB_NAME)
        cursor = conn.cursor()
        query = query.format(table) or query
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        if log:
            self.last_query = query
        return data


class MainWindow(Window):
    def __init__(self, ui, db_name) -> None:
        if not connect_db(db_name):
            sys.exit(-1)
        # self.form = MF.Ui_MainWindow
        self.db_name = db_name
        tables = self.get_data(query="SELECT * \nFROM sqlite_master \nWHERE type='table'")
        self.tables = [t[1] for t in tables]
        super().__init__(ui)

    def show_table(self, table, title='', headers=None, column_widths=None, data=None):
        # check if table exists in database
        self.form.ViewWidget.show()
        # if table == "Tp_nir":
        #     self.sort_selected()
        if not data:
            data = self.get_data(table)
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
        self.form.label.setText(title)

    def sort_selected(self):
        item = self.form.comboBoxSort.currentText()
        query = self.last_query
        if not query:
            query = "SELECT * \nFROM Tp_nir"

        if item == "Сортировка по потенциальному ключу":
            sort_toggle = False
            self.form.ViewWidget.setSortingEnabled(sort_toggle)
            if "GROUP BY" not in query:
                query = "\n".join([query, "GROUP BY Tp_nir.codvuz, rnw"])
            else:
                query = "\n".join(query.split('\n')[:-1] + ["GROUP BY Tp_nir.codvuz, rnw"])
        else:
            if "GROUP BY" in query:
                query = "\n".join(query.split('\n')[:-1])

            sort_toggle = False if item == "Без сортировки" else True

        self.show_table('Tp_nir', 'Информация о НИР', headers=config.TP_NIR_HEADERS,
                        column_widths=config.TP_NIR_COLUMN_WIDTH,
                        data=self.get_data(query=query, log=False))
        self.form.ViewWidget.setSortingEnabled(sort_toggle)

    @helpers.send_args_inside_func
    def reset_filters(self, window):
        self.show_table('Tp_nir', 'Информация о НИР', config.TP_NIR_HEADERS, config.TP_NIR_COLUMN_WIDTH)
        self.form.comboBoxSort.setCurrentIndex(0)
        self.form.resetFiltersButton.setEnabled(False)
        window.reset_form()


class FilterWindow(Window):
    def __init__(self, ui) -> None:
        super().__init__(ui)
        self.boxes_data = {"FO": [""], "Region": [""], "City": [""], "University": [""]}
        self.condition = []
        self.column2widget = dict(zip(["region", "oblname", "city", "VUZ.z2"],
                                      self.boxes_data))
        self.query_template = '\n'.join(["SELECT DISTINCT {select_column}",
                                         "FROM Tp_nir JOIN VUZ ON Tp_nir.codvuz = VUZ.codvuz",
                                         "WHERE {column} = \"{value}\""])
        for data in self.get_data(query="\n".join([f"SELECT DISTINCT {', '.join(self.column2widget)}",
                                                   "FROM VUZ JOIN Tp_nir ON VUZ.codvuz = Tp_nir.codvuz"])):
            self.boxes_data['FO'].append(data[0])
            self.boxes_data['Region'].append(data[1])
            self.boxes_data['City'].append(data[2])
            self.boxes_data['University'].append(data[3])

        self.boxes_data = {k: sorted(set(v)) for k, v in self.boxes_data.items()}
        self.form.comboBoxFO.addItems(self.boxes_data['FO'])
        self.form.comboBoxRegion.addItems(self.boxes_data['Region'])
        self.form.comboBoxCity.addItems(self.boxes_data['City'])
        self.form.comboBoxUniversity.addItems(self.boxes_data['University'])

    def get_combobox_values(self, target_column):
        query = []
        for column, filter_level in self.column2widget.items():
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
            query = f"SELECT DISTINCT {target_column} \nFROM VUZ JOIN Tp_nir ON Tp_nir.codvuz = VUZ.codvuz"

        return sorted([element[0] for element in self.get_data(query=query)])

    @helpers.send_args_inside_func
    def combobox_filter(self, target):
        data = self.get_combobox_values(target)
        filter_level = self.column2widget[target]
        self.boxes_data[filter_level] = [""] + data
        getattr(self.form, f"comboBox{filter_level}").clear()
        getattr(self.form,
                f"comboBox{filter_level}").addItems(self.boxes_data[filter_level])

    @helpers.send_args_inside_func
    def apply_filter(self, window: MainWindow):
        self.condition = []
        query_template = "\n".join(["SELECT Tp_nir.*",
                                    "FROM Tp_nir JOIN VUZ ON Tp_nir.codvuz = VUZ.codvuz",
                                    "WHERE {column} {sign} \"{value}\""])
        grnti = self.form.lineEdit.text()
        queries = []
        if grnti.isdigit():
            queries.append("\nUNION\n".join(
                [query_template.format(column="f10", sign="LIKE", value=f"{grnti}%"),
                 query_template.format(column="f10", sign="LIKE", value=f"%;{grnti}%")]))
            self.condition.append(grnti)

        for column, box_name in sorted(self.column2widget.items()):
            value = getattr(self.form, f"comboBox{box_name}").currentText()
            self.condition.append(value or None)
            if value:
                queries.append(query_template.format(column=column, sign="=", value=value))

        self.condition = self.condition[::-1]
        if not queries:
            return
        data = window.get_data(query="\nINTERSECT\n".join(queries))
        window.show_table('Tp_nir', 'Информация о НИР', config.TP_NIR_HEADERS,
                          config.TP_NIR_COLUMN_WIDTH, data)
        window.form.resetFiltersButton.setEnabled(True)
        self.window.hide()

    def reset_form(self):
        self.form.lineEdit.clear()
        for box_name in list(self.boxes_data)[::-1]:
            if getattr(self.form, f"comboBox{box_name}").currentIndex():
                getattr(self.form, f"comboBox{box_name}").setCurrentIndex(0)
