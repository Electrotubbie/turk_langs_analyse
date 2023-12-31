import pandas as pd
import fasttext
from razdel import sentenize
from data_preprocessing import *

model = fasttext.load_model('./pyfasttext/models/lid.176.bin')
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

# удаляем пропуски из предложений и разместим из в отдельных списках
def drop_dup_none(df):
    df['list_in_list_without_none'] = pd.NA
    for i, row in df.iterrows():
        list_in_list_without_none = list()
        # создали новый список куда будем складывать предложения
        new_list_content = list()
        content = row['only_turk_content']
        if content is not None:
            for j in range(0,len(content)):
                sent = content[j]
                # Если стоит нон, то сделай список чистым
                if sent is None:
                    # положи список предложений в глобальный список и очисти список
                    list_in_list_without_none.append(new_list_content)
                    new_list_content = list()
                # Если есть предложение положи его в в список
                else:
                    # если это последнее редложение то добавь его в список и список добавь в глобальный список
                    if j == len(content)-1:
                        new_list_content.append(sent)
                        list_in_list_without_none.append(new_list_content)
                    else:
                        new_list_content.append(sent)
            df.at[i, 'list_in_list_without_none'] = list_in_list_without_none
# load file
df = pd.read_csv('clear_re_text (ba).csv')
# del old index
del df['Unnamed: 0']
# return dict after fastext 6 columns
sentenize_and_predict(df)

# creat list sent for P_valid with none, 7 columns
create_only_turk_text_list(df)
# даляем пропуски
drop_dup_none(df)