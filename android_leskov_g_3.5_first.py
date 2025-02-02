import pandas as pd
from pathlib import Path

# Создаем пустой список для хранения предложений
sentences = []

# Путь к папке с текстовыми файлами
folder_path = Path("e:/cleaned_text")

# Читаем каждый файл и добавляем предложения в список
for file_path in folder_path.glob("*.txt"):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
        # Добавляем предложения в список
        sentences.extend(text.split(". "))

# Создаем датафрейм pandas
df = pd.DataFrame(sentences, columns=["Sentences"])

# Выводим первые строки датафрейма
print(df.head())
df.shape
print(df.sample(30))
print(df.tail(30))

search_phrase = "юная римская патрицианка"

# Найти все предложения, содержащие словосочетание
matching_sentences = df[df["Sentences"].str.contains(search_phrase, case=False)]

# Вывести найденные предложения
print(matching_sentences)
print(df["Sentences"][26988])
