import re
import pandas as pd
from PyPDF2 import PdfReader
from tqdm import tqdm  # Импортируем tqdm для прогресс-бара

def extract_data(text):
    # Регулярное выражение для извлечения данных
    pattern = r'([А-ЯЁ][а-яё]+(?:[-][А-ЯЁ][а-яё]+)?\s[А-ЯЁ][а-яё]+\s[А-ЯЁ][а-яё]+)(.*?)(?=([А-ЯЁ][а-яё]+(?:[-][А-ЯЁ][а-яё]+)?\s[А-ЯЁ][а-яё]+\s[А-ЯЁ][а-яё]+)|$)'
    matches = re.findall(pattern, text, re.DOTALL)

    cleaned_matches = []
    for match in matches:
        fio = match[0].strip()  # ФИО
        description = match[1].strip()  # Описание
        # Ищем дату и количество лет в описании
        date_pattern = r'f\s(\d{1,2}\s\w+\s\d{4})'
        age_pattern = r'(\d{1,2})\s(л|г)\.'
        
        date_match = re.search(date_pattern, description)
        age_match = re.search(age_pattern, description)

        if date_match:
            date = date_match.group(1)
        else:
            date = ''

        if age_match:
            age = age_match.group(1)
        else:
            age = '-'

        cleaned_matches.append((fio, date, age, description))  # Добавляем описание

    return cleaned_matches

# Чтение PDF файла
pdf_path = r'd:\pdf_read_py\rus_nekropol_2014.pdf'
reader = PdfReader(pdf_path)

# Извлечение текста из страниц, начиная с 14-й
text = ''
for i in tqdm(range(13, len(reader.pages)), desc="Обработка страниц"):  # Начинаем с 13, так как индексация начинается с 0
    text += reader.pages[i].extract_text()

# Извлечение данных
data = extract_data(text)

# Создание DataFrame
df = pd.DataFrame(data, columns=['Фамилия Имя Отчество', 'Дата смерти', 'Количество лет', 'Описание'])

# Сохранение DataFrame в CSV файл
csv_path = r'd:\pdf_read_py\rus_nekropol_2014.csv'
df.to_csv(csv_path, index=False, encoding='utf-8-sig')  # Сохраняем в CSV без индексов

# Сохранение DataFrame в Excel файл
excel_path = r'd:\pdf_read_py\rus_nekropol_2014.xlsx'
df.to_excel(excel_path, index=False, engine='openpyxl')  # Сохраняем в Excel без индексов

# Вывод 20 случайных записей
print(df.sample(20))

# Вывод результата
print(f"Данные успешно сохранены в {csv_path} и {excel_path}")
