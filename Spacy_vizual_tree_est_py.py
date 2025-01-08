import re
import spacy
import numpy as np
from spacy import displacy

# Загрузка модели spacy для русского языка
nlp = spacy.load("ru_core_news_sm")

# Чтение содержимого файла
file_path = "f:/chatepc/chatalx/work/data/Гробовщик.txt"
with open(file_path, 'r', encoding='utf-8') as file:
    text_data = file.read()

# Очистка текста
def clean_text(text):
    text = text.lower()  # Приводим к нижнему регистру
    text = re.sub(r"[^а-яё\s]", " ", text)  # Удаляем всё, кроме кириллических букв и пробелов
    text = re.sub(r"\s+", " ", text)  # Удаляем лишние пробелы
    text = text.strip()  # Убираем пробелы в начале и конце строки
    return text

# Обработка текста с помощью spacy
doc = nlp(text_data)

# Разбиение текста на предложения
sentences = list(doc.sents)

# Очистка каждого предложения
cleaned_sentences = [clean_text(sentence.text) for sentence in sentences]

# Удаление пустых предложений
cleaned_sentences = [sentence for sentence in cleaned_sentences if len(sentence) > 0]


# Извлечение именованных сущностей
proper_nouns = [ent.text for ent in doc.ents if ent.label_ == "PER"]

# Вывод имен собственных
print("Имена собственные (русские):")
for name in proper_nouns:
    print(name)
# for token in doc:
#     print(f"{token.text} - {token.pos_}")

# Визуализация синтаксического дерева
# displacy.render(doc, style='dep', jupyter=True)