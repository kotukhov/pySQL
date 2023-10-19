from PyQt6.QtWidgets import QApplication
import windows as wnd
import config
import helpers


@helpers.send_args_inside_func
def close_all(*windows):
    for w in windows:
        w.window.close()


def main():
    app = QApplication([])
    main_window = wnd.MainWindow('MF.ui')
    filter_window = wnd.FilterWindow('filtr.ui')
    exit_window = wnd.Window('ex_aht.ui')
    add_window = wnd.MainWindowButtons('add_button.ui')

    shadow_show_table = helpers.send_args_inside_func(main_window.show_table)
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
    main_window.form.resetFiltersButton.clicked.connect(shadow_show_table(
        'Tp_nir', 'Информация о НИР', config.TP_NIR_HEADERS, config.TP_NIR_COLUMN_WIDTH))

    main_window.form.resetFiltersButton.clicked.connect(main_window.resfil_but)

    main_window.form.Exaction.triggered.connect(exit_window.window.show)

    exit_window.form.agreeButton.clicked.connect(close_all(main_window,
                                                           filter_window,
                                                           add_window,
                                                           exit_window))
    exit_window.form.cancelButton.clicked.connect(exit_window.window.close)

    main_window.form.removeButton.clicked.connect(wnd.MainWindowButtons.delete_button(main_window))

    main_window.form.appendButton.clicked.connect(add_window.open_window(main_window, add_window, True))
    main_window.form.changeButton.clicked.connect(add_window.open_window(main_window, add_window, False))
    return app.exec()


if __name__ == '__main__':
    main()
