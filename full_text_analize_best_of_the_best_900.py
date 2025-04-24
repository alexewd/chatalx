import pandas as pd
import nltk
import re
from collections import Counter
from nltk.tokenize import sent_tokenize, word_tokenize
from ufal.udpipe import Model, Pipeline, ProcessingError
import multiprocessing
import wordcloud
import matplotlib.pyplot as plt
from stop_words import get_stop_words
import os

# Загрузка текста
text_file = "D:/NLP_Toxic/WP/oblomov.txt"
if not os.path.exists(text_file):
    raise FileNotFoundError("Файл не найден!")
with open(text_file, 'r', encoding='utf-8') as f:
    text_lines = f.readlines()
text = ' '.join(text_lines)

# 2. Статистика по знакам пунктуации
punct_chars = [c for c in text if not c.isalnum()]
punct_freq = Counter(punct_chars)
punct_table = pd.DataFrame(punct_freq.items(), columns=['Symbol', 'Frequency']).sort_values(by='Frequency', ascending=False)
print("Таблица частоты знаков пунктуации и не буквенных символов:")
print(punct_table)

# 3. Статистика по цифрам с примерами предложений
sentences = sent_tokenize(text, language='russian')
number_matches = [re.findall(r'\d', sent) for sent in sentences]
number_freq = Counter([num for sublist in number_matches for num in sublist])
number_table = pd.DataFrame(number_freq.items(), columns=['Number', 'Frequency'])
number_table['Example_Sentence'] = ''
for num in number_table['Number']:
    for sent in sentences:
        if num in sent:
            number_table.loc[number_table['Number'] == num, 'Example_Sentence'] = sent
            break
    if number_table.loc[number_table['Number'] == num, 'Example_Sentence'].empty:
        number_table.loc[number_table['Number'] == num, 'Example_Sentence'] = 'Нет примера'
print("Таблица частоты цифр с примерами предложений:")
print(number_table)

# 4. Таблица глав (римские цифры и первые предложения)
roman_pattern = r'^\s*(I{1,3}|IV|VI{0,3}|X{1,3})\s*\.?\s*$'
chapter_starts = [i for i, line in enumerate(text_lines) if re.match(roman_pattern, line)]
if not chapter_starts:
    print("Римские цифры не найдены. Пример строк текста:")
    print(text_lines[:10])
    raise ValueError("Проверьте формат глав в файле.")

chapter_table = pd.DataFrame(columns=['Chapter', 'First_Sentence'])
for i, start in enumerate(chapter_starts):
    chapter_num = re.match(roman_pattern, text_lines[start]).group(1).strip()
    next_line_idx = start + 1
    while next_line_idx < len(text_lines) and text_lines[next_line_idx].strip() == '':
        next_line_idx += 1
    if next_line_idx >= len(text_lines):
        next_line_idx = start
    next_text = ' '.join(text_lines[next_line_idx:])
    first_sentence = sent_tokenize(next_text, language='russian')[0] if next_text else "Нет предложения"
    chapter_table = pd.concat([chapter_table, pd.DataFrame({'Chapter': [chapter_num], 'First_Sentence': [first_sentence]})], ignore_index=True)
print("Таблица глав и первых предложений:")
print(chapter_table)

# 5. Имена собственные/ФИО (оптимизированный udpipe)
model_path = "russian-syntagrus-ud-2.5-191206.udpipe"
if not os.path.exists(model_path):
    raise FileNotFoundError("Скачайте модель 'russian-syntagrus-ud-2.5-191206.udpipe' и поместите в рабочую директорию")
model = Model.load(model_path)
if not model:
    raise RuntimeError("Не удалось загрузить модель UDPipe")

# Уменьшаем объем текста: берем уникальные предложения
unique_sentences = list(set(sentences))
max_sentences = 1000
if len(unique_sentences) > max_sentences:
    unique_sentences = unique_sentences[:max_sentences]
text_subset = ' '.join(unique_sentences)

# Аннотируем с использованием многопоточности
pipeline = Pipeline(model, 'tokenize', Pipeline.DEFAULT, Pipeline.DEFAULT, 'conllu')
error = ProcessingError()
annotated = pipeline.process(text_subset, error)
if error.occurred():
    raise RuntimeError(f"Ошибка обработки UDPipe: {error.message}")

# Парсим результат в DataFrame
lines = annotated.split('\n')
data = []
current_sentence_id = 0
for line in lines:
    if line.startswith('# text ='):
        current_sentence_id += 1
    elif line and not line.startswith('#'):
        fields = line.split('\t')
        if len(fields) >= 10:
            data.append({
                'sentence_id': current_sentence_id,
                'token': fields[1],
                'upos': fields[3],
                'head_token_id': fields[6],
                'dep_rel': fields[7]
            })
annotated_dt = pd.DataFrame(data)

