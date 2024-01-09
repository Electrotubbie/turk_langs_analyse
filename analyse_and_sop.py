import pandas as pd
import numpy as np
import random
import fasttext
from razdel import sentenize
import re
df = pd.read_csv('/content/drive/MyDrive/only_turk_content.csv')
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

model = fasttext.load_model('/content/drive/MyDrive/pyfasttext/lid.176.bin')
valid_language_set = tuple(['ba', 'kk', 'tt', 'ky', 'tr', 'az', 'tk', 'uz', 'ug', 'cv', 'krc'])

def sentenize_and_predict(df, content='content'):
    '''
    {
        'index': номер предложения,
        'text': текст предложения,
        'predict': предсказание фасттекста к=3,
        'predict_add':{
            'turk': P_only_turk, вероятность тюркских языков
            'other': P_only_turk вероятность тюркских языков
        }
    }
    '''
    df['sentenсes'] = pd.NA
    for i, row in df.iterrows():
        senteces = list()
        new_text = remove_dup_spaces(check_for_bad_dots(row[content].replace('\n', ''), show=True))
        dirty_splitted_text = [list(sentence)[2] for sentence in list(sentenize(new_text))]
        splitted_text = [text_preprocessing(sentence, show=True) for sentence in dirty_splitted_text]
        for sentence_i, sentence in enumerate(splitted_text):
            sentence_params = dict()
            sentence_params['index'] = sentence_i
            sentence_params['text'] = sentence
            sentence_params['predict'] = model.predict(sentence, k=3)
            sentence_params['predict_add'] = {
                'turk': 0,
                'other': 0
            }
            predict_add = model.predict(sentence, k=20)
            for i_lang, lang in enumerate(predict_add[0]):
                if lang.replace('__label__', '') in valid_language_set:
                    sentence_params['predict_add']['turk'] += predict_add[1][i_lang]
                elif lang.replace('__label__', '') not in valid_language_set:
                    sentence_params['predict_add']['other'] += predict_add[1][i_lang]
            sentence_params['lenth'] = len(sentence)
            senteces.append(sentence_params)
        df.at[i, 'sentenсes'] = senteces
    return df

def create_only_turk_text_list(df, P_valid = 0.3):
    # СОЗДАНИЕ СПИСКА ПРЕДЛОЖЕНИЙ, КОТОРЫЕ ПОДХОДЯТ ПО P_valid, не подходящие будут None в списке
    df['only_turk_content'] = pd.NA
    none_cols = list()
    for i, row in df[:].iterrows():
        text = list()
        text_list = row.sentenсes
        for j, sent in enumerate(text_list):
            if sent['predict_add']['turk'] > P_valid:
                text.append(sent['text'])
            else:
                try:
                    if (text_list[j-1]['predict_add']['turk'] > P_valid # проверка обособленных
                    and text_list[j+1]['predict_add']['turk'] > P_valid
                    and sent['predict_add']['turk'] <= P_valid):
                        text.append(sent['text'])
                    else:
                        text.append(None)
                except:
                        text.append(None)
        text = list_strip_none(text)
        # если нет тюркских предложений вообще
        if len(text) < 3:
            none_cols.append(i)
            print(f'Маленькое')
        for sent in text:
            if sent:
                df.at[i, 'only_turk_content'] = text
                break
        else:
            df.at[i, 'only_turk_content'] = None
            none_cols.append(i)
    df = df.drop(none_cols).reset_index(drop='index')
    return df

def join_with_none(splitted_text: list, sep=' '):
    join_text = str()
    for sent in splitted_text:
        if sent:
            join_text += sent + sep
    return join_text.strip()

def list_strip_none(list_with_none):
    l = 0 # левая граница
    r = len(list_with_none) # правая граница
    for i, elem in enumerate(list_with_none):
        if elem:
            l = i
            break
    for i, elem in enumerate(list_with_none[::-1]):
        if elem:
            r -= i + 1
            break
    return list_with_none[l:r]
