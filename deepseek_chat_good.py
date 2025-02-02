import os
import re
from collections import Counter
import math
import numpy as np
from Levenshtein import distance as lev_distance
import time

# Список русских стоп-слов
russian_stopwords = set([
    "и", "в", "во", "не", "что", "он", "на", "я", "с", "со", "как", "а", "то", "все", "она", "так", "его", 
    "но", "да", "ты", "к", "у", "же", "вы", "за", "бы", "по", "только", "ее", "мне", "было", "вот", "от", 
    "меня", "еще", "нет", "о", "из", "ему", "теперь", "когда", "даже", "ну", "вдруг", "ли", "если", "уже", 
    "или", "ни", "быть", "был", "него", "до", "вас", "нибудь", "опять", "уж", "вам", "ведь", "там", "потом", 
    "себя", "ничего", "ей", "может", "они", "тут", "где", "есть", "надо", "ней", "для", "мы", "тебя", "их", 
    "чем", "была", "сам", "чтоб", "без", "будто", "чего", "раз", "тоже", "себе", "под", "будет", "ж", "тогда", 
    "кто", "этот", "того", "потому", "этого", "какой", "совсем", "ним", "здесь", "этом", "один", "почти", "мой", 
    "тем", "чтобы", "нее", "сейчас", "были", "куда", "зачем", "всех", "никогда", "можно", "при", "наконец", "два", 
    "об", "другой", "хоть", "после", "над", "больше", "тот", "через", "эти", "нас", "про", "всего", "них", "какая", 
    "много", "разве", "три", "эту", "моя", "впрочем", "хорошо", "свою", "этой", "перед", "иногда", "лучше", "чуть", 
    "том", "нельзя", "такой", "им", "более", "всегда", "конечно", "всю", "между"
])

# Функция для загрузки текста из файла
def load_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Функция для загрузки всех текстов из каталога
def load_texts_from_directory(directory):
    texts = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            texts.append(load_text(file_path))
    return " ".join(texts)  # Объединяем все тексты в один

# Функция для предобработки текста
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Удаляем пунктуацию
    text = re.sub(r'\d+', '', text)  # Удаляем цифры
    tokens = text.split()
    tokens = [word for word in tokens if word not in russian_stopwords and len(word) > 2]  # Удаляем стоп-слова и короткие слова
    return tokens

# Функция для расчета расстояния Кульбака-Лейблера
def kullback_leibler_divergence(p, q):
    epsilon = 1e-10  # Чтобы избежать деления на ноль
    return sum(p[i] * math.log((p[i] + epsilon) / (q[i] + epsilon)) for i in range(len(p)))

