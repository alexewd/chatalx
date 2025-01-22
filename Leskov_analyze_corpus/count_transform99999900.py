import os
import re
from pathlib import Path
from collections import Counter
from pymorphy3 import MorphAnalyzer
from concurrent.futures import ProcessPoolExecutor
import nltk
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import seaborn as sns

# Инициализация pymorphy3 и кеша
morph = MorphAnalyzer()
morph_cache = {}

def lemmatize_word(word):
    """Лемматизация одного слова с кешированием."""
    if word in morph_cache:
        return morph_cache[word]
    lemma = morph.parse(word)[0].normal_form
    morph_cache[word] = lemma
    return lemma

def lemmatize_text(text):
    """Лемматизация текста с удалением стоп-слов."""
    words = re.findall(r'\b\w+\b', text)
    lemmatized_words = [
        lemmatize_word(word) for word in words if word.isalpha() and word not in russian_stopwords
    ]
    return " ".join(lemmatized_words)

def lemmatize_texts_parallel(texts, max_workers=None):
    """Распараллеливание лемматизации текстов."""
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        lemmatized_texts = list(executor.map(lemmatize_text, texts))
    return lemmatized_texts

def load_texts_from_folder(folder_path):
    """Загрузка текстов из папки."""
    texts = []
    for file_path in Path(folder_path).glob("*.txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            texts.append(f.read())
    return texts

def analyze_frequencies(texts, top_n=20):
    """Частотный анализ текста."""
    all_words = " ".join(texts).split()
    word_counts = Counter(all_words)
    return word_counts.most_common(top_n)

def plot_frequencies(word_counts):
    """Визуализация частотности."""
    words, counts = zip(*word_counts)
    plt.figure(figsize=(12, 6))
    sns.barplot(x=list(words), y=list(counts), palette="viridis")
    plt.title("Топ самых частых слов", fontsize=16)
    plt.xticks(rotation=45, fontsize=12)
    plt.ylabel("Частота", fontsize=14)
    plt.xlabel("Слова", fontsize=14)
    plt.tight_layout()
    plt.show()

# Основной процесс
folder_path = "e:/cleaned_text"
texts = load_texts_from_folder(folder_path)

# Загрузка стоп-слов
nltk.download("stopwords")
russian_stopwords = set(stopwords.words("russian"))
custom_stopwords = {"стр", "гг", "руб", "году", "год"}
russian_stopwords.update(custom_stopwords)

# Лемматизация с распараллеливанием
lemmatized_texts = lemmatize_texts_parallel(texts, max_workers=os.cpu_count() - 1)

# Частотный анализ
word_counts_filtered = analyze_frequencies(lemmatized_texts)
print("Топ-20 самых частых слов (без стоп-слов):")
for word, count in word_counts_filtered:
    print(f"{word}: {count}")

# Визуализация
plot_frequencies(word_counts_filtered)