def drop_dup_none(df):
    df['list_in_list_without_none'] = pd.NA
    for i, row in df.iterrows():
        list_in_list_without_none = list()
        # создали новый список куда будем складывать предложения
        new_list_content = list()
        content = row['only_turk_content']
        if content is not None:
            for j in range(0,len(content)):
                # print(j)
                sent = content[j]
                # print('DLINNA',len(content))
                # Если стоит нон, то сделай список чистым
                if sent is None:
                    # print('NONE IN SENT',i, sent)
                    # положи список предложений в глобальный список и очисти список
                    list_in_list_without_none.append(new_list_content)
                    new_list_content = list()
                # Если есть предложение положи его в в список
                else:
                    # если это последнее предложение то добавь его в список и список добавь в глобальный список
                    if j == len(content)-1:
                        # print('POSLEDNEE SENT',j, sent)
                        new_list_content.append(sent)
                        list_in_list_without_none.append(new_list_content)
                    else:
                        new_list_content.append(sent)
            # print('ITOG',list_in_list_without_none)
            df.at[i, 'list_in_list_without_none'] = list_in_list_without_none
            # print(df['list_in_list_without_none'])
        else:
            df.at[i, 'list_in_list_without_none'] = None
    def clear_list_in_none(df):
        for i, row in df.iterrows():
            # print(i, type(row.list_in_list_without_none))
            if row.list_in_list_without_none is not None:
                clear_list = list()
                for item in row.list_in_list_without_none:
                    if item == []:
                        pass
                    else:
                            clear_list.append(item)
                df.at[i, 'list_in_list_without_none'] = clear_list
            else:
                df.at[i, 'list_in_list_without_none'] = None
    clear_list_in_none(df)

# [['sent_1','sent_2', 'sent_3'],[],['sent_4', 'sent_5', 'sent_6']]
#Убрали пустые списки из list_in_list_without_none
df_triplet = pd.DataFrame()
def create_triplet(sent_list):
    df_triplet['triplet'] = pd.NA
    df_triplet['splitted_text'] = pd.NA
    df_triplet['all_sent'] = pd.NA
    # print(df_triplet)
    K = 0.2 # максимальное отклонение по длине предложения относительно рассматриваемого
    MIN_L_SENT = 30
    MAX_L_SENT = 100
    for j in sent_list:
        # сейчас находимся в [['ssent'], ['sent','sent']]
        if j is not None:
            for splitted_text in j:
                # print(splitted_text)
                # зашли в список внутри большого списка
                if len(splitted_text)>= 3:
                    # print(splitted_text)
                #     #  проверяем на количество предложений внутри списка, если предложений больше чем 3 то работает с ним, если меньше то уходим
                    i = 0
                    triplet_list = []
                    for  i in range(0, len(splitted_text)):
                        # print('сколько предложений', len(splitted_text), 'на каком мы сейчас', i)
                        triplet = splitted_text[i:i+3]
                        # print(i)
                        if i == (len(splitted_text)-1) or i == (len(splitted_text)-2): # если i равна поелденему или предпоследнему предложению, ничего не происходит
                            # print(i, len(splitted_text))
                            pass
                        else: # если предложение не последнее
                            mean_lenth = float(np.array([len(elem) for elem in triplet]).mean())
                            if mean_lenth >= MIN_L_SENT and mean_lenth <= MAX_L_SENT:
                                sent_deviations = [abs(1 - len(sent)/mean_lenth) for sent in triplet]
                                if max(sent_deviations) <= K: # если отклонения в порядке, то это "равнодлинный" триплет
                                    text = splitted_text[i+3:]

                                    df_triplet.loc[len(df_triplet.index)] = [triplet, text, splitted_text]

    return df_triplet


def shuffle_triplet_SOP(df):
    df_triplet['SOP_triplet'] = pd.NA
    for j,row in df.iterrows():
        triplet = row.triplet.copy()
        # print(triplet)
        combinations = [(triplet, True)] # исходный триплет заведомо верный
        combination = triplet.copy()
        while combination == triplet:
            random.shuffle(combination)
            # print(combination == triplet, combination)
        print(combination == triplet, combination)
        df.at[j, 'SOP_triplet'] = combination
    return df




sentenize_and_predict(df)
create_only_turk_text_list(df)
drop_dup_none(df)
create_triplet(df.list_in_list_without_none)
shuffle_triplet_SOP(df_triplet)