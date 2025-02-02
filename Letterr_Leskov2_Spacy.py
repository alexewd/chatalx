import spacy
import pandas as pd
import os

# Загрузка модели для русского языка
nlp = spacy.load("ru_core_news_sm")
nlp.max_length = 10000000
# Путь к директории с томами
directory_path = r'e:\cleaned_text_letter'

# Список для хранения имен собственных
names = []

# Проходим по всем файлам в директории
for filename in os.listdir(directory_path):
    if filename.endswith('.txt'):  # Проверяем, что файл имеет расширение .txt
        file_path = os.path.join(directory_path, filename)
        
        # Чтение содержимого файла
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        
        # Обработка текста с помощью spaCy
        doc = nlp(text)
        
        # Извлечение имен собственных
        for ent in doc.ents:
            if ent.label_ == "PER":  # Проверяем, что это имя человека
                names.append(ent.text)

# Удаляем дубликаты и сортируем имена
unique_names = sorted(set(names))

# Создание DataFrame
df_names = pd.DataFrame(unique_names, columns=['Names'])

# Вывод первых 5 строк DataFrame
print(df_names.head())

# Сохранение DataFrame в CSV файл (по желанию)
df_names.to_csv('unique_names_spacy.csv', index=False, encoding='utf-8')
