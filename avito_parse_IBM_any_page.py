import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from requests.exceptions import HTTPError

# Базовый URL поиска (без параметра страницы)
base_url = "https://www.avito.ru/moskva/tovary_dlya_kompyutera/klaviatury_i_myshi-ASgBAgICAUTGB7xO?cd=1&q=ibm+model+m"

# Заголовки для имитации браузера
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Функция для получения HTML страницы с обработкой ошибок
def get_page_content(url):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except HTTPError as e:
        print(f"Ошибка при запросе {url}: {e}")
        return None

# Определяем последнюю страницу
def get_last_page(soup):
    if not soup:
        return 1
    pagination = soup.find("div", {"data-marker": "pagination-button"})
    if pagination:
        buttons = pagination.find_all("span", {"data-marker": "page-link"})
        if buttons:
            last_button = buttons[-1].text.strip()
            try:
                return int(last_button)
            except ValueError:
                return 1
    return 1

# Список для хранения всех текстов
all_texts = []

# Парсим первую страницу, чтобы определить количество страниц
first_page_soup = get_page_content(base_url)
if first_page_soup:
    last_page = get_last_page(first_page_soup)
    print(f"Найдено страниц: {last_page}")
else:
    last_page = 1
    print("Не удалось загрузить первую страницу, обработаю только её")

# Парсим все страницы
for page in range(1, last_page + 1):
    page_url = f"{base_url}&p={page}" if page > 1 else base_url
    print(f"Обрабатываю страницу {page} из {last_page}: {page_url}")
    
    soup = get_page_content(page_url)
    if soup:
        # Находим все элементы с классом (заголовки объявлений)
        class_name = "index-root-gtkvj"
        elements = soup.find_all(class_=class_name)
        
        # Извлекаем текст
        texts = [element.get_text(strip=True) for element in elements]
        all_texts.extend(texts)
        print(f"Найдено {len(texts)} элементов на странице {page}")
    
    # Задержка 5 секунд между запросами
    time.sleep(5)

# Создаем DataFrame
df = pd.DataFrame(all_texts, columns=["Текст элементов"])

# Сохраняем в CSV-файл
df.to_csv("avito_texts.csv", index=False, encoding="utf-8-sig")
print("Тексты элементов успешно сохранены в avito_texts.csv")

# Сохраняем в Excel-файл
df.to_excel("avito_texts.xlsx", index=False, engine="openpyxl")
print("Тексты элементов успешно сохранены в avito_texts.xlsx")
print(df)