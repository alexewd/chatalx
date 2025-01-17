import pandas as pd
from collections import Counter
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.feature_extraction.text import CountVectorizer

# Убедимся, что необходимые пакеты скачаны
nltk.download('punkt')

def read_and_split(file_path):
    """Считывает файл и разбивает текст на предложения."""
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    sentences = sent_tokenize(text)
    return sentences

def word_frequency(text):
    """Подсчитывает частоту слов в тексте."""
    words = word_tokenize(text.lower())
    words = [word for word in words if word.isalnum()]
    freq = Counter(words)
    return freq

def bigram_frequency(text):
    """Подсчитывает частоту биграмм в тексте."""
    vectorizer = CountVectorizer(ngram_range=(2, 2))
    bigrams = vectorizer.fit_transform([text])
    bigram_freq = dict(zip(vectorizer.get_feature_names_out(), bigrams.toarray()[0]))
    return bigram_freq

def create_frequency_dataframe(freq_dict, bigram_dict, label):
    """Создаёт DataFrame из словарей частот слов и биграмм."""
    words_df = pd.DataFrame(list(freq_dict.items()), columns=['Term', f'{label}_Word_Frequency'])
    bigrams_df = pd.DataFrame(list(bigram_dict.items()), columns=['Bigram', f'{label}_Bigram_Frequency'])
    combined_df = pd.concat([words_df.set_index('Term'), bigrams_df.set_index('Bigram')], axis=1).reset_index()
    return combined_df

def main():
    # Пути к файлам
    file1 = r'e:\\posl\\data\\posl_04.12.12.txt'
    file2 = r'e:\\posl\\data\\posl_29.02.24.txt'

    # Чтение и обработка файлов
    sentences1 = read_and_split(file1)
    sentences2 = read_and_split(file2)

    # Создание датафрейма для предложений
    max_len = max(len(sentences1), len(sentences2))
    sentences1 += [''] * (max_len - len(sentences1))  # Заполняем пустые строки
    sentences2 += [''] * (max_len - len(sentences2))

    df = pd.DataFrame({
        'Index': range(1, max_len + 1),
        'File1_Sentences': sentences1,
        'File2_Sentences': sentences2
    })

    # Объединяем текст каждой речи
    text1 = ' '.join(sentences1)
    text2 = ' '.join(sentences2)

    # Подсчёт частот слов и биграмм для каждой речи
    freq1 = word_frequency(text1)
    freq2 = word_frequency(text2)
    bigram_freq1 = bigram_frequency(text1)
    bigram_freq2 = bigram_frequency(text2)

    # Создание датафрейма для частотных данных
    df_freq1 = create_frequency_dataframe(freq1, bigram_freq1, 'File1')
    df_freq2 = create_frequency_dataframe(freq2, bigram_freq2, 'File2')

    # Объединение данных в один датафрейм
    df2 = pd.merge(df_freq1, df_freq2, how='outer', on='index').fillna(0)

    # Сохраняем результаты
    output_path_sentences = r'e:\\posl\\data\\sentences_result.xlsx'
    output_path_frequencies = r'e:\\posl\\data\\frequencies_result.xlsx'

    df.to_excel(output_path_sentences, index=False)
    df2.to_excel(output_path_frequencies, index=False)

    print(f"Результат сохранён в {output_path_sentences} и {output_path_frequencies}")
    print(df.sample(10))
    print(df2.sample(10))
    
if __name__ == "__main__":
    main()
