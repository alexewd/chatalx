import re
import nltk
from nltk.probability import FreqDist
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords

# scikit-learn !!! package

# Загрузите библиотеку nltk
nltk.download('punkt')
# Загрузка стоп-слов для русского языка
nltk.download('stopwords')
russian_stopwords = stopwords.words('russian')

# Создание списка своих стоп-слов
my_stopwords = ["не","на","только","с","к","я","о","а","ему","от","у","она","но",\
"так","все","было","что","и","в","его","как","из","еще","за","это","бы","вы","то",\
"он","же","по","ее","это", "в", "с", "и", "который", "свой", "весь", "хотя", "вообще,",\
 "ох", "всё", "ты","который","которые","ежели", "очень", "бы", "что-то", "—", "…","— "," —"]

# Объединение своих стоп-слов со стандартными стоп-словами
all_stopwords = list(set(russian_stopwords).union(set(my_stopwords)))
# Открыть файл текста
# Чтение файла
with open('posl_29.02.24.txt', 'r', encoding='utf-8') as file:
    text = file.readlines()

# Препроцессинг текста
# Удаление цифр и специальных символов
text = re.sub(r'\d+', '', text)
text = re.sub(r'[^\w\s]', '', text)

# Разделение текста на слова
words = nltk.word_tokenize(text.lower())

# Подсчет частоты слов
freq_dist = FreqDist(words)

# Вывод 10 самых частотных слов
print('Top 10 most frequent words:')
top_10 = freq_dist.most_common(10)
for word, freq in top_10:
    print(f'{word}: {freq}')

# Вывод всех слов с их частотой
print('\nAll words and their frequencies:')
for word, freq in freq_dist.items():
    print(f'{word}: {freq}')

##################################
# Создание векторизатора с обновленным списком стоп-слов
vectorizer = CountVectorizer(stop_words=all_stopwords)

# Преобразование текста в документ-термин матрицу (DTM)
dtm = vectorizer.fit_transform(text)

# Преобразование DTM в DataFrame
term_matrix_df = pd.DataFrame(dtm.toarray(), columns=vectorizer.get_feature_names_out())

# Вывод первых строк и столбцов
# print(term_matrix_df.iloc[:5, :10])  # Вывод первых 5 строк и 10 столбцов

# Частотный анализ
term_freq = term_matrix_df.sum(axis=0).sort_values(ascending=False)
top_terms = term_freq.head(20)
print(top_terms)

# Анализ ассоциаций терминов (например, для термина "Счастье")
# Скорее находит где вместе слова в предложении встречаются !!!
target_term = 'счастье'
if target_term in vectorizer.get_feature_names_out():
    target_index = vectorizer.get_feature_names_out().tolist().index(target_term)
    similarities = cosine_similarity(dtm.T[target_index], dtm.T).flatten()
    
    # Преобразование результата в DataFrame
    assoc_df = pd.DataFrame({
        'term': vectorizer.get_feature_names_out(),
        'correlation': similarities
    }).sort_values(by='correlation', ascending=False)
    
    print(assoc_df.head(30))
else:
    print(f"Term '{target_term}' not found in the text data.")