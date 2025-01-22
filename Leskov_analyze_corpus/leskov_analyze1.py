import os
import json
import nltk
from nltk.corpus import stopwords
from collections import Counter
import string

# Загрузим стоп-слова
nltk.download('stopwords')
stop_words = set(stopwords.words('russian'))

# Функция для чтения всех текстов из папки
def load_text_files(text_folder):
    texts = []
    for filename in os.listdir(text_folder):
        if filename.endswith('.txt'):
            with open(os.path.join(text_folder, filename), 'r', encoding='utf-8') as file:
                texts.append(file.read())
    return texts

# Функция для загрузки JSON файлов
def load_json_files(json_folder):
    texts = []
    for filename in os.listdir(json_folder):
        if filename.endswith('.json'):
            with open(os.path.join(json_folder, filename), 'r', encoding='utf-8') as file:
                data = json.load(file)
                texts.append(data.get('content', ''))
    return texts

# Функция для очистки текста
def clean_text(text):
    # Удаляем пунктуацию и приводим к нижнему регистру
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Разделяем текст на слова
    words = text.split()
    # Удаляем стоп-слова
    words = [word for word in words if word not in stop_words]
    return words

# Функция для анализа частотности слов
def word_frequency_analysis(texts):
    all_words = []
    for text in texts:
        all_words.extend(clean_text(text))
    word_counts = Counter(all_words)
    return word_counts

# Пример использования
text_folder = 'e:/cleaned_text'
json_folder = 'e:/cleaned_json'

# Загружаем тексты и JSON
texts_from_txt = load_text_files(text_folder)
texts_from_json = load_json_files(json_folder)

# Объединяем тексты
# all_texts = texts_from_txt + texts_from_json
all_texts = texts_from_json
# Анализируем частоту слов
word_counts = word_frequency_analysis(all_texts)

# Выводим 10 самых частых слов
print(word_counts.most_common(10))
import pandas as pd
from collections import Counter

# Функция для анализа частотности слов
def word_frequency_analysis(texts):
    all_words = []
    for text in texts:
        all_words.extend(clean_text(text))
    word_counts = Counter(all_words)
    return word_counts

# Преобразуем результат частотного анализа в DataFrame
def create_frequency_dataframe(word_counts):
    # Преобразуем в DataFrame
    df = pd.DataFrame(word_counts.items(), columns=['Word', 'Frequency'])
    # Добавляем индекс 'id'
    df['id'] = df.index + 1  # Индексация начинается с 1
    # Переупорядочиваем столбцы, чтобы id был первым
    df = df[['id', 'Word', 'Frequency']]
    return df

# Пример использования
json_folder = 'e:/cleaned_json'

# Загружаем тексты из JSON
texts_from_json = load_json_files(json_folder)

# Анализируем частоту слов
word_counts = word_frequency_analysis(texts_from_json)

# Преобразуем частотность в DataFrame
frequency_df = create_frequency_dataframe(word_counts)

# Выводим результат в табличном виде
print(frequency_df)

# Если хочешь сохранить в CSV
frequency_df.to_csv('word_frequency.csv', index=False)

