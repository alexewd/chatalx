import re
import pandas as pd
from PyPDF2 import PdfReader
from tqdm import tqdm  # Импортируем tqdm для прогресс-бара

# Функция для извлечения данных из текста
def extract_data(text):
    # Регулярное выражение для извлечения данных
    pattern = r'([А-ЯЁ][а-яё]+(?:[-][А-ЯЁ][а-яё]+)?\s[А-ЯЁ][а-яё]+\s[А-ЯЁ][а-яё]+),.*?f\s(\d{1,2}\s\w+\s\d{4})(?:,\s(\d{1,2})\s(л|г)\.)?'
    matches = re.findall(pattern, text)

    cleaned_matches = []
    for match in matches:
        # Если количество лет указано, добавляем его, иначе ставим прочерк
        if match[2]:  # Если количество лет указано
            cleaned_matches.append((match[0], match[1], match[2]))  # Сохраняем ФИО, дату и количество лет
        else:  # Если количество лет не указано
            cleaned_matches.append((match[0], match[1], '-'))  # Сохраняем ФИО, дату и прочерк

    return cleaned_matches

# Чтение PDF файла
pdf_path = r'd:\pdf_read_py\rus_nekropol_2014.pdf'
reader = PdfReader(pdf_path)

# Извлечение текста из всех страниц с прогресс-баром
text = ''
for i in tqdm(range(len(reader.pages)), desc="Обработка страниц"):
    text += reader.pages[i].extract_text()

# Извлечение данных
data = extract_data(text)

# Создание DataFrame
df = pd.DataFrame(data, columns=['Фамилия Имя Отчество', 'Дата смерти', 'Количество лет'])

# Сохранение DataFrame в CSV файл
csv_path = r'd:\pdf_read_py\rus_nekropol_2014.csv'
df.to_csv(csv_path, index=False, encoding='utf-8-sig')  # Сохраняем в CSV без индексов

# Вывод результата
print(df)

# Преобразование столбца "Количество лет" в числовой формат
df['Количество лет'] = pd.to_numeric(df['Количество лет'], errors='coerce')

# Статистика по количеству лет
age_groups = {
    'Меньше 18': df[df['Количество лет'] < 18],
    'От 18 до 40': df[(df['Количество лет'] >= 18) & (df['Количество лет'] < 40)],
    'От 40 до 60': df[(df['Количество лет'] >= 40) & (df['Количество лет'] < 60)],
    '60 и выше': df[df['Количество лет'] >= 60],
    'От 65 до 70': df[(df['Количество лет'] >= 65) & (df['Количество лет'] < 70)],
    'Больше 70': df[df['Количество лет'] > 70]
}

# Подсчет количества и процентов
total_count = len(df)
statistics = {}

for group, group_df in age_groups.items():
    count = len(group_df)
    percentage = (count / total_count * 100) if total_count > 0 else 0
    statistics[group] = {'Количество': count, 'Процент': percentage}

# Вывод статистики
print("Статистика по количеству лет:")
for group, stats in statistics.items():
    print(f"{group}: {stats['Количество']} человек, {stats['Процент']:.2f}%")
