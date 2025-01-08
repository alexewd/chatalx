import pandas as pd
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer

# Установка пути к файлу
file_path = 'f:/chatepc/chatalx/work/data/poem.txt'

# Чтение содержимого файла
with open(file_path, 'r', encoding='utf-8') as file:
    text = file.read()

# Загрузка необходимых ресурсов NLTK
nltk.download('punkt')
nltk.download('stopwords')

# Токенизация текста на русском языке
tokens = nltk.word_tokenize(text, language='russian')

# Загрузка стоп-слов для русского языка
from nltk.corpus import stopwords
stop_words = list(stopwords.words('russian'))

# Удаление стоп-слов и оставление только алфавитных слов
filtered_tokens = [word for word in tokens if word.lower() not in stop_words and word.isalpha()]

# Преобразование текста в список строк для TF-IDF
lines = text.split('\n')

# Создание DataFrame с строками текста
text_df = pd.DataFrame({'text': lines})

# Инициализация TfidfVectorizer с указанием стоп-слов для русского языка
vectorizer = TfidfVectorizer(stop_words=stop_words)

# Обучение и трансформация текста
tfidf_matrix = vectorizer.fit_transform(text_df['text'])

# Преобразование TF-IDF матрицы в DataFrame для удобства анализа
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out())

# Пример использования токенов и TF-IDF значений
print("Первый DataFrame с токенами после удаления стоп-слов:")
print(filtered_tokens[:10])  # Печать первых 10 токенов после удаления стоп-слов

print("\nDataFrame с TF-IDF значениями:")
print(tfidf_df.head())