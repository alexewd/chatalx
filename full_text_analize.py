import pandas as pd
import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from tqdm import tqdm
import string

# Загрузка ресурсов NLTK
nltk.download('punkt')
nltk.download('stopwords')

# Функция для загрузки текста
def load_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

# Функция для анализа пунктуации и не буквенных символов
def analyze_punctuation(text):
    punctuation_counts = Counter(char for char in text if char in string.punctuation or char in string.whitespace)
    punctuation_df = pd.DataFrame(punctuation_counts.items(), columns=['Symbol', 'Count'])
    return punctuation_df.sort_values(by='Count', ascending=False)

# Функция для анализа цифр с примером предложения
def analyze_digits(text):
    sentences = sent_tokenize(text)
    digit_data = []
    digit_pattern = r'\d+'
    
    for sentence in tqdm(sentences, desc="Analyzing digits"):
        digits = re.findall(digit_pattern, sentence)
        for digit in set(digits):  # Уникальные цифры в предложении
            digit_data.append({'Digit': digit, 'Sentence': sentence})
    
    digits_df = pd.DataFrame(digit_data)
    if not digits_df.empty:
        digits_df = digits_df.groupby('Digit').agg({'Sentence': 'first', 'Digit': 'size'}).rename(columns={'Digit': 'Count'}).reset_index()
    return digits_df

# Функция для очистки текста
def clean_text(text):
    # Приведение к нижнему регистру и удаление пунктуации
    text = text.lower()
    text = re.sub(f'[{string.punctuation}]', ' ', text)
    # Удаление цифр
    text = re.sub(r'\d+', ' ', text)
    # Удаление лишних пробелов
    text = ' '.join(text.split())
    return text

# Функция для получения частоты слов (без стоп-слов)
def word_frequency(text):
    stop_words = set(stopwords.words('russian'))
    words = word_tokenize(text)
    words = [word for word in words if word not in stop_words]
    word_counts = Counter(words)
    word_df = pd.DataFrame(word_counts.items(), columns=['Word', 'Count'])
    return word_df.sort_values(by='Count', ascending=False)

# Функция для получения биграмм
def bigrams_frequency(text):
    words = word_tokenize(text)
    stop_words = set(stopwords.words('russian'))
    words = [word for word in words if word not in stop_words]
    bigrams = [(words[i], words[i+1]) for i in range(len(words)-1)]
    bigram_counts = Counter(bigrams)
    bigram_df = pd.DataFrame(bigram_counts.items(), columns=['Bigram', 'Count'])
    bigram_df['Bigram'] = bigram_df['Bigram'].apply(lambda x: ' '.join(x))
    return bigram_df.sort_values(by='Count', ascending=False)

# Функция для получения триграмм
def trigrams_frequency(text):
    words = word_tokenize(text)
    stop_words = set(stopwords.words('russian'))
    words = [word for word in words if word not in stop_words]
    trigrams = [(words[i], words[i+1], words[i+2]) for i in range(len(words)-2)]
    trigram_counts = Counter(trigrams)
    trigram_df = pd.DataFrame(trigram_counts.items(), columns=['Trigram', 'Count'])
    trigram_df['Trigram'] = trigram_df['Trigram'].apply(lambda x: ' '.join(x))
    return trigram_df.sort_values(by='Count', ascending=False)

# Функция для подсчета средней длины предложений
def average_sentence_length(text):
    sentences = sent_tokenize(text)
    lengths = [len(word_tokenize(sentence)) for sentence in sentences]
    return sum(lengths) / len(lengths) if lengths else 0

# Основная функция
def main(file_path):
    print("Loading text...")
    text = load_text(file_path)
    
    # Анализ пунктуации
    print("Analyzing punctuation...")
    punctuation_df = analyze_punctuation(text)
    print("\nPunctuation and Non-Alphabetic Symbols Statistics:")
    print(punctuation_df)
    
    # Анализ цифр
    print("\nAnalyzing digits...")
    digits_df = analyze_digits(text)
    print("\nDigits Statistics with Example Sentences:")
    print(digits_df)
    
    # Очистка текста
    print("\nCleaning text...")
    cleaned_text = clean_text(text)
    
    # Частота слов
    print("Calculating word frequency...")
    word_freq_df = word_frequency(cleaned_text)
    print("\nWord Frequency (Excluding Stop Words):")
    print(word_freq_df.head(10))  # Показываем топ-10 для краткости
    
    # Биграммы
    print("\nCalculating bigrams...")
    bigrams_df = bigrams_frequency(cleaned_text)
    print("\nBigrams Frequency:")
    print(bigrams_df.head(10))  # Показываем топ-10
    
    # Триграммы
    print("\nCalculating trigrams...")
    trigrams_df = trigrams_frequency(cleaned_text)
    print("\nTrigrams Frequency:")
    print(trigrams_df.head(10))  # Показываем топ-10
    
    # Средняя длина предложений
    print("\nCalculating average sentence length...")
    avg_length = average_sentence_length(text)
    print(f"\nAverage Sentence Length (in words): {avg_length:.2f}")

# Запуск программы
if __name__ == "__main__":
    file_path = 'd:/NLP_Toxic/WP/oblomov.txt'  # Укажите путь к вашему файлу
    main(file_path)