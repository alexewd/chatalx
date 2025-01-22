import os
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
from natasha import Segmenter, MorphVocab, NewsEmbedding, NewsMorphTagger, Doc
from nltk.corpus import stopwords
import pandas as pd
import nltk

# Загружаем стоп-слова
nltk.download("stopwords")
russian_stopwords = set(stopwords.words("russian"))

# Параметры
folder_path = "e:/cleaned_text"

# Настройки Natasha
segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)

# Чтение и предобработка текстов
def read_and_process_files(folder_path):
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), "r", encoding="utf-8") as file:
                documents.append(file.read())
    return documents

texts = read_and_process_files(folder_path)

# Лемматизация и подсчёт частот
def lemmatize_and_count(texts):
    words = []
    for text in texts:
        doc = Doc(text)
        doc.segment(segmenter)
        doc.tag_morph(morph_tagger)
        for token in doc.tokens:
            token.lemmatize(morph_vocab)
            if token.pos not in {"PUNCT", "NUM", "PRON"} and token.lemma not in russian_stopwords:
                words.append(token.lemma)
    return Counter(words)

# Получение частотных лексем
word_counts = lemmatize_and_count(texts)

# Построение графика
def plot_top_words(word_counts, top_n=20):
    most_common = word_counts.most_common(top_n)
    words, counts = zip(*most_common)
    plt.figure(figsize=(12, 8))
    sns.barplot(x=list(counts), y=list(words), palette="viridis")
    plt.title(f"Top-{top_n} Most Frequent Lemmas (Excluding Stopwords)", fontsize=16)
    plt.xlabel("Frequency", fontsize=14)
    plt.ylabel("Lemma", fontsize=14)
    plt.grid(axis="x", linestyle="--", alpha=0.6)
    plt.show()

plot_top_words(word_counts)

# Контекст использования ключевых терминов
def find_context(texts, keyword, window=5):
    keyword_contexts = []
    for text in texts:
        sentences = text.split(".")
        for sentence in sentences:
            if keyword in sentence:
                keyword_contexts.append(sentence.strip())
    return keyword_contexts

# Пример для поиска контекста
keyword = "человек"  # Замените на любое слово
contexts = find_context(texts, keyword)
print(f"Контексты для слова '{keyword}':")
for i, context in enumerate(contexts[:10], 1):  # Ограничение вывода 10 контекстов
    print(f"{i}. {context}")

# Анализ стиля через синтаксический разбор
def syntax_analysis(text):
    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    sentences = []
    for sentence in doc.sents:
        tokens = [(token.text, token.pos, token.feats) for token in sentence.tokens]
        sentences.append(tokens)
    return sentences

# Анализ первого текста
syntax_results = syntax_analysis(texts[0])
print(f"Анализ синтаксиса (первые 3 предложения):")
for i, sent in enumerate(syntax_results[:3], 1):
    print(f"{i}.", sent)
