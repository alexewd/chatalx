import pandas as pd
from pathlib import Path
# stopwords_nltk = stopwords.words('russian')
import re
from nltk.corpus import stopwords
from string import punctuation
stopwords_nltk = stopwords.words('russian')
# Загружаем список стоп-слов на русском языке
russian_stopwords = set(stopwords.words('russian'))

def clean_text(text):
    # Приведение текста к нижнему регистру
    text = text.lower()
    
    # Удаление цифр
    text = re.sub(r'\d+', '', text)
    
    # Удаление пунктуации
    text = ''.join([char for char in text if char not in punctuation])
    
    # Удаление стоп-слов
    text = ' '.join([word for word in text.split() if word not in russian_stopwords])
    
    return text




# Создаем пустой список для хранения предложений
sentences = []

# Путь к папке с текстовыми файлами
folder_path = Path("e:/cleaned_text")

# Читаем каждый файл и добавляем предложения в список
for file_path in folder_path.glob("*.txt"):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
        # Добавляем предложения в список
        sentences.extend(text.split(". "))

# Создаем датафрейм pandas
df = pd.DataFrame(sentences, columns=["Sentences"])

# Создаем пустой список для предложений
sentences_list = []

# Цикл по строкам файла
for index, row in df.iterrows():
    # Очищаем текст предложения
    cleaned_sentence = clean_text(row['Sentences'])
    
    # Добавляем очищенное предложение в список
    sentences_list.append(cleaned_sentence)

df_clear = pd.DataFrame(sentences_list, columns=["Sentences"])

# Выводим первые строки датафрейма
print(df.head())
df.shape
df_clear.shape
print(df_clear.sample(30))
print(df.tail(30))

search_phrase = "юная римская патрицианка"

# Найти все предложения, содержащие словосочетание
matching_sentences = df[df["Sentences"].str.contains(search_phrase, case=False)]

# Вывести найденные предложения
print(matching_sentences)
print(df["Sentences"][26988])
