import re
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Установка пути к файлу
file_path = "f:/chatepc/chatalx/work/data/Гробовщик.txt"

# Чтение содержимого файла
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Удаление пустых строк
non_empty_lines = [line for line in lines if line.strip() != ""]

# Запись обратно в файл
with open(file_path, 'w', encoding='utf-8') as file:
    file.writelines(non_empty_lines)

print("Пустые строки успешно удалены из файла.")

# 1. Загрузка текста
# file_path = "f:/chatepc/chatalx/work/data/Гробовщик.txt"
with open(file_path, 'r', encoding='utf-8') as file:
    text_data = file.read()

# 2. Разбиение текста на предложения
sentences = sent_tokenize(text_data, language='russian')

# 3. Очистка каждого предложения
def clean_text(text):
    text = text.lower()  # Приводим к нижнему регистру
    text = re.sub(r"[^а-яА-ЯёЁ\s]", " ", text)  # Удаляем всё, кроме букв и пробелов
    text = re.sub(r"\s+", " ", text)  # Удаляем лишние пробелы
    text = text.strip()  # Убираем пробелы в начале и конце строки
    return text

cleaned_sentences = [clean_text(sentence) for sentence in sentences]

# Проверяем, что предложения не пусты после очистки
cleaned_sentences = [sentence for sentence in cleaned_sentences if sentence]

# Дополнительная проверка предложений
print(f"Количество предложений: {len(cleaned_sentences)}")
print(f"Пример предложений: {cleaned_sentences[:5]}")

# Если предложений нет, выводим сообщение
if len(cleaned_sentences) == 0:
    print("Не удалось разделить текст на предложения.")
else:
    # Анализ длины предложений в символах
    sentence_lengths = [len(sentence) for sentence in cleaned_sentences]
    average_sentence_length = np.mean(sentence_lengths)
    print(f"Средняя длина предложения в символах: {average_sentence_length}")

    # Анализ количества слов в каждом предложении
    word_count_in_sentences = [len(word_tokenize(sentence, language='russian')) for sentence in cleaned_sentences]
    average_sentence_length_words = np.mean(word_count_in_sentences)
    print(f"Средняя длина предложения в словах: {average_sentence_length_words}")

# 4. Создание словаря с биграммами и триграммами
stop_words = stopwords.words('russian')  # Преобразуем множество в список
vectorizer = CountVectorizer(ngram_range=(1, 3), stop_words=stop_words)
dtm = vectorizer.fit_transform(cleaned_sentences)

# Проверка содержимого DTM
if dtm.shape[0] == 0 or dtm.shape[1] == 0:
    raise ValueError("DTM пуст. Проверьте настройки итератора или векторизации.")

# 5. Анализ частотности
term_frequency = np.asarray(dtm.sum(axis=0)).flatten()
terms = vectorizer.get_feature_names_out()
top_terms = sorted(zip(terms, term_frequency), key=lambda x: x[1], reverse=True)[:30]

print("Топ-30 терминов:")
for term, freq in top_terms:
    print(f"{term}: {freq}")

# 6. Визуализация частотности терминов с помощью WordCloud
wordcloud = WordCloud(width=800, height=400, scale=2, max_font_size=100, background_color="white").generate_from_frequencies(dict(top_terms))
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("Топ-30 терминов по частоте")
plt.show()

#############################
from nltk.tokenize import word_tokenize
import numpy as np

# Подсчет слов и символов
word_count_in_sentences = [len(word_tokenize(sentence, language='russian')) for sentence in sentences]
char_count_in_sentences = [len(sentence) for sentence in sentences]

average_sentence_length_words = np.mean(word_count_in_sentences)
average_sentence_length_chars = np.mean(char_count_in_sentences)

print(f"Средняя длина предложения в словах: {average_sentence_length_words}")
print(f"Средняя длина предложения в символах: {average_sentence_length_chars}")