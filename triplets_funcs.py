from math import factorial
import numpy as np
from razdel import sentenize

K = 0.2 # the maximum deviation in the length of the sentence relative to the one under consideration
MIN_L_SENT = 30 # maximum sentence length
MAX_L_SENT = 100 # minimum sentence length

def sentenize_text_to_list(text: str) -> list:
    '''
    The function returns a list of sentences from the source text.
    The text is processed through the sentenize function.
    '''
    
    return [list(sentence)[2] for sentence in list(sentenize(text))]

def check_text_type(text: str | list) -> list:
    '''
    The function is a handler for the text received as input.
    '''

    if type(text) == str:
        splitted_text = sentenize_text_to_list(text)
    elif type(text) == list:
        splitted_text = text
    else:
        raise TypeError(f'The function should accept only list or std as input, but has adopted a {type(text)}')
    return splitted_text

def find_triplet(text: str | list) -> tuple:
    '''
    The function of searching for a triplet in the text according to the following conditions:
        MIN_L_SENT <= average sentence length in a triplet <= MAX_L_SENT.
    After finding sentences with suitable lengths, 
    the triplet sentences are checked for approximately the same length 
    relative to the deviation coefficient K.

    If the function finds a triplet in the list of sentences, 
    it returns a tuple (triplet, the remaining text after the triplet).

    If the function does not find a triplet in the list of sentences, it returns a tuple (None, None)
    '''

    splitted_text = check_text_type(text) # preparing the list of sentences
    i = 0
    while i < len(splitted_text)//3 * 3: # 
        triplet = splitted_text[i:i+3] #
        if len(triplet) < 3:
            # If the slice length is less than 3, 
            # then this means it is the tail of the list and there is nothing left to return.
            return (None, None)
        if None in triplet:
            # If the triplet contains a deleted sentence, then this triplet must be skipped. 
            i += 1
        else:
            # In this code block, the triplet is checked for the average length of sentences, 
            # and for the relative deviation of sentences.
            mean_lenth = float(np.array([len(elem) for elem in triplet]).mean())
            if mean_lenth >= MIN_L_SENT and mean_lenth <= MAX_L_SENT:
                # calculation of deviations relative to the average length of sentences
                sent_deviations = [abs(1 - len(sent)/mean_lenth) for sent in triplet]
                if max(sent_deviations) <= K:
                    # if the deviations are in order, then this is an "equidistant" triplet
                    return (triplet, splitted_text[i+3:])
                else:
                    # if the triplet is not "equidistant", then proceed to the next combination
                    i += 1
            else:
                # if the triplet does not pass according to the length condition, 
                # then proceed to the next combination
                i += 1
    else:
        # if the loop ended unsuccessfully (as a result, nothing was returned), 
        # then the function returns an empty tuple
        return (None, None)

def find_all_triplets(text: str | list):
    '''
    A function to search for all triplets in the text.
    Using the find_triplet function, all valid triplets in the text are searched.
    '''

    splitted_text = check_text_type(text) # preparing the list of sentences
    triplets = list()
    while splitted_text:
        (triplet, splitted_text) = find_triplet(splitted_text)
        if triplet:
            triplets.append(triplet)
    return triplets

def shuffle_triplet_SOP(triplet: list) -> list | None:
    '''
    A function for getting all possible combinations inside a single triplet.
    How it works:
    - The function accepts a list of 3 sentences as input;
    - The first combination is the original triplet ;
    - Other combinations are created in the 'for' loop;
    Example of generating:

    >>> triplet = ['sent1', 'sent2', 'sent3']
    >>> shuffle_triplet_SOP(triplet)
    [('sent1 sent2 sent3', True), 
    ('sent1 sent3 sent2', False),
    ('sent3 sent1 sent2', False), 
    ('sent3 sent2 sent1', False), 
    ('sent2 sent3 sent1', False), 
    ('sent2 sent1 sent3', False)]
    
    You may see that on 1 iteration replaced sent2 and sent3, on second iteration replaced sent3 and sent1.
    '''

    if len(triplet) == 3:
        combinations = [(' '.join(triplet), True)] # the first triplet is obviously correct
        combination = triplet
        for i in range(1, factorial(3)):
            if i % 2 == 1: # replace in triplet 2 and 3 sentences
                combination = [combination[0], combination[2], combination[1]]
            elif i % 2 == 0: # replace in triplet 1 and 2 sentences
                combination = [combination[1], combination[0], combination[2]]
            combinations.append((' '.join(combination), False)) # adding a 'False' triplet to the list of combinations
        return combinations
    else:
        print(f'This is not a triplet: {triplet}')
        return None

def generate_triplets_SOP(text: str | list) -> list | None:
    '''
    A function for getting all possible triplets and their combinations from the text.
    For SOP tasks, it is enough to simply find triplets and mix sentences inside them.
    '''

    if text:
        splitted_text = check_text_type(text) # preparing the list of sentences
        triplets = find_all_triplets(splitted_text)
        shuffled_triplets = list()
        for triplet in triplets:
            shuffled = shuffle_triplet_SOP(triplet)
            shuffled_triplets.append(shuffled)
        return shuffled_triplets
    else:
        return None

def shuffle_triplet_NSP(triplet: list, sentence: str) -> list:
    '''
    A function for getting combinations of a triplet and another sentence.
    Combinations are joins by whitespaces.

    Example:

    >>> triplet = ['sent1', 'sent2', 'sent3']
    >>> sentence = 'other_sent'
    >>> shuffle_triplet_NSP(triplet, sentence)
    [('sent1 sent2 sent3', True), 
    ('other_sent sent2 sent3', False), 
    ('sent1 other_sent sent3', False), 
    ('sent1 sent2 other_sent', False)]
    '''

    combinations = [(' '.join(triplet), True)] # the first triplet is obviously correct
    combination = str()
    for i in range(len(triplet)):
        combination = triplet.copy() 
        combination[i] = sentence # replacing the offer with the offer we need
        combinations.append((' '.join(combination), False)) # adding a 'False' triplet to the list of combinations
    return combinations

def generate_triplets_NSP(text: str | list) -> list | None:
    '''
    A function for getting possible triplets and their combinations with suitable sentences from the text.
    '''
    
    if text:
        splitted_text = check_text_type(text) # preparing the list of sentences
        shuffled_triplets = list()
        while splitted_text:
            (triplet, splitted_text) = find_triplet(splitted_text)
            if triplet:
                # calculating the average length of sentences from triplets
                mean_lenth = float(np.array([len(elem) for elem in triplet]).mean())
                # search for a suitable offer
                for i_sent, sent in enumerate(splitted_text):
                    if sent:
                        # checking a sentence for deviation
                        if abs(1 - len(sent)/mean_lenth) <= K:
                            shuffled = shuffle_triplet_NSP(triplet, sent)
                            shuffled_triplets.append(shuffled)
                            splitted_text[i_sent] = None
                            break
            else:
                break
        return shuffled_triplets
    else:
        return None
