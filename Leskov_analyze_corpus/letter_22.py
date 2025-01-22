import re
import pandas as pd
import json
from pathlib import Path

def extract_letter_info(text):
    """
    Извлекает информацию из текста письма: адресат, дата, место и подпись.
    """
    recipient_pattern = r"^([А-ЯЁ][а-яё]+(?: [А-ЯЁ]\. [А-ЯЁ][а-яё]+)?)"
    date_pattern = r"(\d{1,2} [а-яё]+ \d{4} г\.)"
    place_pattern = r", ([А-ЯЁ][а-яё]+)\."
    signature_pattern = r"(Ваш Н\. Лесков)"

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
    """
    letters = []
    for file_path in json_folder.glob("*.json"):
        print(f"Processing file: {file_path}")
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

    # Выводим анализ
    print("Все письма:")
    print(letters_df)

    # Пример фильтрации: письма за 1887 год
    letters_df["date"] = pd.to_datetime(letters_df["date"], format="%d %B %Y г.", errors="coerce")
    letters_1887 = letters_df[letters_df["date"].dt.year == 1887]
    print("\nПисьма за 1887 год:")
    print(letters_1887)

    # Пример: письма к С. Н. Шубинскому
    shubinsky_letters = letters_df[letters_df["recipient"] == "С. Н. Шубинскому"]
    print("\nПисьма к С. Н. Шубинскому:")
    print(shubinsky_letters)
