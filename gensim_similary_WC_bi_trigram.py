import os
import pandas as pd
import string
import re
from gensim.models import Word2Vec
from gensim.models import Phrases
from nltk.corpus import stopwords
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Загрузка стоп-слов
nltk.download('stopwords')
stop_words = set(stopwords.words('russian'))

# Добавление своих стоп-слов
custom_stop_words = {'в', 'он', 'и', 'который', 'которое', 'очень', 'всем', 'своей'}
stop_words = stop_words.union(custom_stop_words)

# Преобразование множества стоп-слов в список
stop_words_list = list(stop_words)

# Путь к папке с текстовыми файлами
folder_path = 'e:\\cleaned_text'

# Список для хранения предложений
sentences = []
documents = []  # Список для хранения документов для TF-IDF

# Функция для предобработки текста
def preprocess_text(text):
    # Приведение к нижнему регистру
    text = text.lower()
    # Удаление знаков пунктуации и цифр
    text = re.sub(r'[^\w\s]', '', text)  # Удаление пунктуации
    text = re.sub(r'\d+', '', text)      # Удаление цифр
    return text

# Чтение текстовых файлов из папки
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):  # Убедитесь, что это текстовый файл
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            # Чтение содержимого файла
            text = file.read()
            # Предобработка текста
            text = preprocess_text(text)
            documents.append(text)  # Добавляем обработанный текст в список документов
            # Разделение текста на предложения и слова
            for sentence in text.splitlines():
                words = sentence.split()  # Разделение на слова
                # Удаление стоп-слов
                words = [word for word in words if word not in stop_words]
                if words:  # Проверка, что предложение не пустое
                    sentences.append(words)

# Создание биграмм и триграмм
bigram = Phrases(sentences, min_count=5, threshold=10)  # Создание биграмм
trigram = Phrases(bigram[sentences], min_count=5, threshold=10)  # Создание триграмм

# Применение биграмм и триграмм к предложениям
sentences_bigrams = [bigram[sentence] for sentence in sentences]
sentences_trigrams = [trigram[sentence] for sentence in sentences_bigrams]

# Обучение модели Word2Vec
model = Word2Vec(sentences_trigrams, vector_size=100, window=5, min_count=1, workers=4)

# Поиск похожих слов
similar_words = model.wv.most_similar('человек', topn=10)

# Создание DataFrame из результатов Word2Vec
df_similar_words = pd.DataFrame(similar_words, columns=['Слово', 'Сходство'])

# Вывод таблицы с похожими словами
print("Похожие слова к 'человек':")
print(df_similar_words)

# Вычисление частоты слов
vectorizer = CountVectorizer(stop_words=stop_words_list)
count_matrix = vectorizer.fit_transform(documents)

# Получение слов и их частот
word_counts = count_matrix.toarray().sum(axis=0)
feature_names = vectorizer.get_feature_names_out()

# Создание DataFrame для частот слов
df_word_counts = pd.DataFrame(word_counts, index=feature_names, columns=['Частота'])
df_word_counts = df_word_counts.sort_values(by='Частота', ascending=False)

# Вывод таблицы самых частых слов
print("\nСамые частые слова:")
print(df_word_counts.head(10))  # Выводим топ-10 самых частых слов

# Визуализация с помощью WordCloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(df_word_counts['Частота'])

# Отображение WordCloud
# Отображение WordCloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')  # Отключаем оси
plt.show()

# Вычисление частоты биграмм
bigram_vectorizer = CountVectorizer(ngram_range=(2, 2), stop_words=stop_words_list)
bigram_count_matrix = bigram_vectorizer.fit_transform([' '.join(sentence) for sentence in sentences_bigrams])

# Получение биграмм и их частот
bigram_word_counts = bigram_count_matrix.toarray().sum(axis=0)
bigram_feature_names = bigram_vectorizer.get_feature_names_out()

# Создание DataFrame для частот биграмм
df_bigram_counts = pd.DataFrame(bigram_word_counts, index=bigram_feature_names, columns=['Частота'])
df_bigram_counts = df_bigram_counts.sort_values(by='Частота', ascending=False)

# Вывод таблицы самых частых биграмм
print("\nСамые частые биграммы:")
print(df_bigram_counts.head(10))  # Выводим топ-10 самых частых биграмм

# Вычисление частоты триграмм
trigram_vectorizer = CountVectorizer(ngram_range=(3, 3), stop_words=stop_words_list)
trigram_count_matrix = trigram_vectorizer.fit_transform([' '.join(sentence) for sentence in sentences_trigrams])

# Получение триграмм и их частот
trigram_word_counts = trigram_count_matrix.toarray().sum(axis=0)
trigram_feature_names = trigram_vectorizer.get_feature_names_out()

# Создание DataFrame для частот триграмм
df_trigram_counts = pd.DataFrame(trigram_word_counts, index=trigram_feature_names, columns=['Частота'])
df_trigram_counts = df_trigram_counts.sort_values(by='Частота', ascending=False)

# Вывод таблицы самых частых триграмм
print("\nСамые частые триграммы:")
print(df_trigram_counts.head(10))  # Выводим топ-10 самых частых триграмм

# Визуализация биграмм с помощью WordCloud
bigram_wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(dict(zip(bigram_feature_names, bigram_word_counts)))

# Визуализация триграмм с помощью WordCloud
trigram_wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(dict(zip(trigram_feature_names, trigram_word_counts)))

# Отображение WordCloud для биграмм
plt.figure(figsize=(10, 5))
plt.imshow(bigram_wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Биграммы')
plt.show()

# Отображение WordCloud для триграмм
plt.figure(figsize=(10, 5))
plt.imshow(trigram_wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Триграммы')
plt.show()
