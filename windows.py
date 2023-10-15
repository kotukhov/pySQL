import sys
from PyQt6 import uic, QtCore
from PyQt6 import QtWidgets as qtw
from PyQt6.QtSql import QSqlDatabase

import config
import helpers


class Window:
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
        tables = helpers.get_data(db_name,
                                  query="SELECT * FROM sqlite_master WHERE type='table'")
        self.tables = [t[1] for t in tables]
        super().__init__(ui)

    def show_table(self, table, title='', headers=None, column_widths=None, data=None):
        # check if table exists in database
        self.form.ViewWidget.show()
        if not data:
            data = helpers.get_data(self.db_name, table)
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
        if item == "Сортировка по Увеличению Кода":
            self.form.ViewWidget.setSortingEnabled(False)
            data = helpers.get_data(
                self.db_name,
                query=f"""SELECT * 
                        FROM Tp_nir 
                        ORDER BY codvuz, rnw""")
            self.show_table('Tp_nir', 'Информация о НИР', data=data, headers=config.TP_NIR_HEADERS)
            self.form.ViewWidget.sortItems(0, QtCore.Qt.SortOrder.AscendingOrder)
        else:
            sort_toggle = False if item == "Без сортировки" else True
            self.show_table('Tp_nir', 'Информация о НИР', headers=config.TP_NIR_HEADERS,
                            column_widths=config.TP_NIR_COLUMN_WIDTH)
            self.form.ViewWidget.setSortingEnabled(sort_toggle)

    def reset_filters(self):
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

        for data in helpers.get_data(config.DB_NAME, query="\n".join([f"SELECT DISTINCT {', '.join(self.filtered_columns)}",
                                                               "FROM VUZ JOIN Tp_nir ON VUZ.codvuz = Tp_nir.codvuz"])):
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

        return sorted([element[0] for element in helpers.get_data(config.DB_NAME, query=query)])

    @helpers.send_args_inside_func
    def combobox_filter(self, target):
        data = self.get_combobox_values(target)
        filter_level = self.filtered_columns[target]
        self.meta[filter_level] = [""] + data
        getattr(self.form, f"comboBox{filter_level}").clear()
        getattr(self.form,
                f"comboBox{filter_level}").addItems(self.meta[filter_level])

    @helpers.send_args_inside_func
    def apply_filter(self, window: MainWindow):
        query_template = "\n".join(["SELECT Tp_nir.*",
                                    "FROM Tp_nir JOIN VUZ ON Tp_nir.codvuz = VUZ.codvuz",
                                    "WHERE {column} {sign} \"{value}\""])
        grnti = self.form.lineEdit.text()
        queries = []
        if grnti.isdigit():
            queries.append("\nUNION\n".join(
                [query_template.format(column="f10", sign="LIKE", value=f"{grnti}%"),
                 query_template.format(column="f10", sign="LIKE", value=f"%,{grnti}%"),
                 query_template.format(column="f10", sign="LIKE", value=f"%;{grnti}%")]))

        for column, box_name in sorted(self.filtered_columns.items()):
            value = getattr(self.form, f"comboBox{box_name}").currentText()
            if value:
                queries.append(query_template.format(column=column, sign="=", value=value))
                break

        if not queries:
            return
        data = helpers.get_data(window.db_name, query="\nINTERSECT\n".join(queries))
        window.show_table('Tp_nir', 'Информация о НИР', config.TP_NIR_HEADERS,
                          config.TP_NIR_COLUMN_WIDTH, data)
        window.form.resetFiltersButton.setEnabled(True)

    def reset_combo_boxes(self):
        self.form.lineEdit.clear()
        for box_name in list(self.meta)[::-1]:
            if getattr(self.form, f"comboBox{box_name}").currentIndex():
                getattr(self.form, f"comboBox{box_name}").setCurrentIndex(0)
