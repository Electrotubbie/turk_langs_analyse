REGULARS_TO_NOTHING = [
    r'http[s]?\:\/\/[A-z-a-z-а-я\-0-9\.]{1,20}.[comrupnewskzg][\/]?[^\s@]+',
    r'[A-z-а-я-0-9\-\.@]{2,60}\.[comrupkz]{2,3}[^\s@]*', # www.kkfjsd.ru
    r'Автор[ы]?\:[\s]?[А-Я-а-яәүһҙҫөңғҡқіғҚұӘҒҢӨҮәөҺІҰҖҗ]+[\s\.]+[А-Я-а-яәүһҙҫөңғҡқіғҚұӘҒҢӨҮәөҺІҰҖҗ]+',# Автор: Галина Бланка
    r'Фото[:][\s]?[А-Я]{1}[а-я-яәүһҙҫөңғҡқіғҚұӘҒҢӨҮәөҺІҰҖҗ]{2,15}\s[А-Я]{1}[А-я-яәүһҙҫөңғҡқіғҚұӘҒҢӨҮәөҺІҰҖҗ]{2,15}',# Фото: Рәмил Нафиҡов
    r'Видео[:][\s]?[А-Я]{1}[а-я-яәүһҙҫөңғҡқіғҚұӘҒҢӨҮәөҺІҰҖҗ]{2,15}\s[А-Я]{1}[А-я-яәүһҙҫөңғҡқіғҚұӘҒҢӨҮәөҺІҰҖҗ]{2,15}',  # Видео: Галина Бланка
    r'Фото[:][\s]?[А-Я-яәүһҙҫөңғҡқіғҚұӘҒҢӨҮәөҺІҰҖҗ]{1}[\.]?[\s]?[А-яәүһҙҫөңғҡқіғҚұӘҒҢӨҮәөҺІҰҖҗ]{1}[а-яәүһҙҫөңғҡқіғҚұӘҒҢӨҮәөҺІҰҖҗ]{1,15}', # Фото: Г. Бланка Фото: Г. Бланка
    r'Автор\s[\bфото|\bвид]{3}[а-яәүһҙҫөңғҡқіғҚұӘҒҢӨҮәөҺІҰҖҗ]{1,}', #Автор (фото)видеояҙмаһы
    r'Автор фото-видеолары', # Автор фото-видеолары
    r'[А-Я]*[\s\.][А-Я]*\.Фото[:|\s]*[\w+]*\.[comrup]*',
    r'[Тт]ел[фон|\.]?\/факс[:]?', # Тел./факс Тел/факс:
    r'[Тт]елеф[а-яәүһҙҫөңғҡқіғҚұӘҒҢӨҮәөҺІҰҖҗ]{1,10}[:]', # Телефондар: Телефон
    r'[Тт]ел[\.]', # Тел.
    r'[+]?[7|8][\s]?\([0-9]{3,5}\)[\s]?[0-9]{3,5}[-|\s]?[0-9]{2}[-|\s]?[0-9]{2}', # 8 (347) 289-65-50
    r'8?[-|\s]?\([0-9]{3,5}\)[-\s]?[0-9]{1,5}[-\s]?[0-9]{1,5}[-|\s]?[0-9]{1,2}', # 8 (34767) 6-61-2 , (34786) 3-23-02
    r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', #+7 926 123 45 67 , 8(926)123-45-67
    r'\xa0',
    r'\u200b',
    r'\xad',
    r'Фото, видео:',
    r'yandex.ru',
    r'Фото: видеонан скриншот',
    r'Источник:',
    r'\b8[-\s][0-9]{3}[-\s][0-9]{2,3}[-\s][0-9\-]{1,6}', # 8 800 100 000  8-964-96-08-462
    r'ФОТО:',
    r'\b8[0-9]{3}[-\s][0-9]{3}[-\s][0-9\-]{5}', # 8965-666-20-68
    r'Дереккөз:',
    r'Булак:',
    r'[Дд]зен[:]?',
    r'[KAZ\.]?NUR\.KZ',
    r'SUPER.KG'
]

REGULARS = [
    {'sign_to_replace': '', 'regulars_list': REGULARS_TO_NOTHING}
]