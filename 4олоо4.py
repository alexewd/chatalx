import re
import pandas as pd
from pathlib import Path

# Загрузка текстов из папки
def load_texts_from_folder(folder_path):
    texts = []
    for file_path in folder_path.glob("*.txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
            texts.append(text)
    return texts

# Разбиение текста на предложения
def split_into_sentences(text):
    sentences = re.split(r'[.!?]', text)
    return [sentence.strip() for sentence in sentences if sentence.strip()]

# Анализ предложений
def analyze_sentences(texts):
    all_sentences = []
    for text in texts:
        sentences = split_into_sentences(text)
        all_sentences.extend(sentences)
    
    total_sentences = len(all_sentences)
    total_words = sum(len(sentence.split()) for sentence in all_sentences)
    avg_sentence_length = total_words / total_sentences if total_sentences > 0 else 0
    
    return total_sentences, avg_sentence_length

# Основной процесс
folder_path = Path("e:/cleaned_text")
texts = load_texts_from_folder(folder_path)

# Анализ предложений
total_sentences, avg_sentence_length = analyze_sentences(texts)

# Вывод результатов
print(f"Общее количество предложений: {total_sentences}")
print(f"Средняя длина предложения: {avg_sentence_length:.2f} слов")
