import numpy as np
from pathlib import Path
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import re
from nltk.corpus import stopwords
import nltk

# Убедимся, что стоп-слова загружены
nltk.download("stopwords")
russian_stopwords = stopwords.words("russian")

# Путь к текстовому файлу
text_file = Path("e:/cleaned_json_letter/Лесков Николай. Том 11.txt")

# Функция для разбиения текста на предложения
def split_into_sentences(text):
    # Регулярное выражение для нахождения предложений
    sentence_endings = r"[.!?]\\s"
    sentences = re.split(sentence_endings, text)
    # Убираем пустые строки и лишние пробелы
    return [sentence.strip() for sentence in sentences if sentence.strip()]

# Читаем текстовый файл
with open(text_file, "r", encoding="utf-8") as file:
    text = file.read()

# Разбиваем текст на предложения
sentences_list = split_into_sentences(text)

# Преобразуем список в массив NumPy
text_data = np.array(sentences_list)

# Пример использования CountVectorizer
count = CountVectorizer()
bag_of_words = count.fit_transform(text_data)

# Используем TfidfVectorizer с фильтрацией стоп-слов и биграммами
tfidf = TfidfVectorizer(ngram_range=(1, 2), stop_words=russian_stopwords)
feature_matrix = tfidf.fit_transform(text_data)

# Получаем слова и биграммы с их значениями TF-IDF
feature_names = tfidf.get_feature_names_out()
tfidf_scores = feature_matrix.sum(axis=0).A1

# Создаем список из слов/биграмм и их значений
features_with_scores = list(zip(feature_names, tfidf_scores))

# Сортируем по убыванию значимости
sorted_features = sorted(features_with_scores, key=lambda x: x[1], reverse=True)

# Фильтруем элементы: убираем цифры и комбинации букв и цифр
filtered_features = [(feature, score) for feature, score in sorted_features if not re.search(r"\\d", feature)]

# Выводим топ-10 самых значимых слов и биграмм
print("Топ-10 значимых слов и биграмм по TF-IDF:")
for feature, score in filtered_features[:10]:
    print(f"{feature}: {score:.4f}")

# Выводим примерный результат
print("Пример предложений:", text_data[:5])
print("Форма bag_of_words:", bag_of_words.shape)
