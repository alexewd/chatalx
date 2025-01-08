import pandas as pd

# Путь к файлу
file_path = 'f:/chatepc/chatalx/work/data/poem.txt'

# Чтение содержимого файла
with open(file_path, 'r', encoding='utf-8') as file:
    text = file.read()

# Преобразование текста в Series
text_series = pd.Series([text])

# Преобразование текста в список строк
lines = text.split('\n')

# Преобразование списка строк в DataFrame
text_df = pd.DataFrame(lines, columns=['line'])

# Пример использования text_series и text_df
print(text_series.head())
print(text_df.head())