# [EN](README.md/#analysis-of-turkic-sentences) | [RU](README.md/#анализ-тюркских-предложений)

# Analysis of Turkic sentences

## Description

The functions in these files were used to analyze and prepare datasets with news in Bashkir, Kazakh and Kyrgyz languages.

## Datasets

Here you can view the received datasets:
- [classification of Turkic languages](https://huggingface.co/datasets/Electrotubbie/classification_Turkic_languages)
- [Triplets for Turkic languages language models](https://huggingface.co/datasets/Electrotubbie/triplets_Turkic_languages)

## How to use

In order to use the code from these files, you must:

Install the necessary libraries:
```shell
pip install -r requirements.txt
```
Copy the necessary files to the folder with your project.

Import files into your python code, for example:
```python
import data_preprocessing
import datasets_analyse
import triplets_funcs
```

## Description of the files

A detailed description of each function can be read directly inside the files.

### [data_preprocessing.py](data_preprocessing.py)

The functions in this file were used to clean the text from unnecessary information, such as phone numbers, links to websites, links to photos and other constructions described by regular expressions in the file [regulars.py](regulars.py).
Also, thanks to the functions in these files, you can perform the following actions:
- **check_for_bad_dots** - adding spaces, if they are missing in the text after the dots at the ends of sentences;
- **check_for_smiles** - cleaning text from unicode characters such as emoticons and various special characters;
- **remove_dup_spaces** - removing multiple spaces and indents, as well as replacing them with a single space;
- **text_preprocessing** is a pipeline that was used by the authors to preprocess text in datasets.

### [regulars.py](regulars.py)

This file contains a list of regular expressions used to clean texts in the dataset from unnecessary constructions. A detailed application can be viewed in the file [data_preprocessing.py](data_preprocessing.ру).

### [datasets_analyse.py](datasets_analyse.py)

This file describes the functions that have been applied to the dataset for preprocessing and validating text, checking it for belonging to a variety of Turkic languages using the [fasttext](https://fasttext.cc/) module and their models for identifying the language of the text [lid.176.bin](https://fasttext.cc/docs/en/language-identification.html) [[1]](README.md/#references).

The file contains the following functions:
- **sentenize_and_predict** - the function contains text preprocessing using functions from the file [data_preprocessing.py](data_preprocessing.py), decomposing the text into a list of sentences and describing the parameters of these sentences using the model from [fasttext](https://fasttext.cc/). You can learn more about the function in the file [datasets_analyse.py](datasets_analyse.py);
- **create_only_turk_text_list** - this function is designed to remove unnecessary sentences (extensions **not** in Turkic languages) from the list of sentences with parameters in the dictionary created using the **sentenize_and_predict** function.

As well as auxiliary functions:
- **join_with_none** - the function pursues the same goals as the built-in Python function [**join**](https://docs.python.org/3/library/stdtypes.html?highlight=str%20join#str.join), but ignores **None** in the lists, if they are present; 
- **list_strip_none** - deleting at the beginning and end of the list of items **None**.

### [triplets_funcs.py](triplets_funcs.py)

Main functions:
- **generate_triplets_NSP** - a function for getting possible triplets and their combinations with suitable sentences from the text;
- **shuffle_triplet_NSP** - a function for getting combinations of a triplet and another sentence;
- **generate_triplets_SOP** - A function for getting all possible triplets and their combinations from the text. For SOP tasks, it is enough to simply find triplets and mix sentences inside them.
- **shuffle_triplet_SOP** - a function for getting all possible combinations inside a single triplet;
- **find_all_triplets** - a function to search for all triplets in the text. Using the **find_triplet** function, all valid triplets in the text are searched.
- **find_triplet** - a function for searching for the first triplet in the text you are looking for according to certain conditions for the maximum and minimum sentence length, as well as the relative deviation of sentence lengths (for more information on how this function works, see [triplets_funcs.py](triplets_funcs.py))

Auxiliary functions:
- **sentenize_text_to_list** - used to convert text of type **str** to **list[str]** using the module [**razdel**](https://natasha.github.io/razdel/) and the function [**sentenize**](https://github.com/natasha/razdel?tab=readme-ov-file#usage);
- **check_text_type** - used to check the input data and follow up with them. If an object of the **list** type arrives at the input, then nothing will happen to the data. If an object of type **str** is received as input, this text will be converted to **list[str]** via the **sentenize_text_to_list** function.

# References

[1] A. Joulin, E. Grave, P. Bojanowski, T. Mikolov, [Bag of Tricks for Efficient Text Classification](https://arxiv.org/abs/1607.01759)

# Анализ тюркских предложений

## Описание

Функции в данных файлах были применены для анализа и подготовки датасетов с новостями на башкирском, казахском и киргизском языках.

## Датасеты

Здесь вы можете ознакомиться с полученными датасетами:
- [classification of Turkic languages](https://huggingface.co/datasets/Electrotubbie/classification_Turkic_languages)
- [Triplets for Turkic languages language models](https://huggingface.co/datasets/Electrotubbie/triplets_Turkic_languages)

## Как использовать функции

Для того, чтобы использовать код из данных файлов, необходимо:

Установить необходимые библиотеки:
```shell
pip install -r requirements.txt
```

Скопировать необходимы файлы в папку с вашим проектом.

Импортировать файлы в ваш python код, например:
```python
import data_preprocessing
import datasets_analyse
import triplets_funcs
```

## Описание файлов

Подробное описание каждой функции можно прочитать непосредственно внутри файлов.

### [data_preprocessing.py](data_preprocessing.py)

Функции в данном файле были применены для чистки текста от лишней информации, такой как номера телефонов, ссылки на веб-сайты, ссылки на фото и прочие конструкции, описанные регулярными выражениями в файле [regulars.py](regulars.py).
Также благодаря функциям в данных файлах можно выполнить следующие действия:
- **check_for_bad_dots** - добавление пробелов, в случае их отсутствия в тексте после точек в концах предложений;
- **check_for_smiles** - чистка текста от символов юникода, таких как смайлы и различные спец. знаки;
- **remove_dup_spaces** - удаление множественных пробелов и отступов, а также их замена на одиночный пробел;
- **text_preprocessing** - пайплайн, который был использован авторами для препроцессинга текста в датасетах.

### [regulars.py](regulars.py)

Данный файл содержит в себе список регулярных выражений, применённых для чистки текстов в датасете от лишних конструкций. Подробное применение можно рассмотреть в файле [data_preprocessing.py](data_preprocessing.py).

### [datasets_analyse.py](datasets_analyse.py)

В данном файле описаны функции, которые были применены к датасету для препроцессинга и валидации текста, проверяя его на принадлежность к множеству тюркских языков с помощью модуля [fasttext](https://fasttext.cc/) и их модели для идентификации языка текста [lid.176.bin](https://fasttext.cc/docs/en/language-identification.html) [[1]](README.md/#references).

Файл содержит следующие функции:
- **sentenize_and_predict** - функция содержит в себе препроцессинг текста с помощью функций из файла [data_preprocessing.py](data_preprocessing.py), разложение текста на список предложений и описание параметров данных предложений с помощью модели от [fasttext](https://fasttext.cc/). Подробнее с работой функции можно познакомиться в файле [datasets_analyse.py](datasets_analyse.py);
- **create_only_turk_text_list** - данная функция предназначена для удаления лишних предложений (продложений **не** на Тюркских языках) из созданного с помощью функции **sentenize_and_predict** списка предложений с параметрами в словаре.

А также вспомогательные функции:
- **join_with_none** - функция преследует те же цели как и встроенная в Python функция [**join**](https://docs.python.org/3/library/stdtypes.html?highlight=str%20join#str.join), но игнорирует **None** в списках, в случае их присутствия; 
- **list_strip_none** - удаление в начале и конце списка элементов **None**.

### [triplets_funcs.py](triplets_funcs.py)

Файл может быть использован для генерации некоторых видов **триплетов** (троек предложений, идущих в верном, а также в заведомо ложном порядке) для различных задач обучения и проверки языковых моделей.

Основные функции:
- **generate_triplets_NSP** - функция для получения возможных триплетов и их комбинаций с подходящими предложениями из текста; 
- **shuffle_triplet_NSP** - функция для получения комбинаций из триплета и другого предложения;
- **generate_triplets_SOP** - функция для получения всех возможных триплетов и их комбинаций из текста. Для задач SOP достаточно просто найти триплеты и смешать предложения внутри них;
- **shuffle_triplet_SOP** - функция для получения всех возможных комбинаций внутри одного триплета;
- **find_all_triplets** - функция для поиска всех триплетов в тексте. С помощью функции **find_triplet** выполняется поиск по всем допустимым триплетам в тексте.
- **find_triplet** - функция для поиска первого попавшегося триплета в искомом тексте согласно определённым условиям по максимальной и минимальной длине предложения, а также относительному отклонению длин предложений (более подробная информация по работе данной функции указана в [triplets_funcs.py](triplets_funcs.py))

А также вспомогательные функции:
- **sentenize_text_to_list** - применяется для преобразования текста типа **str** в **list[str]** с помощью модуля [**razdel**](https://natasha.github.io/razdel/) и функции [**sentenize**](https://github.com/natasha/razdel?tab=readme-ov-file#usage);
- **check_text_type** - применяется для проверки входных данных и последющих действий с ними. В случае, если на вход поступит объект типа **list**, то с данными ничего не произойдёт. В случае, если на вход поступит объект типа **str**, то данный текст будет преобразован в **list[str]** через функцию **sentenize_text_to_list**.
