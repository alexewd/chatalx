import re
import spacy
import numpy as np

# Загрузка модели spacy для русского языка
nlp = spacy.load("ru_core_news_sm")

# Чтение содержимого файла
file_path = "f:/chatepc/chatalx/work/data/Гробовщик.txt"
with open(file_path, 'r', encoding='utf-8') as file:
    text_data = file.read()

# Очистка текста
def clean_text(text):
    text = text.lower()  # Приводим к нижнему регистру
    text = re.sub(r"[^а-яё\s]", " ", text)  # Удаляем всё, кроме кириллических букв и пробелов
    text = re.sub(r"\s+", " ", text)  # Удаляем лишние пробелы
    text = text.strip()  # Убираем пробелы в начале и конце строки
    return text

# Обработка текста с помощью spacy
doc = nlp(text_data)

# Разбиение текста на предложения
sentences = list(doc.sents)

# Очистка каждого предложения
cleaned_sentences = [clean_text(sentence.text) for sentence in sentences]

# Удаление пустых предложений
cleaned_sentences = [sentence for sentence in cleaned_sentences if len(sentence) > 0]

# Подсчет количества слов и символов
word_count_in_sentences = [len(sentence.split()) for sentence in cleaned_sentences]
char_count_in_sentences = [len(sentence) for sentence in cleaned_sentences]

average_sentence_length_words = np.mean(word_count_in_sentences)
average_sentence_length_chars = np.mean(char_count_in_sentences)

print(f"Количество предложений: {len(cleaned_sentences)}")
print(f"Средняя длина предложения в символах: {average_sentence_length_chars}")
print(f"Средняя длина предложения в словах: {average_sentence_length_words}")

##############################################
# Ранее текст был очищен до того, как был разбит на предложения. Это привело к тому, что все символы, не являющиеся кириллическими буквами или пробелами, были удалены, включая знаки препинания, такие как точки, которые используются для разбиения текста на предложения. В результате весь текст стал одной длинной строкой.

# Исправление заключалось в следующем:

# Разбиение текста на предложения до очистки: Сначала текст разбивается на предложения с помощью библиотеки Spacy.
# Очистка каждого предложения отдельно: После разбиения на предложения каждое предложение очищается отдельно.
# Вот исправленный код снова:

import re
import spacy
import numpy as np

# Загрузка модели spacy для русского языка
nlp = spacy.load("ru_core_news_sm")

# Чтение содержимого файла
file_path = "f:/chatepc/chatalx/work/data/Гробовщик.txt"
with open(file_path, 'r', encoding='utf-8') as file:
    text_data = file.read()

# Очистка текста
def clean_text(text):
    text = text.lower()  # Приводим к нижнему регистру
    text = re.sub(r"[^а-яё\s]", " ", text)  # Удаляем всё, кроме кириллических букв и пробелов
    text = re.sub(r"\s+", " ", text)  # Удаляем лишние пробелы
    text = text.strip()  # Убираем пробелы в начале и конце строки
    return text

# Обработка текста с помощью spacy
doc = nlp(text_data)

# Разбиение текста на предложения
sentences = list(doc.sents)

# Очистка каждого предложения
cleaned_sentences = [clean_text(sentence.text) for sentence in sentences]

# Удаление пустых предложений
cleaned_sentences = [sentence for sentence in cleaned_sentences if len(sentence) > 0]

# Подсчет количества слов и символов
word_count_in_sentences = [len(sentence.split()) for sentence in cleaned_sentences]
char_count_in_sentences = [len(sentence) for sentence in cleaned_sentences]

average_sentence_length_words = np.mean(word_count_in_sentences)
average_sentence_length_chars = np.mean(char_count_in_sentences)

print(f"Количество предложений: {len(cleaned_sentences)}")
print(f"Средняя длина предложения в символах: {average_sentence_length_chars}")
print(f"Средняя длина предложения в словах: {average_sentence_length_words}")
# Пояснение:
# Разбиение текста на предложения:

# Python
# doc = nlp(text_data)
# sentences = list(doc.sents)
# Очистка каждого предложения отдельно:

# cleaned_sentences = [clean_text(sentence.text) for sentence in sentences]
# Удаление пустых предложений:

# cleaned_sentences = [sentence for sentence in cleaned_sentences if len(sentence) > 0]
# Эти изменения обеспечивают правильное разбиение текста на предложения перед очисткой, что позволяет избежать создания одной длинной строки.

