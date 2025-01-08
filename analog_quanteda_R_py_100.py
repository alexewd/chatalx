import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
import pymorphy3
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Загрузка стоп-слов для русского языка
nltk.download('stopwords')
russian_stopwords = stopwords.words('russian')

# Создание списка своих стоп-слов
my_stopwords = ["не", "на", "только", "с", "к", "я", "о", "а", "ему", "от", "у", "она", "но", "так", "все", "было", "что", "и", "в", "его", "как", "из", "еще", "за", "это", "бы", "вы", "то", "он", "же", "по", "ее", "это", "в", "с", "и", "который", "свой", "весь", "хотя", "вообще", "ох", "всё", "ты", "который", "которые", "ежели", "очень", "бы", "что-то", "—", "…", "— ", " —"]

# Чтение файла
with open('f:/chatepc/chatalx/work/data/obriv.txt', 'r', encoding='utf-8') as file:
    text_data = file.readlines()

# Объединение текста в один большой текст для анализа
full_text = ' '.join(text_data)

# Создание экземпляра морфологического анализатора
morph = pymorphy3.MorphAnalyzer()

# Разделение текста на слова
words = full_text.split()

# Поиск имен собственных с использованием pymorphy3
proper_nouns = set()
for word in words:
    parsed_word = morph.parse(word)[0]
    if 'Name' in parsed_word.tag:  # Проверка, является ли слово именем собственным
        proper_nouns.add(word)

# Выводим найденные имена собственные таблицей
proper_nouns_df = pd.DataFrame(list(proper_nouns), columns=["Имена собственные"])
print("\nНайденные имена собственные:")
print(proper_nouns_df)

# Объединение своих стоп-слов со стандартными стоп-словами и найденными именами собственными
all_stopwords = list(set(russian_stopwords).union(set(my_stopwords)).union(proper_nouns))

# Создание векторизатора с обновленным списком стоп-слов
vectorizer = CountVectorizer(stop_words=all_stopwords)

# Преобразование текста в документ-термин матрицу (DTM)
dtm = vectorizer.fit_transform(text_data)

# Преобразование DTM в DataFrame
term_matrix_df = pd.DataFrame(dtm.toarray(), columns=vectorizer.get_feature_names_out())

# Частотный анализ
term_freq = term_matrix_df.sum(axis=0).sort_values(ascending=False)
top_terms = term_freq.head(30)
print("\n30 наиболее частых терминов:")
print(top_terms)

# Анализ ассоциаций терминов (например, для термина "любовь")
target_term = 'любовь'
if target_term in vectorizer.get_feature_names_out():
    target_index = vectorizer.get_feature_names_out().tolist().index(target_term)
    similarities = cosine_similarity(dtm.T[target_index], dtm.T).flatten()
    
    # Преобразование результата в DataFrame
    assoc_df = pd.DataFrame({
        'term': vectorizer.get_feature_names_out(),
        'correlation': similarities
    }).sort_values(by='correlation', ascending=False)
    
    print(f"\nАссоциации для термина '{target_term}':")
    print(assoc_df.head(20))
else:
    print(f"\nТермин '{target_term}' не найден в тексте.")

# Создание облака слов для 30 самых частых слов
wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(top_terms.to_dict())

# Отображение облака слов
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Облако слов для 30 самых частых слов')
plt.show()