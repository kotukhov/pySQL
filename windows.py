import sqlite3
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
        self.last_query = ""
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

    def get_data(self, table=None, query="SELECT * \nFROM {}", log=True):
        conn = sqlite3.connect(config.DB_NAME)
        cursor = conn.cursor()
        query = query.format(table) or query
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        if log and "Tp_nir" in query:
            self.last_query = query
        return data

    @staticmethod
    @helpers.send_args_inside_func
    def close(*windows):
        for w in windows:
            w.window.close()


class MainWindow(Window):
    def __init__(self, ui) -> None:
        if not self.connect_db():
            sys.exit(-1)

        tables = self.get_data(query="SELECT * FROM sqlite_master WHERE type='table'")
        self.tables = [t[1] for t in tables]
        super().__init__(ui)

    def show_table(self, table, title='', headers=None, column_widths=None, data=None):
        # check if table exists in database
        self.form.ViewWidget.show()
        if table != "Tp_nir":
            sort_toggle = False
            self.form.ViewWidget.setSortingEnabled(sort_toggle)
        if not data:
            data = self.get_data(table)
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
        self.form.label.setText(title)

    def sort_selected(self):
        item = self.form.comboBoxSort.currentText()
        query = self.last_query
        if not query or "Tp_nir" not in query:
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
                if len(data_stack[4])>8:
                    cod_grnti = data_stack[4][:9]
                    cod_grnti_2 = data_stack[4][8:]
                    self.ui_window.form.cod_grnti.setText(cod_grnti)
                    self.ui_window.form.cod_grnti_2.setText(cod_grnti_2)

                self.ui_window.form.socr_naming.setEnabled(False)
                self.ui_window.form.socr_naming.setCurrentText(data_stack[3])
                
                self.ui_window.form.reg_number_nir.setDisabled(True)
                self.ui_window.form.reg_number_nir.setText(data_stack[1])

                dict_items = config.dict_character_nir.items()
                for key, value in dict_items:
                    if value == data_stack[2]:
                        character_nir = key
                
                self.ui_window.form.character_nir.setCurrentText(character_nir)
                
                self.ui_window.form.cod_grnti.setText(data_stack[4])
                self.ui_window.form.ruk_nir.setText(data_stack[5])
                self.ui_window.form.post.setText(data_stack[6])
                self.ui_window.form.financial.setValue(int(data_stack[7]))
                self.ui_window.form.naming_nir.setText(data_stack[8])
                
                self.ui_window.form.agreeButton.clicked.connect(self.edit_button(int(data_stack[7]), selected_index[0], main_window))
            else:
                message_text = 'Не выбрана строка для редактирования или выбрано более одной!'
                self.ui_window.form.message = QMessageBox(QMessageBox.Icon.Critical, 'Ошибка', message_text)
                self.ui_window.form.message.show()
                self.new_window.close()
                
        self.ui_window.form.cancelButton.clicked.connect(self.new_window.close)  
            
    @helpers.send_args_inside_func
    def add_button(self, main_window):
        """Функция добавления строки."""

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

            dict_items = config.dict_cod_vuz_socr_naming.items()
            for key, value in dict_items:
                if value == socr_naming:
                    cod_vuz = key
            data = self.get_data(query=f"""SELECT codvuz, rnw FROM Tp_nir""")

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

            if ((len(cod_grnti)<6 or ' ' in cod_grnti or len(cod_grnti) == 7) or
                (cod_grnti_2 != '..' and (len(cod_grnti_2)<6 or ' ' in cod_grnti_2 or len(cod_grnti_2) == 7))):
                message_text = f"""Проверьте правильность написания кода ГРНТИ:\n
                            1) Не должно быть пробелов в коде\n 
                            2) Минимальный код состоит из четырех цифр\n
                            3) Код не может состоять из пяти цифр
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
                    cod_grnti = cod_grnti[:5]
                    print(cod_grnti)

                if cod_grnti_2 != '..':
                    if len(cod_grnti_2) == 6:
                        cod_grnti_2 = cod_grnti_2[:5]
                    cod_grnti = cod_grnti + ';' + cod_grnti_2
                
                query_tp_nir = f"""INSERT INTO Tp_nir (codvuz, rnw, f1, z2, f10, f6, f7, f18, f2) 
                    VALUES ({cod_vuz},'{reg_number_nir}','{config.dict_character_nir[character_nir]}','{socr_naming}','{cod_grnti}', '{ruk_nir}', '{post}',{financial},'{naming_nir}');"""
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
    def edit_button(self, fin0, index, main_window):
        """Функция редактирования строки."""

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


            if ((len(cod_grnti)<6 or ' ' in cod_grnti or len(cod_grnti) == 7) or
                (cod_grnti_2 != '..' and (len(cod_grnti_2)<6 or ' ' in cod_grnti_2 or len(cod_grnti_2) == 7))):
                message_text = f"""Проверьте правильность написания кода ГРНТИ:\n
                            1) Не должно быть пробелов в коде\n 
                            2) Минимальный код состоит из четырех цифр\n
                            3) Код не может состоять из пяти цифр
                            """
                self.ui_window.form.message = QMessageBox(QMessageBox.Icon.Critical, 'Ошибка', message_text)
                self.ui_window.form.message.show()
                error = 1
            
            if error == 0:
                
                if len(cod_grnti) == 6:
                    cod_grnti = cod_grnti[:5]

                if cod_grnti_2 != '..':
                    if len(cod_grnti_2) == 6:
                        cod_grnti_2 = cod_grnti_2[:5]
                    cod_grnti = cod_grnti + ';' + cod_grnti_2
                dict_items = config.dict_cod_vuz_socr_naming.items()
                for key, value in dict_items:
                    if value == socr_naming:
                        cod_vuz = key
                query_tp_nir = f"""UPDATE Tp_nir 
                                SET f1 = '{config.dict_character_nir[character_nir]}', 
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

    @helpers.send_args_inside_func
    def delete_button(self, main_window):
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
                    helpers.query_change_db(query=query_tp_nir)

                    query_tp_fv = f"""
                                    UPDATE Tp_fv
                                    SET z3 = z3 - {stack[i][7]}, numworks = numworks - 1
                                    WHERE codvuz = '{stack[i][0]}';
                                    """
                    helpers.query_change_db(query=query_tp_fv)
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
