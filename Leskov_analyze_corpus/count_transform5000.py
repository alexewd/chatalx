import numpy as np
import pandas as pd
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

# Функция для очистки текста
def preprocess_text(text):
    text = re.sub(r'\d+', ' ', text)  # Удаление чисел
    text = re.sub(r'[^\w\s]', ' ', text)  # Удаление пунктуации
    text = re.sub(r'\s+', ' ', text).strip()  # Удаление лишних пробелов
    return text

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
        if text.strip():  # Убедимся, что файл не пустой
            processed_text = preprocess_text(text)  # Очистка текста
            documents.append(" ".join(split_into_sentences(processed_text)))
        else:
            print(f"Файл {file_path} пустой")

# Проверка, есть ли документы
if not documents:
    raise ValueError("Нет доступных документов для обработки.")

# Настраиваем TfidfVectorizer для работы с триграммами
tfidf = TfidfVectorizer(
    ngram_range=(1, 3),  # Учитываем униграммы, биграммы и триграммы
    stop_words=russian_stopwords,  # Исключаем стоп-слова
    min_df=2,  # Учитываем только слова/фразы, встречающиеся хотя бы 2 раза
    max_df=0.9  # Исключаем слишком часто встречающиеся фразы
)

# Обработка документов
feature_matrix = tfidf.fit_transform(documents)

# Получаем слова/биграммы/триграммы с их значениями TF-IDF
feature_names = tfidf.get_feature_names_out()
tfidf_scores = feature_matrix.sum(axis=0).A1

# Определяем тип n-граммы
def get_ngram_type(ngram):
    num_words = len(ngram.split())
    if num_words == 1:
        return "unigram"
    elif num_words == 2:
        return "bigram"
    elif num_words == 3:
        return "trigram"
    return "unknown"

# Создаем DataFrame
data = {
    "term": feature_names,
    "tfidf_score": tfidf_scores,
    "ngram_type": [get_ngram_type(term) for term in feature_names]
}
df = pd.DataFrame(data)

# Сортируем по убыванию TF-IDF
df = df.sort_values(by="tfidf_score", ascending=False).reset_index(drop=True)

# Выводим первые строки таблицы
print(df.head(40))

# Сохраняем в CSV (если нужно)
df.to_csv("tfidf_results.csv", index=False, encoding="utf-8")

# Вывод размеров таблицы
print(f"Размер таблицы: {df.shape}")

import matplotlib.pyplot as plt
import seaborn as sns

# Выбираем топ-20 терминов по TF-IDF
top_terms = df.head(20)

# Настраиваем график
plt.figure(figsize=(12, 8))
sns.barplot(
    data=top_terms,
    y="term",
    x="tfidf_score",
    hue="ngram_type",
    dodge=False,  # Объединяем значения unigram, bigram, trigram
    palette="viridis"
)

# Оформляем график
plt.title("Top-20 Terms by TF-IDF Score", fontsize=16)
plt.xlabel("TF-IDF Score", fontsize=14)
plt.ylabel("Term", fontsize=14)
plt.legend(title="N-gram Type", fontsize=12)
plt.grid(axis="x", linestyle="--", alpha=0.6)

# Показываем график
plt.tight_layout()
plt.show()

