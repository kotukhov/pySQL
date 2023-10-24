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

COLUMN_WIDTHS_NirbVUZ = (120,90,130)
COLUMN_WIDTHS_Nirbhar = (200,90,130)
COLUMN_WIDTHS_Nirbgrnti = (70,250,90,130)

HEADERS_NirbVUZ = ('Сокр. наим. ВУЗа','Кол-во НИР','Плановое Финанс.')
HEADERS_Nirbhar = ('Характер', 'Кол-во НИР', 'Плановое Финанс.')
HEADERS_Nirbgrnti = ('Код ГРНТИ','Рубрика','Кол-во НИР','Плановое Финанс.')

widgetnames = ['Financial', 'Vuz', 'Grnti', 'Nir']
DB_NAME = 'database.db'

dict_character_nir = {
            'Экспериментальная разработка':'Р',
            'Фундаментальное исследование': 'Ф',
            'Прикладное исследование': 'П'
        }

dict_cod_vuz_socr_naming = {1: 'АлтГТУ', 
                            2: 'АлтГУ', 
                            3: 'АнгарГТА', 
                            4: 'Сев(Аркт)ФУ', 
                            6: 'БалтГТУ', 
                            7: 'БашГУ', 
                            8: 'БелГТхнУ', 
                            9: 'АмурГУ', 
                            10: 'БратГУ', 
                            11: 'БрянГТУ', 
                            12: 'БрянГИТА', 
                            13: 'ВладГУ', 
                            14: 'ВолгГУ', 
                            15: 'ВолгГАСУ', 
                            16: 'ВолгГТУ', 
                            17: 'ВологГТУ', 
                            18: 'ВорГУ', 
                            19: 'ВорГАСУ', 
                            20: 'ВорГЛТА', 
                            21: 'ВорГТУ', 
                            22: 'ВорГУИТ', 
                            23: 'ВСГУТиУ', 
                            26: 'МГУТиУ', 
                            28: 'РГУНГ', 
                            29: 'ГУУ', 
                            33: 'ДагГУ', 
                            34: 'ДагГТУ', 
                            35: 'ДВГТУ', 
                            36: 'ДВФУ', 
                            37: 'ТихокГЭУ', 
                            38: 'ДонГТУ', 
                            40: 'ИвГУ', 
                            41: 'ИвГЭУ', 
                            42: 'ИвГАСУ', 
                            43: 'ИвГТА', 
                            44: 'ИвГХТхнУ', 
                            45: 'ИжГТУ', 
                            51: 'ИркГУ', 
                            52: 'БайГУЭП', 
                            53: 'ИркГТУ', 
                            54: 'КБГУ', 
                            55: 'КазНИТУ-КАИ', 
                            56: 'КазНИТхнУ', 
                            57: 'Каз(Прив)ФУ', 
                            58: 'КазГАСУ', 
                            59: 'КазФЭИ', 
                            60: 'БалтФУ', 
                            61: 'КалмГУ', 
                            62: 'КамГИЭА', 
                            63: 'СКГГТхнА', 
                            64: 'КемГУ', 
                            65: 'КемТИПП', 
                            66: 'ВятГУ',
                            67: 'КоврГТА', 
                            68: 'КнАГТУ', 
                            69: 'КострГТУ', 
                            70: 'КубГТхнУ', 
                            71: 'СибФУ', 
                            72: 'КрГАСА', 
                            73: 'ГУЦМиЗ', 
                            74: 'КрГТУ', 
                            75: 'КубГУ', 
                            76: 'КузГТУ', 
                            77: 'КургГУ', 
                            78: 'ЮЗГУ', 
                            79: 'ЛипГТУ', 
                            80: 'МагнГТУ', 
                            81: 'МарГУ', 
                            82: 'ПовГТУ', 
                            84: 'МордГУ', 
                            85: 'МАМИ', 
                            86: 'МГУДиТ', 
                            87: 'МГУП', 
                            88: 'МГУПищП', 
                            89: 'МГУПБио', 
                            90: 'РГГРУ', 
                            91: 'МГТекстУ', 
                            92: 'МАИ', 
                            93: 'МАТИ', 
                            94: 'МГИндУ', 
                            95: 'МАРХИ', 
                            96: 'МГВМетИ', 
                            97: 'МГГУ', 
                            99: 'МАДИ', 
                            100: 'МГИЭМ', 
                            101: 'НИУ МИЭТ', 
                            102: 'МГЛингУ', 
                            103: 'МГОУ', 
                            104: 'МГТУ', 
                            105: 'Станкин', 
                            107: 'МГСУ', 
                            108: 'НИУ МИФИ', 
                            109: 'МГУГИК', 
                            110: 'МГАКХиС', 
                            111: 'МГУПИ', 
                            112: 'МГИРЭА', 
                            113: 'НИУ МИСиС', 
                            114: 'МГУТХТ', 
                            115: 'МГУИЭ', 
                            116: 'МГГЭИ', 
                            118: 'МГУЛ', 
                            119: 'МПедГУ', 
                            120: 'МФТИ', 
                            121: 'МГХПА', 
                            122: 'МЭСИ', 
                            123: 'НИУ МЭИ', 
                            132: 'НижГАСУ', 
                            133: 'НижГТУ', 
                            134: 'НижГУ', 
                            136: 'НовгГУ', 
                            137: 'НовсГАХА', 
                            138: 'НовсГТУ', 
                            139: 'НовсНИГУ', 
                            140: 'НовсГАСУ', 
                            141: 'СибГГА', 
                            142: 'НовсГУЭУ', 
                            143: 'ЮРГТУ', 
                            144: 'НорИИ', 
                            146: 'ОбнГТУАЭ',
                            147: 'ОмскГУ', 
                            148: 'ОмскГТУ', 
                            149: 'ОренГУ', 
                            150: 'ПензГУАС', 
                            151: 'ПензГУ', 
                            152: 'ПермНИПУ', 
                            153: 'ПермГНИУ', 
                            154: 'ПетрГУ', 
                            162: 'РЭУ', 
                            166: 'РосГидро', 
                            167: 'РГГУ', 
                            168: 'РосЗИТЛП', 
                            170: 'РУДН', 
                            171: 'РХТУ', 
                            172: 'РостГСУ', 
                            173: 'РостААИ', 
                            174: 'ЮжнФУ', 
                            175: 'РостГАСМ', 
                            176: 'РосГЭУ', 
                            177: 'РыбГАТУ', 
                            178: 'РязГРТУ', 
                            179: 'СПбГУАКП', 
                            180: 'СПбГИЭУ', 
                            181: 'СПбГЛТУ', 
                            182: 'Горный', 
                            183: 'СПбГМТУ', 
                            184: 'СПбГПолУ', 
                            185: 'СПбГУ', 
                            186: 'СПбГУТД', 
                            187: 'ЛЭТИ', 
                            188: 'СПбГАСУ', 
                            189: 'СПбИМаш', 
                            190: 'СПбНИУИТМО', 
                            191: 'СПбГТехИ', 
                            192: 'СПбГУНТПТ', 
                            193: 'СПбГТУРП', 
                            194: 'СПбГУЭиФ', 
                            195: 'СПбГХПА', 
                            197: 'СамГАСУ', 
                            198: 'СамГАУ', 
                            199: 'СамГТУ', 
                            200: 'СамГУ', 
                            201: 'СамГЭУ', 
                            202: 'СаратГТУ', 
                            203: 'СаратГУ', 
                            204: 'СаратСЭУ', 
                            205: 'СаратГЮА', 
                            207: 'СКГМИ', 
                            209: 'СОГУ', 
                            210: 'СЗГЗТУ', 
                            211: 'СибАКУ', 
                            212: 'СибГАДА', 
                            213: 'СибГИндУ', 
                            214: 'СибГТхнУ', 
                            216: 'СКФУ', 
                            217: 'СыктГУ', 
                            218: 'ТагГРТУ', 
                            219: 'ТамбГТУ', 
                            220: 'ТверГУ', 
                            221: 'ТверГТУ', 
                            222: 'ТолГУ', 
                            223: 'НИТомГУ', 
                            224: 'ТомГАСУ', 
                            225: 'ТомГУСУР', 
                            226: 'НИТомПУ', 
                            227: 'ТулГУ', 
                            228: 'ТюмГУ', 
                            229: 'ТюмГНУ', 
                            230: 'ТюмГАСУ', 
                            231: 'УдмГУ', 
                            232: 'УлГТУ', 
                            233: 'УрГЮА', 
                            234: 'УрГАРХА', 
                            235: 'УрГГУ', 
                            236: 'УрГТУ', 
                            237: 'УрГУ', 
                            238: 'УрГЭУ', 
                            239: 'УрГЛУ', 
                            240: 'УфГАТУ', 
                            241: 'УфГНТУ', 
                            242: 'УхГТУ', 
                            245: 'ТихокГУ', 
                            246: 'ХабГАЭП', 
                            252: 'ЮУГУ', 
                            253: 'ЧелГУ', 
                            254: 'ЧечГУ', 
                            255: 'ЗабайкГУ', 
                            256: 'ЧувГУ', 
                            257: 'СВФедУ', 
                            258: 'ЯрГУ', 
                            259: 'ЯрГТУ', 
                            261: 'СочГУ', 
                            264: 'ГУ-УНПК', 
                            267: 'ЧерГУ', 
                            272: 'РГУИТП', 
                            275: 'ГАлтГУ', 
                            278: 'КыргРСУ', 
                            279: 'ГАкСК', 
                            281: 'ПущГЕНИ', 
                            285: 'ТамбГУ', 
                            289: 'ГЕА', 
                            291: 'РГУТС', 
                            292: 'ВладГУЭС', 
                            293: 'ИнгГУ', 
                            294: 'ХакГУ', 
                            296: 'УлГУ', 
                            300: 'МайГТхнУ', 
                            304: 'ВЗФЭИ', 
                            310: 'ВорГПУ', 
                            311: 'АдГУ', 
                            312: 'БурГУ', 
                            314: 'ЮРУЭиС', 
                            318: 'ЛитИн', 
                            319: 'ОмскГИС', 
                            321: 'ГАУГН', 
                            330: 'ВятГГУ', 
                            331: 'ГлазГПИ', 
                            332: 'ГрозГНТУ', 
                            333: 'ЕлабГПУ', 
                            334: 'ЕлецГУ', 
                            335: 'ВСГАО', 
                            336: 'ОмскГПУ', 
                            337: 'ИркГЛУ', 
                            338: 'ИшимГПИ', 
                            339: 'ТатГГПУ', 
                            340: 'КалужГУ', 
                            341: 'КамчГУ', 
                            342: 'КЧГУ', 
                            343: 'КарелГПА', 
                            345: 'КомиГПИ', 
                            346: 'АГПГУ', 
                            347: 'КострГУ', 
                            348: 'КрГПУ', 
                            349: 'КурскГУ', 
                            351: 'ЛипГПУ', 
                            352: 'МагнГУ', 
                            353: 'МарГПИ', 
                            354: 'СВГУ', 
                            355: 'МичГПИ', 
                            356: 'МордГПИ', 
                            357: 'МГГумУ', 
                            359: 'МурмГГУ', 
                            360: 'НЧИСПТиР', 
                            361: 'НижГЛУ', 
                            362: 'НижГПУ', 
                            364: 'НТагГСПА', 
                            365: 'КузГПА', 
                            366: 'НовсГПУ', 
                            367: 'ОренГПУ', 
                            369: 'ОрлГУ', 
                            371: 'ПензГПУ', 
                            372: 'ПермГПУ', 
                            373: 'ПоморГУ', 
                            374: 'ПсковГПУ', 
                            375: 'ПятГЛУ', 
                            376: 'РосГПУ', 
                            377: 'РостГПУ', 
                            378: 'РязГУ', 
                            379: 'ПовГСГА', 
                            381: 'СмолГУ', 
                            382: 'СолГПИ', 
                            383: 'СтавГУ', 
                            384: 'СтерГПА', 
                            385: 'ТагГПИ', 
                            386: 'ТобГСПА', 
                            387: 'ТомГПУ', 
                            388: 'ДагГПУ', 
                            389: 'ТулГПУ', 
                            390: 'ТувГУ', 
                            391: 'УлГПУ', 
                            392: 'УрГПУ', 
                            393: 'РосГППУ',
                            394: 'УсГПИ', 
                            395: 'ДВГГумУ', 
                            396: 'ЧелГПУ', 
                            398: 'ЧеченГПИ', 
                            399: 'ЗабГГПУ', 
                            404: 'ЧувГПУ', 
                            405: 'МГЮрА', 
                            406: 'ШадГПИ', 
                            407: 'ШуйГПУ', 
                            408: 'СахГУ', 
                            409: 'ЯрГПУ', 
                            410: 'АрзГПИ', 
                            411: 'ВолгГСПУ', 
                            412: 'АрмГПА', 
                            413: 'ВолжГИПУ', 
                            414: 'АстрГУ', 
                            415: 'ВологГПУ', 
                            418: 'АлтГПА', 
                            419: 'БашГПУ', 
                            420: 'БелГУ', 
                            421: 'АлтГАО', 
                            422: 'ПриамГУ', 
                            423: 'БирскГСПА', 
                            424: 'БлагГПУ', 
                            425: 'БорисГПИ', 
                            426: 'БрянГУ', 
                            427: 'ВладГГУ', 
                            441: 'ГосИРЯП', 
                            448: 'КазГЭУ', 
                            456: 'ГПолАк', 
                            465: 'СПбГУСЭ', 
                            477: 'ОрГИМ', 
                            481: 'РАрмСлУ', 
                            482: 'ПовГУС', 
                            484: 'УфГАЭиС', 
                            501: 'ГжГХПИ', 
                            502: 'ПенГТхнА', 
                            503: 'ПятГГТхУ', 
                            504: 'СнКГПИ', 
                            505: 'ЮгорГУ', 
                            506: 'ПсковГПИ', 
                            507: 'ВШНИ', 
                            509: 'КрГТЭИ', 
                            511: 'НижКИ', 
                            512: 'ОрлГИЭТ', 
                            513: 'РСТЭУ', 
                            514: 'СПбГТЭУ', 
                            601: 'РГСУ', 
                            609: 'ЯкГИТИ', 
                            610: 'СахаГПА', 
                            700: 'ПсковГУ'
                            }