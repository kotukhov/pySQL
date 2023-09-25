import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
from PyQt6.QtSql import *

DB_NAME = 'database.db'


def on_click():
    print('')


def show_table(table_name):
    def view():
            table = QSqlTableModel()
            table.setTable(table_name)
            table.select()
            global form
            form.tableView.setModel(table)
            form.tableView.setSortingEnabled(True)
    
    return view


def connect_db(db_name):
    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName(db_name)
    if not db.open():
        print('Connection failed')
        return
    
    return db


def main(db_name):
    if not db_name:
        db_name = DB_NAME

    if not connect_db(db_name):
        return
    
    print('Connection OK')
    Form, Window = uic.loadUiType("MainForm.ui")
    app = QApplication([])
    window = Window()
    global form
    form = Form()
    form.setupUi(window)
    form.pushButton.clicked.connect(show_table('Tp_nir'))
    form.pushButton_2.clicked.connect(show_table('Tp_fv'))
    form.pushButton_3.clicked.connect(show_table('grntirub'))
    form.pushButton_4.clicked.connect(show_table('VUZ'))
    window.show()
    app.exec()


if __name__ == "__main__":
    main(sys.argv[1:])
