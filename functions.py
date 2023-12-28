from math import factorial
import numpy as np
from razdel import sentenize

K = 0.2 # максимальное отклонение по длине предложения относительно рассматриваемого
MIN_L_SENT = 30
MAX_L_SENT = 100

# [sent1, sent2, sent3, sent4, sent5, ...]
# [sent1, sent2, sent3, sent5, ...] vs [sent1, sent2, sent3, None, sent5, ...]
# 
# [sent1, sent2, sent3, None, sent5, ...]

def sentenize_text_to_list(text: str) -> list:
    '''
    Разбивка текста на предложения с помощью метода 
    sentenize библиотеки razdel.
    '''
    return [list(sentence)[2] for sentence in list(sentenize(text))]

def find_triplet(text: str | list) -> tuple:
    '''
    Функция для поиска триплета в тексте.
    '''
    if type(text) == str:
        splitted_text = sentenize_text_to_list(text)
    elif type(text) == list:
        splitted_text = text
    else:
        raise TypeError('Функция должна принимать на вход только list или str, а приняла {type(text)}')

    i = 0
    while i < len(splitted_text)//3 * 3:
        triplet = splitted_text[i:i+3]
        if len(triplet) < 3:
            return (None, None) # если цепляется хвост из последних двух предложений, то это конец цикла
        if None in triplet:
            i += 1 # None
        else:
            mean_lenth = float(np.array([len(elem) for elem in triplet]).mean())
            if mean_lenth >= MIN_L_SENT and mean_lenth <= MAX_L_SENT:
                # расчёт отклонений относительно средней длины предложений
                sent_deviations = [abs(1 - len(sent)/mean_lenth) for sent in triplet]
                if max(sent_deviations) <= K: # если отклонения в порядке, то это "равнодлинный" триплет
                    return (triplet, splitted_text[i+3:])
                else: # иначе пропускаем предложение и идём дальше
                    i += 1
            else:
                i += 1
    else:
        return (None, None)

def find_all_triplets(text: str | list):
    '''
    Функция для поиска всех триплетов в тексте.
    '''
    if type(text) == str:
        splitted_text = sentenize_text_to_list(text)
    elif type(text) == list:
        splitted_text = text
    else:
        raise TypeError(f'Функция должна принимать на вход только list или str, а приняла {type(text)}')
    
    triplets = list()
    while splitted_text:
        (triplet, splitted_text) = find_triplet(splitted_text)
        if triplet:
            triplets.append(triplet)
    return triplets

def shuffle_triplet_SOP(triplet: list) -> list:
    '''
    Получение всех размещений предложений в триплете.
    '''
    combinations = [(' '.join(triplet), True)] # исходный триплет заведомо верный
    combination = triplet
    for i in range(1, factorial(3)):
        if i % 2 == 1: # смена в триплете второй пары a B C
            combination = [combination[0], combination[2], combination[1]]
        elif i % 2 == 0: # смена в триплете первой пары A B c
            combination = [combination[1], combination[0], combination[2]]
        combinations.append((' '.join(combination), False)) # добавление заведомо ложного триплета
    return combinations

def generate_triplets_SOP(text: str | list) -> list:
    '''
    Функция для получения возможных триплетов и их комбинаций из текста.
    '''
    if text == None:
        return []
    
    triplets = find_all_triplets(text)
    shuffled_triplets = list()
    for triplet in triplets:
        shuffled = shuffle_triplet_SOP(triplet)
        shuffled_triplets.append(shuffled)
    return shuffled_triplets

def shuffle_triplet_NSP(triplet: list, sentence: str) -> list:
    '''
    Функция для получения комбинаций триплета и входного предложения, например
    triplet - abc, sentence - s
    abc True
    sbc False
    asc False
    abs False
    '''
    combinations = [(' '.join(triplet), True)]
    combination = str()
    for i in range(len(triplet)):
        combination = triplet.copy() 
        combination[i] = sentence # замена предложения на необходимое нам предложение
        combinations.append((' '.join(combination), False)) # добавление заведомо ложного триплета
    return combinations

def generate_triplets_NSP(text: str | list) -> list:
    '''
    Функция для получения возможных триплетов и их комбинаций с предложениями из текста.
    '''
    if text == None:
        return []
    
    if type(text) == str:
        splitted_text = sentenize_text_to_list(text)
    elif type(text) == list:
        splitted_text = text
    else:
        raise TypeError('Функция должна принимать на вход только list или str')
    
    shuffled_triplets = list()
    while splitted_text:
        (triplet, splitted_text) = find_triplet(splitted_text)
        if triplet:
            # расчёт средней длины предложений из триплетов
            mean_lenth = float(np.array([len(elem) for elem in triplet]).mean())
            # поиск подходящего предложения
            for i_sent, sent in enumerate(splitted_text):
                # проверка предложения на отклонение
                if sent:
                    if abs(1 - len(sent)/mean_lenth) <= K:
                        shuffled = shuffle_triplet_NSP(triplet, sent)
                        shuffled_triplets.append(shuffled)
                        splitted_text[i_sent] = None
                        break
        else:
            break
    return shuffled_triplets
