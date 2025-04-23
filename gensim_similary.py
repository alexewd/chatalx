import os
import pandas as pd
import string
import re
from gensim.models import Word2Vec
from nltk.corpus import stopwords
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer

# Загрузка стоп-слов
nltk.download('stopwords')
stop_words = set(stopwords.words('russian'))

# Добавление своих стоп-слов
custom_stop_words = {'в', 'он', 'и', 'который', 'которое', 'очень', 'всем', 'своей'}
stop_words = stop_words.union(custom_stop_words)

# Преобразование множества стоп-слов в список
stop_words_list = list(stop_words)

# Путь к папке с текстовыми файлами
folder_path = 'e:\\cleaned_text'

# Список для хранения предложений
sentences = []
documents = []  # Список для хранения документов для TF-IDF

# Функция для предобработки текста
def preprocess_text(text):
    # Приведение к нижнему регистру
    text = text.lower()
    # Удаление знаков пунктуации и цифр
    text = re.sub(r'[^\w\s]', '', text)  # Удаление пунктуации
    text = re.sub(r'\d+', '', text)      # Удаление цифр
    return text

# Чтение текстовых файлов из папки
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):  # Убедитесь, что это текстовый файл
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            # Чтение содержимого файла
            text = file.read()
            # Предобработка текста
            text = preprocess_text(text)
            documents.append(text)  # Добавляем обработанный текст в список документов
            # Разделение текста на предложения и слова
            for sentence in text.splitlines():
                words = sentence.split()  # Разделение на слова
                # Удаление стоп-слов
                words = [word for word in words if word not in stop_words]
                if words:  # Проверка, что предложение не пустое
                    sentences.append(words)

# Обучение модели Word2Vec
model = Word2Vec(sentences, vector_size=100, window=5, min_count=1, workers=4)

# Поиск похожих слов
similar_words = model.wv.most_similar('человек', topn=10)

# Создание DataFrame из результатов Word2Vec
df_similar_words = pd.DataFrame(similar_words, columns=['Слово', 'Сходство'])

# Вывод таблицы с похожими словами
print("Похожие слова к 'человек':")
print(df_similar_words)

# Вычисление TF-IDF
vectorizer = TfidfVectorizer(stop_words=stop_words_list)
tfidf_matrix = vectorizer.fit_transform(documents)

# Получение слов и их TF-IDF значений
tfidf_scores = tfidf_matrix.toarray()
feature_names = vectorizer.get_feature_names_out()

# Создание DataFrame для TF-IDF
df_tfidf = pd.DataFrame(tfidf_scores, columns=feature_names)

# Суммирование TF-IDF значений по всем документам
df_tfidf_sum = df_tfidf.sum(axis=0).reset_index()
df_tfidf_sum.columns = ['Слово', 'TF-IDF']

# Сортировка по TF-IDF значению
df_tfidf_sum = df_tfidf_sum.sort_values(by='TF-IDF', ascending=False)

# Вывод таблицы TF-IDF
print("\nTF-IDF по словам:")
print(df_tfidf_sum.head(10))  # Выводим топ-10 слов по TF-IDF
