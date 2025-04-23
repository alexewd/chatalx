
# https://www.avito.ru/moskva/tovary_dlya_kompyutera/klaviatury_i_myshi-ASgBAgICAUTGB7xO?cd=1&q=ibm+model+m
# https://www.avito.ru/moskva/tovary_dlya_kompyutera/klaviatury_i_myshi-ASgBAgICAUTGB7xO?cd=1&p=2&q=ibm+model+m 
# page 2 опять запускать код?

import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL страницы
url = "https://www.avito.ru/moskva/tovary_dlya_kompyutera/klaviatury_i_myshi-ASgBAgICAUTGB7xO?cd=1&q=ibm+model+m"

# Заголовки для имитации браузера
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Получаем содержимое страницы
response = requests.get(url, headers=headers)
response.raise_for_status()  # Проверка на ошибки при запросе

# Парсим HTML
soup = BeautifulSoup(response.text, "html.parser")

# Находим все элементы с указанным классом
class_name = "index-root-gtkvj"
elements = soup.find_all(class_=class_name)

# Извлекаем текст из каждого элемента
texts = [element.get_text(strip=True) for element in elements]

# Создаем DataFrame с одним столбцом
df = pd.DataFrame(texts, columns=["Текст элементов"])

# Сохраняем в CSV-файл
df.to_csv("avito_texts_ibm.csv", index=False, encoding="utf-8-sig")
print("Тексты элементов успешно сохранены в avito_texts.csv")

# Сохраняем в Excel-файл
df.to_excel("avito_texts_ibm.xlsx", index=False, engine="openpyxl")
print("Тексты элементов успешно сохранены в avito_texts.xlsx")
print(df)