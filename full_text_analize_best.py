import pandas as pd
import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from tqdm import tqdm
import string
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

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
        for digit in set(digits):
            digit_data.append({'Digit': digit, 'Sentence': sentence})
    
    digits_df = pd.DataFrame(digit_data)
    if not digits_df.empty:
        digits_df = digits_df.groupby('Digit').agg({'Sentence': 'first', 'Digit': 'size'}).rename(columns={'Digit': 'Count'}).reset_index()
    return digits_df

# Функция для извлечения имен собственных и ФИО
def extract_proper_nouns(text):
    sentences = sent_tokenize(text)
    proper_nouns = []
    
    for sentence in tqdm(sentences, desc="Extracting proper nouns"):
        words = word_tokenize(sentence)
        for i, word in enumerate(words):
            if word[0].isupper() and (i > 0 or not sentence.startswith(word)):
                if i < len(words)-1 and words[i+1][0].isupper():
                    proper_nouns.append(f"{word} {words[i+1]}")
                else:
                    proper_nouns.append(word)
    
    proper_noun_counts = Counter(proper_nouns)
    proper_noun_df = pd.DataFrame(proper_noun_counts.items(), columns=['Proper Noun/FIO', 'Count'])
    return proper_noun_df.sort_values(by='Count', ascending=False)

# Функция для проверки, является ли строка римской цифрой
def is_roman_numeral(text):
    roman_pattern = r'^(?=[MDCLXVI])M*(C[MD]|D?C{0,3})(X[CL]|L?X{0,3})(I[XV]|V?I{0,3})$'
    return bool(re.match(roman_pattern, text))

# Функция для извлечения римских цифр и первого предложения главы
def extract_roman_numerals(text):
    sentences = sent_tokenize(text)
    roman_data = []
    current_chapter_start = None
    
    # Регулярное выражение для римских цифр (I, II, III, etc.)
    roman_pattern = r'\b[IVXLCDM]+\b'
    
    for i, sentence in enumerate(tqdm(sentences, desc="Extracting Roman numerals")):
        romans = re.findall(roman_pattern, sentence)
        for roman in romans:
            if is_roman_numeral(roman):  # Проверяем, что это действительно римская цифра
                # Сохраняем первое предложение после римской цифры как начало главы
                if i < len(sentences) - 1:
                    chapter_start = sentences[i + 1]
                else:
                    chapter_start = sentence
                roman_data.append({'Roman Numeral': roman, 'First Sentence': chapter_start})
    
    roman_df = pd.DataFrame(roman_data)
    if not roman_df.empty:
        roman_df = roman_df.groupby('Roman Numeral').agg({'First Sentence': 'first', 'Roman Numeral': 'size'}).rename(columns={'Roman Numeral': 'Count'}).reset_index()
    return roman_df

# Функция для извлечения слов на латинице (исключая римские цифры)
def extract_latin_words(text):
    latin_pattern = r'\b[a-zA-ZÀ-ÿ]+(?:-[a-zA-ZÀ-ÿ]+)?\b'
    latin_words = re.findall(latin_pattern, text)
    # Исключаем римские цифры
    latin_words = [word for word in latin_words if not is_roman_numeral(word.upper())]
    latin_word_counts = Counter(latin_words)
    latin_df = pd.DataFrame(latin_word_counts.items(), columns=['Latin Word', 'Count'])
    return latin_df.sort_values(by='Count', ascending=False)

# Функция для очистки текста
def clean_text(text):
    text = text.lower()
    text = re.sub(f'[{string.punctuation}]', ' ', text)
    text = re.sub(r'\d+', ' ', text)
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

# Функция для TF-IDF анализа (исключая имена собственные)
def tfidf_analysis(text, proper_nouns):
    sentences = sent_tokenize(text)
    stop_words = set(stopwords.words('russian'))
    proper_nouns_set = set(word.lower() for word in proper_nouns['Proper Noun/FIO'].str.split().explode())
    
    # Очистка предложений для TF-IDF
    cleaned_sentences = []
    for sent in sentences:
        words = [word.lower() for word in word_tokenize(sent) if word.lower() not in stop_words and word.isalpha() and word.lower() not in proper_nouns_set]
        cleaned_sentences.append(' '.join(words))
    
    # Выполнение TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(cleaned_sentences)
    feature_names = vectorizer.get_feature_names_out()
    
    # Среднее значение TF-IDF для каждого слова
    tfidf_scores = np.mean(tfidf_matrix.toarray(), axis=0)
    tfidf_df = pd.DataFrame({'Word': feature_names, 'TF-IDF Score': tfidf_scores})
    return tfidf_df.sort_values(by='TF-IDF Score', ascending=False)

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
    
    # Извлечение имен собственных и ФИО
    print("\nExtracting proper nouns and FIO...")
    proper_noun_df = extract_proper_nouns(text)
    print("\nProper Nouns and FIO Statistics:")
    print(proper_noun_df.head(10))
    
    # Извлечение римских цифр
    print("\nExtracting Roman numerals...")
    roman_df = extract_roman_numerals(text)
    print("\nRoman Numerals Statistics with First Sentence of Chapter:")
    print(roman_df)
    
    # Извлечение слов на латинице
    print("\nExtracting Latin words...")


    latin_df = extract_latin_words(text)
    print("\nLatin Words Statistics (Excluding Roman Numerals):")
    print(latin_df.head(10))
    
    # Очистка текста
    print("\nCleaning text...")
    cleaned_text = clean_text(text)
    
    # Частота слов
    print("Calculating word frequency...")
    word_freq_df = word_frequency(cleaned_text)
    print("\nWord Frequency (Excluding Stop Words):")
    print(word_freq_df.head(10))
    
    # Биграммы
    print("\nCalculating bigrams...")
    bigrams_df = bigrams_frequency(cleaned_text)
    print("\nBigrams Frequency:")
    print(bigrams_df.head(10))
    
    # Триграммы
    print("\nCalculating trigrams...")
    trigrams_df = trigrams_frequency(cleaned_text)
    print("\nTrigrams Frequency:")
    print(trigrams_df.head(10))
    
    # TF-IDF анализ
    print("\nCalculating TF-IDF...")
    tfidf_df = tfidf_analysis(text, proper_noun_df)
    print("\nTF-IDF Analysis (Excluding Proper Nouns):")
    print(tfidf_df.head(10))
    
    # Средняя длина предложений
    print("\nCalculating average sentence length...")
    avg_length = average_sentence_length(text)
    print(f"\nAverage Sentence Length (in words): {avg_length:.2f}")

# Запуск программы
if __name__ == "__main__":
    file_path = 'd:/NLP_Toxic/WP/oblomov.txt'  # Укажите путь к вашему файлу
    main(file_path)
