import pdfplumber
import pandas as pd

# Путь к PDF файлу
pdf_path = 'D:/woodbridge-fmlog.pdf'

# Список для хранения данных
data = []

# Открываем PDF файл
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        # Извлекаем таблицу с каждой страницы
        table = page.extract_table()
        if table:
            # Обрабатываем строки таблицы
            for row in table[1:]:
                # Проверяем, если строка содержит многострочные данные
                if len(row) > 13:
                    # Объединяем многострочные данные в последний столбец, фильтруя None
                    information = ' '.join(filter(None, row[13:]))
                    row = row[:13] + [information]
                data.append(row)

# Создаем DataFrame из собранных данных
columns = ['Freq', 'Calls', 'City of License', 'State', 'Country', 'Date', 'Time', 'Prop', 'Miles', 'ERP', 'HD', 'RDS', 'Audio', 'Information']
df = pd.DataFrame(data, columns=columns)

# Сохраняем DataFrame в CSV файл
csv_path = 'D:/woodbridge-fmlog.csv'
df.to_csv(csv_path, index=False)

# Сохраняем DataFrame в Excel файл
excel_path = 'D:/woodbridge-fmlog.xlsx'
df.to_excel(excel_path, index=False, engine='openpyxl')

print(f"Данные успешно сохранены в {csv_path} и {excel_path}")
