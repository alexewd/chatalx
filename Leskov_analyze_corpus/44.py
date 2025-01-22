import re
import pandas as pd
from pathlib import Path

def extract_letter_info_block(text_block):
    """
    Извлекает информацию из одного блока текста письма.
    """
    # Шаблоны для извлечения частей письма
    number_pattern = r"^(\d+)\n"
    recipient_pattern = r"^\d+\n(.*?)\n"
    date_place_pattern = r"\n(\d{1,2} [а-яё]+ \d{4} г\., [А-ЯЁа-яё ]+)\.\n"
    signature_pattern = r"\n(Ваш[^\n]*)$"
    
    # Извлечение данных
    number = re.search(number_pattern, text_block)
    number = number.group(1) if number else None

    recipient = re.search(recipient_pattern, text_block)
    recipient = recipient.group(1) if recipient else None

    date_place = re.search(date_place_pattern, text_block)
    date_place = date_place.group(1) if date_place else None
    date, place = (date_place.split(", ") if date_place else (None, None))

    signature = re.search(signature_pattern, text_block)
    signature = signature.group(1) if signature else None

    # Оставшийся текст — это текст письма
    text = re.sub(rf"{number_pattern}|{recipient_pattern}|{date_place_pattern}|{signature_pattern}", "", text_block).strip()

    return {
        "number": number,
        "recipient": recipient,
        "date": date,
        "place": place,
        "text": text,
        "signature": signature,
    }

def process_letters_from_text_file(file_path):
    """
    Обрабатывает текстовый файл с письмами и возвращает DataFrame.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Разделяем текст на блоки по номерам писем
    letters = re.split(r"(?<=\n)\d+\n", content)
    letters = [f"{i+1}\n{letters[i]}" for i in range(len(letters)) if letters[i].strip()]  # Восстанавливаем номера

    # Обрабатываем каждый блок
    extracted_data = [extract_letter_info_block(letter) for letter in letters]

    return pd.DataFrame(extracted_data)

# Пример использования
if __name__ == "__main__":
    # Укажите путь к текстовому файлу
    text_file = Path("e:/cleaned_json_letter/Лесков Николай. Том 11.txt")
    output_csv = "letters_processed.csv"

    # Обрабатываем текстовый файл
    letters_df = process_letters_from_text_file(text_file)

    # Сохраняем в CSV
    letters_df.to_csv(output_csv, index=False, encoding="utf-8")

    # Выводим результат
    print("Все письма:")
    print(letters_df)
    letters_df.sample(6)


