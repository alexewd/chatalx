import pandas as pd
import json
import re
import os

# Функция для поиска получателя, даты, места, подписи и извлечения текста письма
def extract_letter_info(text):
    # Шаблоны для поиска
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
        "signature": signature,
        "text": text.strip()  # Полный текст письма
    }

# Функция для загрузки писем из JSON
def load_json_files(json_folder):
    letters = []
    for filename in os.listdir(json_folder):
        if filename.endswith('.json'):
            with open(os.path.join(json_folder, filename), 'r', encoding='utf-8') as file:
                data = json.load(file)
                content = data.get('content', '')
                # Разделяем текст на письма (если письма идут в одном блоке, можно уточнить деление)
                letters.extend(content.split("\n\n"))  # Пример разделения на письма
    return letters

# Функция для обработки всех писем
def process_letters(texts):
    return [extract_letter_info(text) for text in texts]

# Создание DataFrame из списка писем
def create_letters_dataframe(letters_info):
    df = pd.DataFrame(letters_info)
    # Преобразуем дату в формат datetime для удобства
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    return df

# Пример использования
json_folder ='e:/cleaned_json_letter'

# Загружаем тексты из JSON
texts_from_json = load_json_files(json_folder)

# Обрабатываем письма
letters_info = process_letters(texts_from_json)

# Преобразуем письма в DataFrame
letters_df = create_letters_dataframe(letters_info)

# Сохраняем результаты в файл
#letters_df.to_csv("letters_with_texts.csv", index=False, encoding='utf-8')
#letters_df.to_excel("letters_with_texts.xlsx", index=False, encoding='utf-8')

# Вывод первых строк таблицы
print(letters_df.head())

print("Столбцы DataFrame:", letters_df.columns)
print("Пример данных:")
print(letters_df.head())


# Пример навигации
# Найти все письма к Л. Толстому
tolstoy_letters = letters_df[letters_df['recipient'].str.contains("Л.? Толстой", na=False)]
print("\nПисьма к Льву Толстому:")
print(tolstoy_letters)

# Просмотр текста конкретного письма
if not tolstoy_letters.empty:
    print("\nТекст первого письма к Льву Толстому:")
    print(tolstoy_letters.iloc[0]['text'])

recipient_tolstoy_letters = letters_df[letters_df['recipient'].str.contains("Л.? Толстой", na=False)]
print(recipient_tolstoy_letters)

letters_1871 = letters_df[letters_df['date'].dt.year == 1871]
print(letters_1871)


specific_letter = letters_df[letters_df['id'] == 1]
print(specific_letter['text'].values[0])

# letters_df.sample(2)
