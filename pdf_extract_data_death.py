import re
import pandas as pd
from PyPDF2 import PdfReader

# Функция для извлечения данных из текста
def extract_data(text):
    # Регулярное выражение для извлечения данных
    pattern = r'([А-Яа-яё]+\s[А-Яа-яё]+\s[А-Яа-яё]+),.*?f\s(\d{1,2}\s\w+\s\d{4}),\s(\d{1,2})\sл\.'
    matches = re.findall(pattern, text)
    return matches

# Чтение PDF файла
pdf_path = r'd:\pdf_read_py\rus_nekropol_2014.pdf'
reader = PdfReader(pdf_path)

# Извлечение текста из первых 50 страниц
text = ''
for i in range(min(50, len(reader.pages))):  # Обрабатываем максимум 50 страниц
    text += reader.pages[i].extract_text()

# Извлечение данных
data = extract_data(text)

# Создание DataFrame
df = pd.DataFrame(data, columns=['Фамилия Имя Отчество', 'Дата смерти', 'Количество лет'])

# Вывод результата
print(df)
