import pandas as pd

# Путь к файлу
file_path = 'f:/chatepc/chatalx/work/data/poem.txt'

# Чтение содержимого файла
with open(file_path, 'r', encoding='utf-8') as file:
    text = file.read()

# Преобразование текста в список строк
lines = text.split('\n')

# Преобразование списка строк в DataFrame с именованными столбцами
text_df = pd.DataFrame({'id': range(1, len(lines) + 1), 'text': lines})

# Пример использования text_df
print("DataFrame с строками текста:")
print(text_df.head())

# Преобразование текста в список слов
words = text.split()

# Преобразование списка слов в DataFrame с индексами
words_df = pd.DataFrame({'id': range(1, len(words) + 1), 'word': words})

# Пример использования words_df
print("\nDataFrame с словами текста:")
print(words_df.head())