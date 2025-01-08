import pandas as pd

# Путь к файлу
file_path = 'f:/chatepc/chatalx/work/data/poem.txt'

# Чтение содержимого файла построчно
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Создание DataFrame с строками и индексами
text_df = pd.DataFrame({'id': range(1, len(lines) + 1), 'text': [line.strip() for line in lines]})

# Пример использования DataFrame с строками
print("DataFrame с строками текста:")
print(text_df.head())

# Преобразование текста в список слов
words = ' '.join([line.strip() for line in lines]).split()

# Преобразование списка слов в DataFrame с индексами
words_df = pd.DataFrame({'id': range(1, len(words) + 1), 'word': words})

# Пример использования DataFrame с словами
print("\nDataFrame с словами текста:")
print(words_df.head())