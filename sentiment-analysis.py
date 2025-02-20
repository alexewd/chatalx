import os
import re
import pandas as pd
from collections import Counter

# Создание DataFrame с оценками слов
data = {
    'word': ['хороший', 'прекрасный', 'замечательный', 'радостный', 'счастливый',
             'плохой', 'ужасный', 'грустный', 'печальный', 'негативный'],
    'sentiment': ['positive', 'positive', 'positive', 'positive', 'positive',
                  'negative', 'negative', 'negative', 'negative', 'negative'],
    'score': [1, 1, 1, 1, 1, -1, -1, -1, -1, -1]
}

sentiments_df = pd.DataFrame(data)

# Путь к папке с текстовыми файлами
folder_path = 'e:/cleaned_text'

# Словари для подсчета положительных и отрицательных слов
positive_counter = Counter()
negative_counter = Counter()

# Функция для предобработки текста
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

# Чтение файлов из папки
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
            text = file.read()
            processed_text = preprocess_text(text)
            words = processed_text.split()

            # Подсчет положительных и отрицательных слов
            for word in words:
                if word in sentiments_df['word'].values:
                    sentiment = sentiments_df.loc[sentiments_df['word'] == word, 'sentiment'].values[0]
                    if sentiment == 'positive':
                        positive_counter[word] += 1
                    elif sentiment == 'negative':
                        negative_counter[word] += 1

# Получение наиболее распространенных слов
most_common_positive = positive_counter.most_common(5)  # 5 наиболее распространенных положительных слов
most_common_negative = negative_counter.most_common(5)  # 5 наиболее распространенных отрицательных слов

# Вывод результатов
print("Наиболее распространенные положительные слова:")
for word, count in most_common_positive:
    print(f"{word}: {count}")

print("\nНаиболее распространенные отрицательные слова:")
for word, count in most_common_negative:
    print(f"{word}: {count}")
