import numpy as np
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
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
    sentence_endings = r"[.!?]\\s"
    sentences = re.split(sentence_endings, text)
    return [sentence.strip() for sentence in sentences if sentence.strip()]

# Читаем текстовый файл
with open(text_file, "r", encoding="utf-8") as file:
    text = file.read()

# Разбиваем текст на предложения
sentences_list = split_into_sentences(text)

# Преобразуем список в массив NumPy
text_data = np.array(sentences_list)

# Настраиваем TfidfVectorizer для работы с триграммами
tfidf = TfidfVectorizer(
    ngram_range=(1, 3),  # Учитываем униграммы, биграммы и триграммы
    stop_words=russian_stopwords,  # Исключаем стоп-слова
    min_df=2,  # Учитываем только слова/фразы, которые встречаются минимум 2 раза
    max_df=1.0  # Убираем только те, что встречаются во всех документах
)
feature_matrix = tfidf.fit_transform([" ".join(sentences_list)])  # Передаём весь текст как один документ

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

# Выводим примерный результат
print("Пример предложений:", text_data[:5])
print("Форма feature_matrix:", feature_matrix.shape)
