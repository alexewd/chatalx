import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from collections import Counter
import re
from fuzzywuzzy import fuzz
import matplotlib.pyplot as plt

# Загрузка необходимых данных NLTK
nltk.download('punkt')
nltk.download('stopwords')

# Функция для чтения текстового файла
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Функция для очистки текста
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Удаляем знаки препинания
    return text

# Анализ частотности слов
def word_frequency(text):
    words = word_tokenize(clean_text(text))
    stop_words = set(stopwords.words('english'))  # Можно заменить на 'russian' для русского текста
    words = [word for word in words if word not in stop_words]
    return Counter(words)

# Анализ длины предложений
def sentence_length_analysis(text):
    sentences = sent_tokenize(text)
    lengths = [len(word_tokenize(sent)) for sent in sentences]
    return sum(lengths) / len(lengths) if lengths else 0, lengths

# Сравнение текстов с помощью нечёткого поиска
def fuzzy_comparison(text1, text2, sample_size=1000):
    text1_chunk = clean_text(text1)[:sample_size]
    text2_chunk = clean_text(text2)[:sample_size]
    return fuzz.ratio(text1_chunk, text2_chunk)

# Основная функция анализа
def analyze_authorship(file1, file2):
    # Чтение файлов
    text1 = read_file(file1)
    text2 = read_file(file2)

    # Частотность слов
    freq1 = word_frequency(text1)
    freq2 = word_frequency(text2)

    # Топ-10 слов
    print(f"Топ-10 слов в {file1}: {freq1.most_common(10)}")
    print(f"Топ-10 слов в {file2}: {freq2.most_common(10)}")

    # Пересечение общих слов
    common_words = set(freq1.keys()) & set(freq2.keys())
    print(f"Количество общих слов: {len(common_words)}")

    # Анализ длины предложений
    avg_len1, lengths1 = sentence_length_analysis(text1)
    avg_len2, lengths2 = sentence_length_analysis(text2)
    print(f"Средняя длина предложений в {file1}: {avg_len1:.2f} слов")
    print(f"Средняя длина предложений в {file2}: {avg_len2:.2f} слов")

    # Нечёткое сравнение
    fuzzy_score = fuzzy_comparison(text1, text2)
    print(f"Нечёткое сходство между текстами: {fuzzy_score}%")

    # Визуализация длины предложений
    plt.hist(lengths1, bins=20, alpha=0.5, label=file1)
    plt.hist(lengths2, bins=20, alpha=0.5, label=file2)
    plt.legend(loc='upper right')
    plt.title('Распределение длины предложений')
    plt.xlabel('Количество слов в предложении')
    plt.ylabel('Частота')
    plt.show()

# Запуск анализа
if __name__ == "__main__":
    file1 = "author_1.txt"
    file2 = "author_2.txt"
    analyze_authorship(file1, file2)