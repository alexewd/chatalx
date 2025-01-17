import collections
import pandas as pd

file_path = "f:/chatepc/chatalx/work/data/obriv.txt"  # Укажите путь к вашему файлу

# Чтение текста из файла
with open(file_path, 'r', encoding='utf-8') as file:
    text = file.read()  # Используем read() для того, чтобы получить весь текст как одну строку

# Приводим текст к нижнему регистру
text = text.lower()

# Считаем частоту букв
frequency = collections.Counter(letter for letter in text if letter.isalpha())

# Убираем пробелы и символы, не являющиеся буквами
total_letters = sum(frequency[letter] for letter in frequency)

# """ Буквы е и ё, а также ь, ъ кодируются обычно одинаково, поэтому в таблице они не различаются.
# Как следует из таблицы, наиболее частая буква русского языка — о.
# Ее относительная частота, равная 0,090, означает, что на 1000 букв русского текста приходится в среднем 90 букв о. 
# В таком же смысле понимаются относительные частоты и остальных букв.
# В таблице не указан еще один “символ” — промежуток между словами (пробел). Его относительная частота наибольшая и равна 0,175. """
# Таблица частот русского языка

russian_frequency = {
    "а": 0.062, "б": 0.014, "в": 0.038, "г": 0.013, "д": 0.025,
    "е": 0.072, "ж": 0.007, "з": 0.016, "и": 0.062, "й": 0.010,
    "к": 0.028, "л": 0.035, "м": 0.026, "н": 0.053, "о": 0.090,
    "п": 0.023, "р": 0.040, "с": 0.045, "т": 0.053, "у": 0.021,
    "ф": 0.002, "х": 0.009, "ц": 0.004, "ч": 0.012, "ш": 0.006,
    "щ": 0.003, "ъ": 0.000, "ы": 0.019, "ь": 0.014, "э": 0.003,
    "ю": 0.006, "я": 0.018
}

# Подготавливаем данные для датафрейма
data = []
for letter, count in frequency.items():
    # Рассчитываем относительную частоту в тексте
    relative_frequency = count / total_letters
    relative_frequency_percent = round(relative_frequency * 100, 3)

    # Сравниваем с таблицей частот
    expected_frequency = russian_frequency.get(letter, 0)
    ratio = round(relative_frequency / expected_frequency, 2) if expected_frequency > 0 else None

    # Добавляем данные в список
    data.append({
        "Буква": letter,
        "Частота в тексте (%)": relative_frequency_percent,
        "Ожидаемая частота (%)": round(expected_frequency * 100, 3),
        "Соотношение к ожиданию": ratio
    })

# Создаем датафрейм
df = pd.DataFrame(data)

# Сортируем датафрейм по частоте в тексте
df = df.sort_values(by="Частота в тексте (%)", ascending=False)

# Выводим датафрейм
print(df)

# (Опционально) Сохранение датафрейма в CSV
output_path = "letter_frequency.csv"
df.to_csv(output_path, index=False, encoding="utf-8")
print(f"Результаты сохранены в файл {output_path}")