# Имена собственные
proper_nouns = annotated_dt[annotated_dt['upos'] == 'PROPN'][['token']].rename(columns={'token': 'Token'})
unwanted_proper = ['Ну', 'Да']
proper_nouns = proper_nouns[~proper_nouns['Token'].isin(unwanted_proper)]
proper_nouns = proper_nouns[proper_nouns['Token'].str.len() >= 3]
proper_noun_freq = proper_nouns.groupby('Token').size().reset_index(name='Frequency').sort_values(by='Frequency', ascending=False)
print("Таблица имён собственных/ФИО:")
print(proper_noun_freq)

# 6. Слова на латинице
latin_words = re.findall(r'\b[a-zA-Z]+\b', text)
latin_freq = Counter(latin_words)
latin_table = pd.DataFrame(latin_freq.items(), columns=['Latin_Word', 'Frequency']).sort_values(by='Frequency', ascending=False)
print("Таблица слов на латинице:")
print(latin_table)

# Пользовательский список стоп-слов
custom_stopwords = ['ну', 'да', 'б', 'а', 'в', 'г']
russian_stopwords = get_stop_words('russian')
all_stopwords = list(set(russian_stopwords + custom_stopwords))

# 7. Частота слов
words = word_tokenize(text.lower(), language='russian')
words_clean = [w for w in words if w.isalpha() and w not in all_stopwords and len(w) >= 2 and w not in proper_nouns['Token'].str.lower()]
word_freq = Counter(words_clean)
word_table = pd.DataFrame(word_freq.items(), columns=['Word', 'Frequency']).sort_values(by='Frequency', ascending=False)
print("Таблица частоты слов (без стоп-слов, имен собственных, пользовательских стоп-слов и коротких слов):")
print(word_table)

# 8. Биграммы
bigrams = list(nltk.bigrams(words_clean))
bigram_freq = Counter(bigrams)
bigram_table = pd.DataFrame([(' '.join(bigram), freq) for bigram, freq in bigram_freq.items()], columns=['Bigram', 'Frequency']).sort_values(by='Frequency', ascending=False)
print("Таблица частоты биграмм:")
print(bigram_table)

# 9. Триграммы
trigrams = list(nltk.trigrams(words_clean))
trigram_freq = Counter(trigrams)
trigram_table = pd.DataFrame([(' '.join(trigram), freq) for trigram, freq in trigram_freq.items()], columns=['Trigram', 'Frequency']).sort_values(by='Frequency', ascending=False)
print("Таблица частоты триграмм:")
print(trigram_table)

# 10. Средняя длина предложений
sentence_lengths = [len([w for w in word_tokenize(sent, language='russian') if w.isalpha()]) for sent in sentences]
mean_sentence_length = sum(sentence_lengths) / len(sentence_lengths)
print(f"Средняя длина предложений (в словах): {mean_sentence_length:.2f}")

# 12. Распределение частей речи
pos_counts = annotated_dt.groupby('upos').size().reset_index(name='Count')
total_tokens = len(annotated_dt)
pos_counts['Proportion'] = pos_counts['Count'] / total_tokens
pos_counts = pos_counts.sort_values(by='Count', ascending=False)
print("Распределение частей речи:")
print(pos_counts)
pos_counts.to_csv("pos_distribution.csv", index=False)
print("Таблица распределения частей речи сохранена в pos_distribution.csv")

# 13. Относительный процент сложноподчиненных предложений
pipeline_parser = Pipeline(model, 'tokenize', Pipeline.DEFAULT, Pipeline.DEFAULT, 'conllu')
annotated_parser = pipeline_parser.process(text_subset, error)
if error.occurred():
    raise RuntimeError(f"Ошибка обработки UDPipe: {error.message}")

# Парсим результат в DataFrame
lines_parser = annotated_parser.split('\n')
data_parser = []
current_sentence_id = 0
for line in lines_parser:
    if line.startswith('# text ='):
        current_sentence_id += 1
    elif line and not line.startswith('#'):
        fields = line.split('\t')
        if len(fields) >= 10:
            data_parser.append({
                'sentence_id': current_sentence_id,
                'token': fields[1],
                'upos': fields[3],
                'head_token_id': fields[6],
                'dep_rel': fields[7]
            })
annotated_dt_parser = pd.DataFrame(data_parser)

# Подсчитываем сложноподчиненные предложения
subordinate_sentences = annotated_dt_parser[
    annotated_dt_parser['dep_rel'].isin(['advcl', 'ccomp', 'acl']) | 
    (annotated_dt_parser['upos'] == 'SCONJ')
]['sentence_id'].unique()
total_sentences = len(annotated_dt_parser['sentence_id'].unique())
subordinate_count = len(subordinate_sentences)
subordinate_percentage = (subordinate_count / total_sentences) * 100
subordinate_table = pd.DataFrame({
    'Total_Sentences': [total_sentences],
    'Subordinate_Sentences': [subordinate_count],
    'Percentage': [subordinate_percentage]
})
print("Относительный процент сложноподчиненных предложений:")
print(subordinate_table)
subordinate_table.to_csv("subordinate_sentences.csv", index=False)
print("Таблица сложноподчиненных предложений сохранена в subordinate_sentences.csv")

