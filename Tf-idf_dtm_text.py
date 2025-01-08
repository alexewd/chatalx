import re
from nltk.corpus import stopwords
from nltk import word_tokenize, sent_tokenize
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 1. Загрузка текста
file_path = "f:/chatepc/chatalx/work/data/Обрыв.txt"
with open(file_path, 'r', encoding='utf-8') as file:
    text_data = file.read()

# 2. Очистка текста
def clean_text(text):
    text = text.lower()  # Приводим к нижнему регистру
    text = re.sub(r"[^а-яА-ЯёЁ\s]", " ", text)  # Удаляем всё, кроме букв и пробелов
    text = re.sub(r"\s+", " ", text)  # Удаляем лишние пробелы
    text = text.strip()  # Убираем пробелы в начале и конце строки
    return text

text_data_cleaned = clean_text(text_data)

# Проверяем, что текст не пуст после очистки
if not text_data_cleaned:
    raise ValueError("Текст пуст после очистки. Проверьте входные данные или параметры очистки.")

# 3. Разбиение текста на предложения
sentences = sent_tokenize(text_data_cleaned, language='russian')
# Дополнительная проверка предложений
print(f"Количество предложений: {len(sentences)}")
print(f"Пример предложений: {sentences[:5]}")

# Если предложений нет, выводим сообщение
if len(sentences) == 0:
    print("Не удалось разделить текст на предложения.")
else:
    # Анализ длины предложений в символах
    sentence_lengths = [len(sentence) for sentence in sentences]
    average_sentence_length = np.mean(sentence_lengths)
    print(f"Средняя длина предложения в символах: {average_sentence_length}")

    # Анализ количества слов в каждом предложении
    word_count_in_sentences = [len(word_tokenize(sentence, language='russian')) for sentence in sentences]
    average_sentence_length_words = np.mean(word_count_in_sentences)
    print(f"Средняя длина предложения в словах: {average_sentence_length_words}")

# 4. Создание словаря с биграммами и триграммами
stop_words = stopwords.words('russian')  # Преобразуем множество в список
vectorizer = CountVectorizer(ngram_range=(1, 3), stop_words=stop_words)
dtm = vectorizer.fit_transform(sentences)

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