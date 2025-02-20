import pandas as pd
import os
import re
from pathlib import Path

# Загрузка словаря
url = "https://raw.githubusercontent.com/text-machine-lab/sentimental/master/sentimental/word_list/russian.csv"
dict_df = pd.read_csv(url)

# Переименование колонок
dict_df.columns = ['word', 'score']

# Агрегация оценок в словаре, чтобы оставить только одно значение для каждого слова
dict_df = dict_df.groupby('word', as_index=False).agg({'score': 'mean'})

# Путь к папке с текстами
text_folder = Path("e:/cleaned_text")

# Создание пустых датафреймов для хранения результатов
results = pd.DataFrame(columns=['file', 'sentiment_score', 'positive_count', 'negative_count'])
found_words = pd.DataFrame(columns=['word', 'positive_count', 'negative_count'])

# Анализ каждого текстового файла
for file_path in text_folder.glob("*.txt"):
    filename = file_path.name
    
    # Чтение текста из файла
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    # Разделение текста на слова
    words = re.findall(r'\w+', text.lower())  # Приведение к нижнему регистру и разделение на слова
    
    # Подсчет суммарной оценки тональности и количества положительных и отрицательных слов
    sentiment_data = pd.Series(words).value_counts().reset_index()
    sentiment_data.columns = ['word', 'count']
    sentiment_data = sentiment_data.merge(dict_df, on='word', how='left')
    
    # Определение тональности
    sentiment_data['sentiment'] = sentiment_data['score'].apply(lambda x: 'positive' if x > 0 else ('negative' if x < 0 else None))
    
    # Подсчет общего количества положительных и отрицательных слов
    positive_count = sentiment_data[sentiment_data['sentiment'] == 'positive']['count'].sum()
    negative_count = sentiment_data[sentiment_data['sentiment'] == 'negative']['count'].sum()
    
    # Подсчет общей оценки
    sentiment_score = (sentiment_data['count'] * sentiment_data['score']).sum()  # Общая оценка
    
    # Добавление результатов в общий датафрейм
    results = pd.concat([results, pd.DataFrame([{'file': filename, 
                                                 'sentiment_score': sentiment_score, 
                                                 'positive_count': positive_count, 
                                                 'negative_count': negative_count}])], ignore_index=True)
    
    # Создание датафреймов для положительных и отрицательных слов
    positive_words = sentiment_data[sentiment_data['sentiment'] == 'positive'][['word', 'count']]
    negative_words = sentiment_data[sentiment_data['sentiment'] == 'negative'][['word', 'count']]
    
    # Переименование столбцов для объединения
    positive_words.columns = ['word', 'positive_count']
    negative_words.columns = ['word', 'negative_count']
    
    # Объединение положительных и отрицательных слов в один датафрейм
    combined_words = pd.merge(positive_words, negative_words, on='word', how='outer').fillna(0)
    
    # Добавление найденных слов в общий датафрейм
    found_words = pd.concat([found_words, combined_words], ignore_index=True)

# Сортировка найденных слов по убыванию count
found_words = found_words.sort_values(by=['positive_count', 'negative_count'], ascending=False)

# Вывод результатов
print(results)
print(found_words)