# 11. Визуализации
# Wordcloud
wc = wordcloud.WordCloud(width=800, height=600, max_words=100, random_state=123, background_color='white').generate_from_frequencies(dict(word_table.values))
plt.figure(figsize=(8, 6))
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.savefig("wordcloud.png")
plt.show()
print("Облако слов сохранено в wordcloud.png")

# Гистограмма для пунктуации (топ-10)
punct_top = punct_table.head(10)
plt.figure(figsize=(8, 6))
plt.bar(punct_top['Symbol'], punct_top['Frequency'], color='steelblue')
plt.title("Частота знаков пунктуации (Топ-10)")
plt.xlabel("Знак")
plt.ylabel("Частота")
plt.savefig("punctuation_plot.png")
plt.show()
print("Гистограмма пунктуации сохранена в punctuation_plot.png")

# Гистограмма для цифр
plt.figure(figsize=(8, 6))
plt.bar(number_table['Number'], number_table['Frequency'], color='darkgreen')
plt.title("Частота цифр")
plt.xlabel("Цифра")
plt.ylabel("Частота")
plt.savefig("numbers_plot.png")
plt.show()
print("Гистограмма цифр сохранена в numbers_plot.png")

# Гистограмма для имён собственных (топ-10)
proper_top = proper_noun_freq.head(10)
plt.figure(figsize=(8, 6))
plt.bar(proper_top['Token'], proper_top['Frequency'], color='purple')
plt.title("Частота имён собственных (Топ-10)")
plt.xlabel("Имя")
plt.ylabel("Частота")
plt.xticks(rotation=45, ha='right')
plt.savefig("proper_nouns_plot.png")
plt.show()
print("Гистограмма имён собственных сохранена в proper_nouns_plot.png")

# Гистограмма для слов на латинице
if not latin_table.empty:
    latin_top = latin_table.head(10)
    plt.figure(figsize=(8, 6))
    plt.bar(latin_top['Latin_Word'], latin_top['Frequency'], color='orange')
    plt.title("Частота слов на латинице (Топ-10)")
    plt.xlabel("Слово")
    plt.ylabel("Частота")
    plt.xticks(rotation=45, ha='right')
    plt.savefig("latin_words_plot.png")
    plt.show()
    print("Гистограмма слов на латинице сохранена в latin_words_plot.png")
else:
    print("Нет слов на латинице для визуализации.")

# Гистограмма для слов (топ-20)
word_top = word_table.head(20)
plt.figure(figsize=(8, 6))
plt.bar(word_top['Word'], word_top['Frequency'], color='red')
plt.title("Частота слов (Топ-20)")
plt.xlabel("Слово")
plt.ylabel("Частота")
plt.xticks(rotation=45, ha='right')
plt.savefig("word_freq_plot.png")
plt.show()
print("Гистограмма слов сохранена в word_freq_plot.png")

# Гистограмма для биграмм (топ-10)
bigram_top = bigram_table.head(10)
plt.figure(figsize=(8, 6))
plt.bar(bigram_top['Bigram'], bigram_top['Frequency'], color='blue')
plt.title("Частота биграмм (Топ-10)")
plt.xlabel("Биграмма")
plt.ylabel("Частота")
plt.xticks(rotation=45, ha='right')
plt.savefig("bigram_freq_plot.png")
plt.show()
print("Гистограмма биграмм сохранена в bigram_freq_plot.png")

# Гистограмма для триграмм (топ-10)
trigram_top = trigram_table.head(10)
plt.figure(figsize=(8, 6))
plt.bar(trigram_top['Trigram'], trigram_top['Frequency'], color='darkred')
plt.title("Частота триграмм (Топ-10)")
plt.xlabel("Триграмма")
plt.ylabel("Частота")
plt.xticks(rotation=45, ha='right')
plt.savefig("trigram_freq_plot.png")
plt.show()
print("Гистограмма триграмм сохранена в trigram_freq_plot.png")

# Гистограмма для распределения частей речи
plt.figure(figsize=(8, 6))
plt.bar(pos_counts['upos'], pos_counts['Count'], color='darkblue')
plt.title("Распределение частей речи")
plt.xlabel("Часть речи")
plt.ylabel("Частота")
plt.xticks(rotation=45, ha='right')
plt.savefig("pos_distribution_plot.png")
plt.show()
print("Гистограмма распределения частей речи сохранена в pos_distribution_plot.png")

# Сохранение результатов в CSV
punct_table.to_csv("punctuation_stats.csv", index=False)
number_table.to_csv("number_stats.csv", index=False)
chapter_table.to_csv("chapter_stats.csv", index=False)
proper_noun_freq.to_csv("proper_nouns.csv", index=False)
latin_table.to_csv("latin_words.csv", index=False)
word_table.to_csv("word_freq.csv", index=False)
bigram_table.to_csv("bigram_freq.csv", index=False)
trigram_table.to_csv("trigram_freq.csv", index=False)
pos_counts.to_csv("pos_distribution.csv", index=False)
subordinate_table.to_csv("subordinate_sentences.csv", index=False)
pd.DataFrame({'Mean_Sentence_Length': [mean_sentence_length]}).to_csv("sentence_length.csv", index=False)