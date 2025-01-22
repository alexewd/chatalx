import os
import json
import nltk
from nltk.util import ngrams
from collections import Counter
import pandas as pd
import string
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Загрузим дополнительные ресурсы для анализа
nltk.download('punkt')
nltk.download('stopwords')

# Функция для загрузки JSON файлов
def load_json_files(json_folder):
    texts = []
    for filename in os.listdir(json_folder):
        if filename.endswith('.json'):
            with open(os.path.join(json_folder, filename), 'r', encoding='utf-8') as file:
                data = json.load(file)
                texts.append(data.get('content', ''))
    return texts

# Функция для очистки текста
def clean_text(text):
    # Приводим к нижнему регистру и удаляем пунктуацию
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Разделяем текст на слова
    words = text.split()
    return words

# Функция для анализа частоты слов
def word_frequency_analysis(texts):
    all_words = []
    for text in texts:
        all_words.extend(clean_text(text))
    word_counts = Counter(all_words)
    return word_counts

# Функция для анализа средней длины слов и предложений
def average_lengths(texts):
    word_lengths = []
    sentence_lengths = []
    
    for text in texts:
        words = clean_text(text)
        word_lengths.extend([len(word) for word in words])
        
        # Разбиваем на предложения и считаем их длину
        sentences = nltk.sent_tokenize(text)
        sentence_lengths.extend([len(sentence.split()) for sentence in sentences])
    
    avg_word_length = sum(word_lengths) / len(word_lengths) if word_lengths else 0
    avg_sentence_length = sum(sentence_lengths) / len(sentence_lengths) if sentence_lengths else 0
    
    return avg_word_length, avg_sentence_length

# Функция для анализа биграмм и триграмм
def ngram_analysis(texts, n=2):
    all_ngrams = []
    
    for text in texts:
        words = clean_text(text)
        ngrams_list = ngrams(words, n)
        all_ngrams.extend(ngrams_list)
    
    ngram_counts = Counter(all_ngrams)
    return ngram_counts

# Преобразуем результат частотного анализа в DataFrame
def create_frequency_dataframe(word_counts):
    df = pd.DataFrame(word_counts.items(), columns=['Word', 'Frequency'])
    df['id'] = df.index + 1
    df = df[['id', 'Word', 'Frequency']]
    return df

# Преобразуем n-граммный анализ в DataFrame
def create_ngram_dataframe(ngram_counts):
    df = pd.DataFrame(ngram_counts.items(), columns=['Ngram', 'Frequency'])
    df['id'] = df.index + 1
    df = df[['id', 'Ngram', 'Frequency']]
    return df

# Функция для генерации wordcloud
def generate_wordcloud(word_counts):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_counts)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

# Пример использования
json_folder = 'e:/cleaned_json'

# Загружаем тексты из JSON
texts_from_json = load_json_files(json_folder)

# Анализируем частоту слов
word_counts = word_frequency_analysis(texts_from_json)

# Анализируем среднюю длину слов и предложений
avg_word_length, avg_sentence_length = average_lengths(texts_from_json)

# Анализируем биграммы и триграммы
bigram_counts = ngram_analysis(texts_from_json, n=2)
trigram_counts = ngram_analysis(texts_from_json, n=3)

# Преобразуем результаты в DataFrame
frequency_df = create_frequency_dataframe(word_counts)
bigram_df = create_ngram_dataframe(bigram_counts)
trigram_df = create_ngram_dataframe(trigram_counts)

# Выводим результаты
print("Частотность слов:")
print(frequency_df)

print("\nСредняя длина слова:", avg_word_length)
print("Средняя длина предложения:", avg_sentence_length)

print("\nБиграммы:")
print(bigram_df)

print("\nТриграммы:")
print(trigram_df)

# Генерируем и показываем wordcloud
generate_wordcloud(word_counts)

# Если хочешь сохранить в CSV
frequency_df.to_csv('word_frequency.csv', index=False)
bigram_df.to_csv('bigram_frequency.csv', index=False)
trigram_df.to_csv('trigram_frequency.csv', index=False)
