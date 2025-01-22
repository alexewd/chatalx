from pymorphy3 import MorphAnalyzer
from gensim.models import Word2Vec
import os
from pathlib import Path
import re

# Путь к папке с текстами
folder_path = Path("e:/cleaned_text")

# Инициализация pymorphy3
morph = MorphAnalyzer()

# Функция для лемматизации текста
def lemmatize_texts(texts):
    lemmatized_sentences = []
    for text in texts:
        # Разбиваем текст на предложения
        sentences = re.split(r'[.!?]', text)
        for sentence in sentences:
            # Разбиваем предложения на слова
            words = re.findall(r'\b\w+\b', sentence)
            # Лемматизируем слова
            lemmatized_words = [
                morph.parse(word)[0].normal_form for word in words
                if word.isalpha()  # Убираем цифры и спецсимволы
            ]
            if lemmatized_words:
                lemmatized_sentences.append(" ".join(lemmatized_words))
    return lemmatized_sentences

# Загрузка текстов из папки
def load_texts_from_folder(folder_path):
    texts = []
    for file_path in folder_path.glob("*.txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
            text = re.sub(r"\s+", " ", text)  # Убираем лишние пробелы
            texts.append(text)
    return texts

# Основной процесс
texts = load_texts_from_folder(folder_path)
lemmatized_sentences = lemmatize_texts(texts)

# Обучение модели Word2Vec
w2v_model = Word2Vec(
    sentences=[sentence.split() for sentence in lemmatized_sentences],
    vector_size=100,  # Размерность эмбеддингов
    window=5,  # Контекстное окно
    min_count=2,  # Минимальная частота слова
    workers=4,  # Количество потоков
    sg=1,  # Skip-Gram
)

# Пример: находим похожие слова
similar_words = w2v_model.wv.most_similar("лесков", topn=10)

# Вывод результатов
print("Слова, похожие на 'лесков':")
for word, similarity in similar_words:
    print(f"{word}: {similarity:.4f}")
