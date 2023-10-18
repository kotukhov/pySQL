TP_NIR_HEADERS = ('Код ВУЗа', 'Рег. номер НИР', 'Характер НИР', 'Сокр. назв. ВУЗа',
                  'Код ГРНТИ', 'Руководитель НИР', 'Должность руководителя',
                  'Плановое финанс.', 'Наименование НИР')
GRNTI_HEADERS = ('Код рубрики', 'Рубрика')
TP_FV_HEADERS = ('Код ВУЗа', 'Сокр. назв. ВУЗА', 'Плановое финанс.',
                 'Фактическое финанс.', 'Кол-во НИР')
VUZ_HEADERS = ('Код ВУЗа', 'Сокр. назв. ВУЗа', 'Статус', 'Фед. округ', 'Город',
               'Код области', 'Субъект Федерации', 'Научный статус',
               'Проф. направление', 'Наименование ВУЗа', 'Полное наименование ВУЗа')
# original headers ['codvuz', 'z2', 'status', 'region', 'city', 'obl', 'oblname', 'gr_ved', 'prof', 'z1', 'z1full']
GRNTI_COLUMN_WIDTH = (100, 550)
TP_NIR_COLUMN_WIDTH = (80, 120, 120, 130, 140, 150, 180, 140, 100)
TP_FV_COLUMN_WIDTH = (80, 130, 140, 150, 100)
VUZ_COLUMN_WIDTH = (80, 130, 120, 130, 140, 100, 200, 140, 100, 700, 1000)

widgetnames = ['Financial', 'Vuz', 'Grnti', 'Nir']

dict_cod_vuz_socr_naming = {
        1: 'АлтГТУ', 
        2: 'АлтГУ',
        3: 'АнгарГТА',
        4: 'Сев(Аркт)ФУ',
        6: 'БалтГТУ',
        8: 'БелГТхнУ',
        10: 'БратГУ',
        12: 'БрянГИТА',
        14: 'ВолгГУ',
        16: 'ВолгГТУ',
        17: 'ВологГТУ',
        18: 'ВорГУ',
        19: 'ВорГАСУ',
        20: 'ВорГЛТА',
        21: 'ВорГТУ',
        22: 'ВорГУИТ',
        23: 'ВСГУТиУ',
        28: 'РГУНГ',
        29: 'ГУУ',
        33: 'ДагГУ',
        34: 'ДагГТУ',
        35: 'ДВГТУ',
        40: 'ИвГУ',
        41: 'ИвГЭУ',
        43: 'ИвГТА',
        44: 'ИвГХТхнУ',
        53: 'ИркГТУ',
        54: 'КБГУ',
        55: 'КазНИТУ-КАИ',
        56: 'КазНИТхнУ',
        57: 'Каз(Прив)ФУ',
        58: 'КазГАСУ',
        60: 'БалтФУ',
        61: 'КалмГУ',
        62: 'КамГИЭА',
        65: 'КемТИПП',
        66: 'ВятГУ',
        67: 'КоврГТА',
        68:	'КнАГТУ',
        69:	'КострГТУ',
        70:	'КубГТхнУ',
        71:	'СибФУ',
        73: 'ГУЦМиЗ',
        76: 'КузГТУ',
        78: 'ЮЗГУ',
        79: 'ЛипГТУ',
        81:	'МарГУ',
        82: 'ПовГТУ',
        84:	'МордГУ',
        85:	'МАМИ',
        86: 'МГУДиТ',
        88:	'МГУПищП',
        89:	'МГУПБио',
        90:	'РГГРУ',
        91:	'МГТекстУ',
        92:	'МАИ',
        94:	'МГИндУ',
        95:	'МАРХИ',
        96:	'МГВМетИ',
        97:	'МГГУ',
        99:	'МАДИ'
        }