import numpy as np
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
import re
from nltk.corpus import stopwords
import nltk

# Убедимся, что стоп-слова загружены
nltk.download("stopwords")
russian_stopwords = stopwords.words("russian")

# Путь к папке с текстовыми файлами
folder_path = Path("e:/cleaned_text")

# Функция для разбиения текста на предложения
def split_into_sentences(text):
    sentence_endings = r"[.!?]\\s"
    sentences = re.split(sentence_endings, text)
    return [sentence.strip() for sentence in sentences if sentence.strip()]

# Читаем все .txt файлы из папки
documents = []
for file_path in folder_path.glob("*.txt"):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
        documents.append(" ".join(split_into_sentences(text)))

# Настраиваем TfidfVectorizer для работы с триграммами
tfidf = TfidfVectorizer(
    ngram_range=(1, 3),  # Учитываем униграммы, биграммы и триграммы
    stop_words=russian_stopwords,  # Исключаем стоп-слова
    min_df=2,  # Учитываем только слова/фразы, которые встречаются минимум 2 раза
    max_df=0.9  # Исключаем фразы, встречающиеся в более чем 90% документов
)
feature_matrix = tfidf.fit_transform(documents)

# Получаем слова/биграммы/триграммы с их значениями TF-IDF
feature_names = tfidf.get_feature_names_out()
tfidf_scores = feature_matrix.sum(axis=0).A1

# Создаем список из слов/фраз и их значений
features_with_scores = list(zip(feature_names, tfidf_scores))

# Сортируем по убыванию значимости
sorted_features = sorted(features_with_scores, key=lambda x: x[1], reverse=True)

# Выводим топ-10 самых значимых слов, биграмм и триграмм
print("Топ-10 значимых слов, биграмм и триграмм по TF-IDF:")
for feature, score in sorted_features[:10]:
    print(f"{feature}: {score:.4f}")

# Выводим количество обработанных документов
print(f"Обработано документов: {len(documents)}")
