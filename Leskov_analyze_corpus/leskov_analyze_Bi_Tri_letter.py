import pandas as pd
import json
import re
import os

# Функция для поиска получателя, даты, места и подписи
def extract_letter_info(text):
    # Шаблоны для поиска получателя, даты, места и подписи
    recipient_pattern = r"(к [А-ЯЁ][а-яё]+(?: [А-ЯЁ][а-яё]+)*)"
    date_pattern = r"(\d{1,2} [а-я]+ \d{4})"
    place_pattern = r"(?:в )([А-ЯЁ][а-яё]+)"
    signature_pattern = r"(Н\.? Лесков)"

    # Найдем получателя
    recipient = re.search(recipient_pattern, text)
    recipient = recipient.group(1) if recipient else None

    # Найдем дату
    date = re.search(date_pattern, text)
    date = date.group(1) if date else None

    # Найдем место
    place = re.search(place_pattern, text)
    place = place.group(1) if place else None

    # Найдем подпись
    signature = re.search(signature_pattern, text)
    signature = signature.group(1) if signature else None

    return {
        "recipient": recipient,
        "date": date,
        "place": place,
        "signature": signature
    }

# Функция для обработки всех писем в файле
def process_letters(texts):
    letters_info = []
    
    for text in texts:
        # Применяем функцию извлечения для каждого текста
        letter_info = extract_letter_info(text)
        letters_info.append(letter_info)
    
    return letters_info

# Функция для загрузки текстов из JSON
def load_json_files(json_folder):
    texts = []
    for filename in os.listdir(json_folder):
        if filename.endswith('.json'):
            with open(os.path.join(json_folder, filename), 'r', encoding='utf-8') as file:
                data = json.load(file)
                texts.append(data.get('content', ''))
    return texts

# Преобразуем извлеченную информацию о письмах в DataFrame
def create_letters_dataframe(letters_info):
    df = pd.DataFrame(letters_info)
    # Преобразуем дату в формат datetime для удобства
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    return df

# Пример использования
json_folder = 'e:/cleaned_json'

# Загружаем тексты из JSON (например, из 10 и 11 томов)
texts_from_json = load_json_files(json_folder)

# Обрабатываем письма
letters_info = process_letters(texts_from_json)

# Преобразуем информацию о письмах в DataFrame
letters_df = create_letters_dataframe(letters_info)

# Сохраняем информацию о письмах в JSON файл
with open('letters_info.json', 'w', encoding='utf-8') as json_file:
    json.dump(letters_info, json_file, ensure_ascii=False, indent=4)

# Выводим несколько примеров для проверки
print(letters_df.head())

# Пример навигации
# 1. Найти все письма к П. К. Щебальскому
recipient_letters = letters_df[letters_df['recipient'].str.contains("П. К. Щебальскому", na=False)]

# 2. Найти все письма, написанные в 1871 году
letters_1871 = letters_df[letters_df['date'].dt.year == 1871]

# 3. Сортировка по дате
letters_sorted = letters_df.sort_values(by='date')

# Вывод результатов
print("Письма к П. К. Щебальскому:")
print(recipient_letters)

print("\nПисьма из 1871 года:")
print(letters_1871)

print("\nПисьма, отсортированные по дате:")
print(letters_sorted)

# 4. Пример фильтрации по Льву Толстому
recipient_tolstoy_letters = letters_df[letters_df['recipient'].str.contains("Л.? Толстой", na=False)]
print("\nПисьма к Льву Толстому:")
print(recipient_tolstoy_letters)
