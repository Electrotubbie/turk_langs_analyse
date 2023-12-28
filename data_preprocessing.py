import pandas as pd
import re

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

# lang;category;text_dirty;url;data

def check_for_regs(text, show=False):
    '''

    '''
    for sign in REGULARS:
        for reg in sign['regulars_list']:
            all = re.findall(reg, text)
            if all != []:
                text = re.sub(reg, sign['sign_to_replace'], text)
                if show:
                    print(f'Delete {all}')
    return text

def check_for_bad_dots(text, show=False):
    bad_dot = r'[а-яәүһҙҫөңғҡқіғұәөҺҗ]\.[0-9А-ЯҚӘҒҢӨҮІҰҖ#]'
    all = re.findall(bad_dot, text)
    if all != []:
        for elem in all:
            text = text.replace(elem, elem.replace('.', '. '))
        if show:
            print(f'Delete all bad dots: {all}')
    return text

def check_for_smiles(text, show=False):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    all = regrex_pattern.findall(text)
    if show and all != []:
        print(f'Delete all smiles: {all}')
    return regrex_pattern.sub(r'',text)

def remove_dup_spaces(text):
    return re.sub(r'[ _\t]+', ' ', text)

def text_preprocessing(text, show=False):
    text = check_for_regs(text, show)
    text = check_for_smiles(text, show)
    text = check_for_bad_dots(text, show)
    text = remove_dup_spaces(text)
    return text