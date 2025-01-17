import pandas as pd
from collections import Counter
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

# Убедимся, что необходимые пакеты скачаны
nltk.download('punkt')

def read_and_split(file_path):
    """Считывает файл и разбивает текст на предложения."""
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    sentences = sent_tokenize(text)
    return sentences

def word_frequency(sentence):
    """Подсчитывает частоту слов в предложении."""
    words = word_tokenize(sentence.lower())
    words = [word for word in words if word.isalnum()]
    freq = Counter(words)
    return freq

def main():
    # Пути к файлам
    file1 = r'e:\\posl\\data\\posl_04.12.12.txt'
    file2 = r'e:\\posl\\data\\posl_29.02.24.txt'

    # Чтение и обработка файлов
    sentences1 = read_and_split(file1)
    sentences2 = read_and_split(file2)

    # Создание датафрейма
    max_len = max(len(sentences1), len(sentences2))
    sentences1 += [''] * (max_len - len(sentences1))  # Заполняем пустые строки
    sentences2 += [''] * (max_len - len(sentences2))

    df = pd.DataFrame({
        'Index': range(1, max_len + 1),
        'File1_Sentences': sentences1,
        'File2_Sentences': sentences2
    })

    # Подсчёт частоты слов для каждого предложения
    df['File1_Frequency'] = df['File1_Sentences'].apply(lambda x: word_frequency(x))
    df['File2_Frequency'] = df['File2_Sentences'].apply(lambda x: word_frequency(x))

    # Сохраняем результат
    output_path = r'e:\\posl\\data\\result.xlsx'
    df.to_excel(output_path, index=False)
    print(f"Результат сохранён в {output_path}")
    print(df.sample(10)) 

if __name__ == "__main__":
    main()
