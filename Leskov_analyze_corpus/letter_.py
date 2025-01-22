import re
import pandas as pd
import json
from pathlib import Path

def extract_letter_info(text):
    """
    Извлекает информацию из текста письма: адресат, дата, место и подпись.
    """
    recipient_pattern = r"^([А-ЯЁ][а-яё]+(?: [А-ЯЁ]\. [А-ЯЁ][а-яё]+)?)"
    date_pattern = r"(\d{1,2} [а-яё]+ \d{4})"
    place_pattern = r"(?:, )([А-ЯЁ][а-яё]+)"
    signature_pattern = r"(Н\. Лесков)"

    recipient = re.search(recipient_pattern, text, re.MULTILINE)
    recipient = recipient.group(1) if recipient else None

    date = re.search(date_pattern, text)
    date = date.group(1) if date else None

    place = re.search(place_pattern, text)
    place = place.group(1) if place else None

    signature = re.search(signature_pattern, text)
    signature = signature.group(1) if signature else None

    return {
        "recipient": recipient,
        "date": date,
        "place": place,
        "text": text.strip(),
        "signature": signature,
    }

def process_letters_from_files(json_folder):
    """
    Обрабатывает все JSON-файлы в указанной папке и извлекает письма.
    Возвращает DataFrame с письмами.
    """
    letters = []
    for file_path in json_folder.glob("*.json"):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            for letter_text in data:
                letter_info = extract_letter_info(letter_text)
                letters.append(letter_info)
    return pd.DataFrame(letters)

def save_letters_to_csv(letters_df, output_path):
    """
    Сохраняет DataFrame с письмами в CSV-файл.
    """
    letters_df.to_csv(output_path, index=False, encoding="utf-8")

if __name__ == "__main__":
    # Укажите путь к папке с JSON-файлами
    json_folder = Path('e:/cleaned_json_letter')
    output_csv = "letters_processed.csv"

    # Обрабатываем письма и сохраняем результат
    letters_df = process_letters_from_files(json_folder)

    # Сохраняем в CSV
    save_letters_to_csv(letters_df, output_csv)

    # Выводим первые несколько строк DataFrame для проверки
    print(letters_df.head())

    # Пример анализа: письма за 1887 год
    if "date" in letters_df:
        letters_1887 = letters_df[letters_df["date"].str.contains("1887", na=False)]
        print("Письма за 1887 год:")
        print(letters_1887)

    # Пример: фильтрация по адресату
    specific_recipient = "С. Н. Шубинскому"
    specific_letters = letters_df[letters_df["recipient"] == specific_recipient]
    print(f"Письма к {specific_recipient}:")
    print(specific_letters)
