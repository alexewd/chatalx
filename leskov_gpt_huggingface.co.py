import pandas as pd
import os
import re
from pathlib import Path
import nltk
from nltk.corpus import stopwords

# Загрузка списка стоп-слов на русском
nltk.download('stopwords')
stop_words = set(stopwords.words('russian'))

# Путь к каталогу с текстовыми файлами
folder_path = Path("e:/cleaned_text")

# Чтение текстов из файлов
all_texts = []
for file_name in os.listdir(folder_path):
    if file_name.endswith('.txt'):  # проверяем, что это текстовый файл
        file_path = folder_path / file_name
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            all_texts.append(content)

# Объединяем всё в один текст
full_text = ' '.join(all_texts)

# Разбиваем текст на предложения
sentences = re.split(r'(?<=[.!?]) +', full_text)

# Функция для очистки текста
def clean_text(text):
    # Приводим к нижнему регистру
    text = text.lower()
    # Убираем пунктуацию
    text = re.sub(r'[^\w\s]', '', text)  # Удаляем пунктуацию
    # Убираем цифры
    text = re.sub(r'\d+', '', text)       # Удаляем цифры
    # Убираем стоп-слова
    text = ' '.join([word for word in text.split() if word not in stop_words])
    return text

# Очищаем предложения и создаём DataFrame
cleaned_sentences = [clean_text(sentence) for sentence in sentences]

# Создаем DataFrame с количеством символов в 'frequencies'
df = pd.DataFrame({
    'id': range(len(cleaned_sentences)),  # создаем id
    'text': cleaned_sentences,
    'frequencies': [len(sentence) for sentence in cleaned_sentences]  # количество символов в каждом предложении
})

# Устанавливаем id как индекс
df.set_index('id', inplace=True)

# Выводим результат
print(df)
df.shape