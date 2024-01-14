import re
from regulars import REGULARS

def check_for_regs(text, show=False):
    '''
    Cleaning the text from the regular expressions presented in the list of REGULARS.
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
    '''
    Adding spaces to dots without spaces at the end of sentences.
    '''
    bad_dot = r'[а-яәүһҙҫөңғҡқіғұәөҺҗ]\.[0-9А-ЯҚӘҒҢӨҮІҰҖ#]'
    all = re.findall(bad_dot, text)
    if all != []:
        for elem in all:
            text = text.replace(elem, elem.replace('.', '. '))
        if show:
            print(f'Delete all bad dots: {all}')
    return text

def check_for_smiles(text, show=False):
    '''
    Removing emoticons and other unicode characters.
    '''

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
    '''
    Cleaning the text from multiple spaces.
    '''
    
    return re.sub(r'[ _\t]+', ' ', text)

def text_preprocessing(text, show=False):
    # PIPLINE
    text = check_for_regs(text, show)
    text = check_for_smiles(text, show)
    text = check_for_bad_dots(text, show)
    text = remove_dup_spaces(text)
    return text