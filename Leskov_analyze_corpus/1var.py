import pandas as pd
import json
import re
import os

# Функция для извлечения информации о письмах
def extract_letter_info_with_text(text):
    # Шаблоны для поиска метаинформации
    recipient_pattern = r"(к [А-ЯЁ][а-яё]+(?: [А-ЯЁ][а-яё]+)*)"
    date_pattern = r"(\d{1,2} [а-я]+ \d{4})"
    place_pattern = r"(?:в )([А-ЯЁ][а-яё]+)"
    signature_pattern = r"(Н\.? Лесков)"

    # Найдем метаинформацию
    recipient = re.search(recipient_pattern, text)
    recipient = recipient.group(1) if recipient else None

    date = re.search(date_pattern, text)
    date = date.group(1) if date else None

    place = re.search(place_pattern, text)
    place = place.group(1) if place else None

    signature = re.search(signature_pattern, text)
    signature = signature.group(1) if signature else None

    # Возвращаем метаинформацию и текст
    return {
        "recipient": recipient,
        "date": date,
        "place": place,
        "text": text.strip()
    }

# Функция для загрузки текстов из JSON
def load_json_files_with_texts(json_folder):
    texts = []
    for filename in os.listdir(json_folder):
        if filename.endswith('.json'):
            with open(os.path.join(json_folder, filename), 'r', encoding='utf-8') as file:
                data = json.load(file)
                texts.append(data.get('content', ''))
    return texts

# Функция для обработки всех писем и создания DataFrame
def process_letters_with_texts(json_folder):
    texts = load_json_files_with_texts(json_folder)
    letters_info = [extract_letter_info_with_text(text) for text in texts]
    df = pd.DataFrame(letters_info)
    # Преобразуем дату в формат datetime
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['id'] = range(1, len(df) + 1)  # Уникальный ID для каждого письма
    return df

# Пример использования
json_folder = 'e:/cleaned_json_letter'

# Создаем DataFrame с письмами
letters_df = process_letters_with_texts(json_folder)

# Сохраняем DataFrame в файл CSV для удобства
letters_df.to_csv('letters_full.csv', index=False, encoding='utf-8')

# Вывод первых строк для проверки
print(letters_df.head())

# Пример навигации
# Найти все письма к Л. Толстому
recipient_tolstoy_letters = letters_df[letters_df['recipient'].str.contains("Л.? Толстой", na=False)]
print("\nПисьма к Льву Толстому:")
print(recipient_tolstoy_letters)

# Найти текст конкретного письма
specific_letter = letters_df[letters_df['id'] == 1]
print("\nТекст первого письма:")
print(specific_letter['text'].values[0])
