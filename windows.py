import re
import sys
from PyQt6 import uic, QtCore
from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QMessageBox, QDialog, QTableWidgetItem

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

    def connect_db(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(config.DB_NAME)
        if not db.open():
            print('Не удалось подключиться к базе')
            return False
        return db

    def sbros(self):
        self.form.comboBoxCity.clear()
        self.form.comboBoxRegion.clear()
        self.form.comboBoxUniversity.clear()


class MainWindow(Window):
    def __init__(self, ui) -> None:
        if not self.connect_db():
            sys.exit(-1)

        tables = helpers.get_data(query="SELECT * FROM sqlite_master WHERE type='table'")
        self.tables = [t[1] for t in tables]
        super().__init__(ui)

    def show_table(self, table, title='', headers=None, column_widths=None, data=None):
        # check if table exists in database
        self.form.ViewWidget.show()
        if not data:
            data = helpers.get_data(table)
        self.form.ViewWidget.setRowCount(len(data))
        self.form.ViewWidget.setColumnCount(len(data[0]))
        for i in range(len(data)):
            for j in range(len(data[0])):
                item = QTableWidgetItem(str(data[i][j]))
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
            data = helpers.get_data(
                query=f"""SELECT codvuz || rnw AS clmn,  {', '.join(helpers.get_headers('Tp_nir')[2:])} 
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

        for data in helpers.get_data(query="\n".join([f"SELECT DISTINCT {', '.join(self.filtered_columns)}",
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

        return sorted([element[0] for element in helpers.get_data(query=query)])

    @helpers.send_args_inside_func
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

    @helpers.send_args_inside_func
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

        data = helpers.get_data(query="\nINTERSECT\n".join(query))
        window.show_table('Tp_nir', 'Информация о НИР', config.TP_NIR_HEADERS,
                          config.TP_NIR_COLUMN_WIDTH, data)

        window.form.resetFiltersButton.setEnabled(True)

    def reset_combo_boxes(self):
        self.form.lineEdit.clear()
        for box_name in list(self.meta)[::-1]:
            if getattr(self.form, f"comboBox{box_name}").currentIndex():
                getattr(self.form, f"comboBox{box_name}").setCurrentIndex(0)


class MainWindowButtons(Window):
    """Класс для кнопок главного окна: добавить, изменить"""
    def __init__(self, ui):
        super().__init__(ui)

    @helpers.send_args_inside_func
    def open_window(self, main_window, add_window, flag: bool):
        self.new_window = QDialog()
        self.ui_window = add_window
        self.ui_window.form.setupUi(self.new_window)
        self.new_window.show()
        if flag == True:
            self.ui_window.form.agreeButton.clicked.connect(self.add_button(main_window))
        else:
            selected_row = main_window.form.ViewWidget.selectionModel().selectedRows()
            selected_index = [index.row() for index in selected_row]

            if 0 < len(selected_index) < 2:

                data_stack = helpers.get_rows_from_table(selected_index[0], main_window.form.ViewWidget.model())
                if len(data_stack[4] ) >8:
                    cod_grnti = data_stack[4][:9]
                    cod_grnti_2 = data_stack[4][8:]
                    self.ui_window.form.cod_grnti.setText(cod_grnti)
                    self.ui_window.form.cod_grnti_2.setText(cod_grnti_2)

                # self.ui_window.form.cod_vuz.setEnabled(False)
                # self.ui_window.form.cod_vuz.setValue(int(data_stack[0]))
                self.ui_window.form.socr_naming.setEnabled(False)
                self.ui_window.form.socr_naming.setCurrentText(data_stack[3])

                self.ui_window.form.reg_number_nir.setDisabled(True)
                self.ui_window.form.reg_number_nir.setText(data_stack[1])

                self.ui_window.form.character_nir.setCurrentText(data_stack[2])

                self.ui_window.form.cod_grnti.setText(data_stack[4])
                self.ui_window.form.ruk_nir.setText(data_stack[5])
                self.ui_window.form.post.setText(data_stack[6])
                self.ui_window.form.financial.setValue(int(data_stack[7]))
                self.ui_window.form.naming_nir.setText(data_stack[8])

                self.ui_window.form.agreeButton.clicked.connect(self.edit_button(int(data_stack[7]),
                                                                                 selected_index[0],
                                                                                 main_window))
            else:
                message_text = 'Не выбрана строка для редактирования или выбрано более одной!'
                self.ui_window.form.message = QMessageBox(QMessageBox.Icon.Critical, 'Ошибка', message_text)
                self.ui_window.form.message.show()
                self.new_window.close()

        self.ui_window.form.cancelButton.clicked.connect(self.new_window.close)

    @helpers.send_args_inside_func
    def add_button(self, main_window: MainWindow):
        """Функция добавления строки."""

        # cod_vuz = self.ui_window.form.cod_vuz.value()
        reg_number_nir = self.ui_window.form.reg_number_nir.text()
        character_nir = self.ui_window.form.character_nir.currentText()
        socr_naming = self.ui_window.form.socr_naming.currentText()
        cod_grnti = self.ui_window.form.cod_grnti.text()
        cod_grnti_2 = self.ui_window.form.cod_grnti_2.text()
        ruk_nir = self.ui_window.form.ruk_nir.text()
        post = self.ui_window.form.post.text()
        financial = self.ui_window.form.financial.value()
        naming_nir = self.ui_window.form.naming_nir.toPlainText()

        error = 0

        if (reg_number_nir != '' and
                character_nir != '' and
                socr_naming != '' and
                cod_grnti != '..' and
                ruk_nir != ' ..' and
                post != '' and
                naming_nir != ''):

            # if cod_vuz <= 0:
            #     message_text = 'Код ВУЗа не может быть меньше или равен нулю!'
            #     self.ui_window.form.message = QMessageBox(QMessageBox.Icon.Critical, 'Ошибка', message_text)
            #     self.ui_window.form.message.show()
            #     error = 1
            dict_items = config.dict_cod_vuz_socr_naming.items()
            for key, value in dict_items:
                if value == socr_naming:
                    cod_vuz = key
            data = helpers.get_data(query=f"""SELECT codvuz, rnw FROM Tp_nir""")
            set_cod_vuz_reg_number_nir = (cod_vuz, reg_number_nir)
            if set_cod_vuz_reg_number_nir in data:
                message_text = 'Связь код ВУЗа и рег.номера НИР не уникальна!'
                self.ui_window.form.message = QMessageBox(QMessageBox.Icon.Critical, 'Ошибка', message_text)
                self.ui_window.form.message.show()
                error = 1

            if financial <= 0:
                message_text = 'Значение планового финансирования не может быть меньше или равно нулю!'
                self.ui_window.form.message = QMessageBox(QMessageBox.Icon.Critical, 'Ошибка', message_text)
                self.ui_window.form.message.show()
                error = 1

            if ((len(cod_grnti ) <6 or ' ' in cod_grnti) or
                    (cod_grnti_2 != '..' and (len(cod_grnti_2 ) <6 or ' ' in cod_grnti_2))):
                message_text = f"""Проверьте правильность написания кода ГРНТИ:\n
                            1) Не должно быть пробелов в коде\n 
                            2) Минимальный код состоит из четырех цифр
                            """
                self.ui_window.form.message = QMessageBox(QMessageBox.Icon.Critical, 'Ошибка', message_text)
                self.ui_window.form.message.show()
                error = 1

            if config.dict_cod_vuz_socr_naming[cod_vuz] != socr_naming:
                message_text = f'Данному коду ВУЗа соответсвует название: {config.dict_cod_vuz_socr_naming[cod_vuz]}'
                self.ui_window.form.message = QMessageBox(QMessageBox.Icon.Critical, 'Ошибка', message_text)
                self.ui_window.form.message.show()
                error = 1

            if error == 0:
                if len(cod_grnti) == 6:
                    cod_grnti = cod_grnti[:6]

                if cod_grnti_2 != '..':
                    if len(cod_grnti_2) == 6:
                        cod_grnti_2 = cod_grnti_2[:6]
                    cod_grnti = cod_grnti + ',' + cod_grnti_2

                query_tp_nir = f"""INSERT INTO Tp_nir (codvuz, rnw, f1, z2, f10, f6, f7, f18, f2) 
                    VALUES ({cod_vuz},'{reg_number_nir}','{character_nir}','{socr_naming}','{cod_grnti}', '{ruk_nir}', '{post}',{financial},'{naming_nir}');"""
                index = helpers.query_change_db(query_tp_nir)

                query_tp_fv = f"""
                            UPDATE Tp_fv
                            SET z3 = z3 + {financial}, numworks = numworks + 1
                            WHERE codvuz = '{cod_vuz}';
                            """
                helpers.query_change_db(query_tp_fv)
                main_window.show_table('Tp_nir', 'Информация о НИР', config.TP_NIR_HEADERS, config.TP_NIR_COLUMN_WIDTH)

                self.new_window.close()
                main_window.form.ViewWidget.selectRow(index-1)
        else:
            message_text = 'Заполните все поля!'
            self.ui_window.form.message = QMessageBox(QMessageBox.Icon.Critical, 'Ошибка заполнения полей', message_text)
            self.ui_window.form.message.show()

    @helpers.send_args_inside_func
    def edit_button(self, fin0, index, main_window: MainWindow):
        """Функция редактирования строки."""

        # cod_vuz = self.ui_window.form.cod_vuz.value()
        socr_naming = self.ui_window.form.socr_naming.currentText()
        reg_number_nir = self.ui_window.form.reg_number_nir.text()
        character_nir = self.ui_window.form.character_nir.currentText()
        cod_grnti = self.ui_window.form.cod_grnti.text()
        cod_grnti_2 = self.ui_window.form.cod_grnti_2.text()
        ruk_nir = self.ui_window.form.ruk_nir.text()
        post = self.ui_window.form.post.text()
        financial = self.ui_window.form.financial.value()
        naming_nir = self.ui_window.form.naming_nir.toPlainText()

        error = 0
        if (
                character_nir != '' and
                cod_grnti != '..' and
                ruk_nir != ' ..' and
                post != '' and
                naming_nir != ''):

            if financial <= 0:
                message_text = 'Значение планового финансирования не может быть меньше или равно нулю!'
                self.ui_window.form.message = QMessageBox(QMessageBox.Icon.Critical, 'Ошибка', message_text)
                self.ui_window.form.message.show()
                error = 1

            if ((len(cod_grnti ) <6 or ' ' in cod_grnti) or
                    (cod_grnti_2 != '..' and (len(cod_grnti_2 ) <6 or ' ' in cod_grnti_2))):
                message_text = f"""Проверьте правильность написания кода ГРНТИ:\n
                            1) Не должно быть пробелов в коде\n 
                            2) Минимальный код состоит из четырех цифр
                            """
                self.ui_window.form.message = QMessageBox(QMessageBox.Icon.Critical, 'Ошибка', message_text)
                self.ui_window.form.message.show()
                error = 1

            if error == 0:

                if len(cod_grnti) == 6:
                    cod_grnti = cod_grnti[:6]

                if cod_grnti_2 != '..':
                    if len(cod_grnti_2) == 6:
                        cod_grnti_2 = cod_grnti_2[:6]
                    cod_grnti = cod_grnti + ',' + cod_grnti_2
                dict_items = config.dict_cod_vuz_socr_naming.items()
                for key, value in dict_items:
                    if value == socr_naming:
                        cod_vuz = key
                query_tp_nir = f"""UPDATE Tp_nir 
                                SET f1 = '{character_nir}', 
                                    f10 = '{cod_grnti}', 
                                    f6 = '{ruk_nir}',
                                    f7 = '{post}',
                                    f18 = {financial},
                                    f2 =  '{naming_nir}'
                                WHERE codvuz = '{cod_vuz}' AND rnw = '{reg_number_nir}';"""
                helpers.query_change_db(query_tp_nir)

                if fin0 != financial:

                    query_tp_fv = f"""
                                UPDATE Tp_fv
                                SET z3 = z3 - {fin0} + {financial}
                                WHERE codvuz = '{cod_vuz}';
                                """
                    helpers.query_change_db(query_tp_fv)
                main_window.show_table('Tp_nir', 'Информация о НИР', config.TP_NIR_HEADERS, config.TP_NIR_COLUMN_WIDTH)

                self.new_window.close()
                main_window.form.ViewWidget.selectRow(index)
        else:
            message_text = 'Заполните все поля!'
            self.ui_window.form.message = QMessageBox(QMessageBox.Icon.Critical, 'Ошибка заполнения полей', message_text)
            self.ui_window.form.message.show()

    @staticmethod
    @helpers.send_args_inside_func
    def delete_button(main_window: MainWindow):
        """Функция удаления строки."""

        selected_rows = main_window.form.ViewWidget.selectionModel().selectedRows()
        selected_indexes = [index.row() for index in selected_rows]
        main_window.form.message = QMessageBox()
        if len(selected_indexes) > 0:
            main_window.form.message.setText("Вы уверены, что хотите удалить выделенные записи?")
            main_window.form.message.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if main_window.form.message.exec() == main_window.form.message.StandardButton.Yes:
                stack = []
                for index in selected_indexes:
                    stack.append(helpers.get_rows_from_table(index, main_window.form.ViewWidget.model()))

                for i in range(len(stack)):
                    query_tp_nir = f"DELETE FROM Tp_nir WHERE codvuz = '{stack[i][0]}' AND rnw = '{stack[i][1]}';"
                    helpers.query_change_db(query_tp_nir)

                    query_tp_fv = f"""
                                    UPDATE Tp_fv
                                    SET z3 = z3 - {stack[i][7]}, numworks = numworks - 1
                                    WHERE codvuz = '{stack[i][0]}';
                                    """
                    helpers.query_change_db(query_tp_fv)
                    main_window.form.ViewWidget.model().removeRow(index)
                    main_window.show_table('Tp_nir', 'Информация о НИР', config.TP_NIR_HEADERS, config.TP_NIR_COLUMN_WIDTH)

            else:
                message_text = 'Удаление отменено'
                main_window.form.message = QMessageBox(QMessageBox.Icon.Critical, 'Ошибка удаления', message_text)
                main_window.form.message.show()
        else:
            message_text = 'Не выбрана запись для удаления'
            main_window.form.message = QMessageBox(QMessageBox.Icon.Critical, 'Ошибка удаления', message_text)
            main_window.form.message.show()
