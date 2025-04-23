# Импортируем необходимые библиотеки
import json
import pandas as pd
path = 'f:\\chatepc\\chatalx\\data\\freelancer.json'


# Открываем JSON файл с указанием кодировки
with open(path, 'r', encoding='utf-8') as file:
    # Загружаем данные из файла
    data = json.load(file)

# Проверяем, является ли data списком
if isinstance(data, list):
    # Преобразуем данные в DataFrame
    df = pd.DataFrame(data)
else:
    # Если это не список, используем json_normalize
    df = pd.json_normalize(data)

# Выводим DataFrame
print(df)

# Дополнительно: сохраняем DataFrame в CSV файл
df.to_csv('freelancer.csv', index=False)
