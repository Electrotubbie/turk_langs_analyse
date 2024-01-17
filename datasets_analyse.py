import pandas as pd
import fasttext
from razdel import sentenize
from data_preprocessing import *

model = fasttext.load_model('./models/lid.176.bin')
valid_language_set = tuple(['ba', 'kk', 'tt', 'ky', 'tr', 'az', 'tk', 'uz', 'ug', 'cv', 'krc'])

def sentenize_and_predict(df, content='content'):
    '''
    As input, the function accepts a DataFrame and a column from the dataframe with the text that needs to be worked out.
    The function returns a similar dataframe to the output, 
    but with a new column 'sentenсes' containing the text after preprocessing and its parameters.

    Preparation of sentences from the text for analysis into the language we need. 
    The purpose of the function is to divide the text into a list of sentences, while preprocessing the text, 
    removing unnecessary elements according to the functions: remove_dup_spaces, check_for_bad_dots and text_preprocessing. 
    Also, in the process of creating a list, a dictionary of the following type is formed for each sentence:
    {
        'index': sentece number,
        'text': sentece text,
        'predict': fasttext predict к=3,
        'predict_add':{ # additional probability
            'turk': P_only_turk, # the probability of the Turkic language
            'other': P_other_lang # the probability of the non Turkic language
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
            sentence_params['index'] = sentence_i # sentece number
            sentence_params['text'] = sentence # sentece text
            sentence_params['predict'] = model.predict(sentence, k=3) # fasttext predict к=3
            sentence_params['predict_add'] = { # additional probability
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

def create_only_turk_text_list(df, column = 'sentenсes', P_valid = 0.3, drop_small = True, small_text_range = 3):
    '''
    As input, the function accepts a DataFrame and a column from the dataframe with the list of sentences that needs to be worked out.
    Also the function accepts the following parameters:
     - P_valid = 0.3 - the probability specified by the fasttext module, above which the text was recognized as Turkic;
     - drop_small = True - a flag that allows you to delete lists that are too small relative to the small_text_range parameter, obtained as a result;
     - small_text_range = 3 - the length of the resulting list, below which the list is considered invalid and is designated as None and subsequently drop.
    As output, the function returns a data frame with a new column 'only_turk_content', which contains text only in the Turkic language and 
    None elements that show that some sentences have been deleted from this text.
    
    Checking sentences that match the language in question according to the prediction of the fasttext module. 
    Also, if the probability is less than or equal to P_valid, then a check is performed on the sentences in the text standing before and after.
    '''

    df['only_turk_content'] = pd.NA
    df['processed'] = False
    none_rows = list()
    for i, row in df[:].iterrows():
        text = [None]
        text_list = row[column]
        for j, sent in enumerate(text_list):
            # the check for P_valid is performed here 
            if sent['predict_add']['turk'] > P_valid:
                text.append(sent['text'])
            else:
                # the try except construct is executed in order not to get an exception on the last element of the list 
                try:
                    # here, the sentences in the text are checked before and after the sentence in question
                    if (text_list[j-1]['predict_add']['turk'] > P_valid and # проверка обособленных
                    text_list[j+1]['predict_add']['turk'] > P_valid and
                    sent['predict_add']['turk'] <= P_valid):
                        text.append(sent['text'])
                    else:
                        # if one of the sentences does not meet the conditions, then mark the text as 'processed'
                        df.at[i, 'processed'] = True
                        if text[-1] != None:
                            text.append(None)
                except:
                    # if one of the sentences does not meet the conditions, then mark the text as 'processed'
                    df.at[i, 'processed'] = True
                    if text[-1] != None:
                        text.append(None)
        text = list_strip_none(text) # delete all None items at the beginning and end of the list
        # check for small text range
        if len(text) < small_text_range:
            none_rows.append(i)
        # checking for the absolute absence of Turkic sentences
        for sent in text:
            if sent:
                df.at[i, 'only_turk_content'] = text
                break
        else:
            df.at[i, 'only_turk_content'] = None
            none_rows.append(i)
    # deleting dataset lines that do not contain the text that suits us
    if drop_small:
        df = df.drop(none_rows).reset_index(drop=True)
    return df

def join_with_none(splitted_text: list, sep=' '):
    '''
    A function like 'join' is built into python, but accepts lists with None elements.
    '''
    join_text = str()
    for sent in splitted_text:
        if sent:
            join_text += sent + sep
    return join_text.strip()

def list_strip_none(list_with_none):
    '''
    The function removes all None items from the beginning and end of the list
    '''
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