# Функция для расчета коэффициента Жаккара
def jaccard_coefficient(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0

# Упрощенная функция для расчета среднего расстояния Левенштейна
def average_levenshtein_distance(text1, text2, sample_size=100):
    tokens1 = preprocess_text(text1)
    tokens2 = preprocess_text(text2)
    # Берем только sample_size слов для ускорения
    sample1 = np.random.choice(tokens1, min(len(tokens1), sample_size), replace=False)
    sample2 = np.random.choice(tokens2, min(len(tokens2), sample_size), replace=False)
    distances = [lev_distance(t1, t2) for t1 in sample1 for t2 in sample2]
    return np.mean(distances) if distances else 0

# Функция для стилометрического анализа
def stylometric_analysis(text):
    sentences = re.split(r'[.!?]', text)
    sentence_lengths = [len(s.split()) for s in sentences if s]
    avg_sentence_length = np.mean(sentence_lengths) if sentence_lengths else 0
    words = preprocess_text(text)
    word_freq = Counter(words)
    lexical_diversity = len(word_freq) / len(words) if words else 0
    return avg_sentence_length, lexical_diversity

# Основная функция для сравнения текста с каталогами
def compare_text_with_catalogs(unknown_text, catalog1_text, catalog2_text):
    print("Начало обработки...")
    start_time = time.time()

    # Предобработка текстов
    print("Предобработка текстов...")
    unknown_tokens = set(preprocess_text(unknown_text))
    catalog1_tokens = set(preprocess_text(catalog1_text))
    catalog2_tokens = set(preprocess_text(catalog2_text))

    # Оптимизированный частотный анализ
    print("Частотный анализ...")
    start_freq_time = time.time()

    # Подсчет частот для каждого текста
    unknown_counter = Counter(preprocess_text(unknown_text))
    catalog1_counter = Counter(preprocess_text(catalog1_text))
    catalog2_counter = Counter(preprocess_text(catalog2_text))

    # Создание общего списка уникальных слов
    all_words = list(set(unknown_counter.keys()).union(set(catalog1_counter.keys())).union(set(catalog2_counter.keys())))

    # Создание векторов частот
    unknown_vec = np.array([unknown_counter.get(word, 0) for word in all_words])
    catalog1_vec = np.array([catalog1_counter.get(word, 0) for word in all_words])
    catalog2_vec = np.array([catalog2_counter.get(word, 0) for word in all_words])

    # Нормализация векторов
    unknown_vec = unknown_vec / np.sum(unknown_vec) if np.sum(unknown_vec) != 0 else unknown_vec
    catalog1_vec = catalog1_vec / np.sum(catalog1_vec) if np.sum(catalog1_vec) != 0 else catalog1_vec
    catalog2_vec = catalog2_vec / np.sum(catalog2_vec) if np.sum(catalog2_vec) != 0 else catalog2_vec

    print(f"Частотный анализ завершен за {time.time() - start_freq_time:.2f} секунд.")

    # Расстояние Кульбака-Лейблера
    print("Расчет KLD...")
    kld1 = kullback_leibler_divergence(unknown_vec, catalog1_vec)
    kld2 = kullback_leibler_divergence(unknown_vec, catalog2_vec)

    # Коэффициент Жаккара
    print("Расчет коэффициента Жаккара...")
    jaccard1 = jaccard_coefficient(unknown_tokens, catalog1_tokens)
    jaccard2 = jaccard_coefficient(unknown_tokens, catalog2_tokens)

    # Расстояние Левенштейна
    print("Расчет расстояния Левенштейна...")
    lev1 = average_levenshtein_distance(unknown_text, catalog1_text)
    lev2 = average_levenshtein_distance(unknown_text, catalog2_text)

    # Стилометрия
    print("Стилометрический анализ...")
    unknown_style = stylometric_analysis(unknown_text)
    catalog1_style = stylometric_analysis(catalog1_text)
    catalog2_style = stylometric_analysis(catalog2_text)

    # Сравнение стилометрических характеристик
    style_diff1 = np.linalg.norm(np.array(unknown_style) - np.array(catalog1_style))
    style_diff2 = np.linalg.norm(np.array(unknown_style) - np.array(catalog2_style))

    # Агрегация результатов
    print("Агрегация результатов...")
    score1 = (1 / (1 + kld1)) + jaccard1 + (1 / (1 + lev1)) + (1 / (1 + style_diff1))
    score2 = (1 / (1 + kld2)) + jaccard2 + (1 / (1 + lev2)) + (1 / (1 + style_diff2))

    # Нормализация вероятностей
    total_score = score1 + score2
    prob1 = score1 / total_score
    prob2 = score2 / total_score

    print(f"Обработка завершена за {time.time() - start_time:.2f} секунд.")
    return prob1, prob2

# Пути к каталогам и файлу
leskov_dir = 'e:/cleaned_text'
tolstoy_dir = 'd:/tolstoy_texts'
unknown_text_path = 'd:/goncharov/nnn.txt'

# Загрузка текстов
print("Загрузка текстов...")
leskov_text = load_texts_from_directory(leskov_dir)
tolstoy_text = load_texts_from_directory(tolstoy_dir)
unknown_text = load_text(unknown_text_path)

# Сравнение текста с каталогами
prob_leskov, prob_tolstoy = compare_text_with_catalogs(unknown_text, leskov_text, tolstoy_text)

# Вывод результатов
print(f"Вероятность принадлежности Лескову: {prob_leskov:.2f}")
print(f"Вероятность принадлежности Толстому: {prob_tolstoy:.2f}")