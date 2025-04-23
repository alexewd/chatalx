from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time

# Путь к chromedriver
chrome_driver_path = "c:\\Users\\alexewd\\chromedriver\\chromedriver.exe"

# Настройка Selenium
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service)

# Базовый URL
base_url = "https://www.avito.ru/moskva/tovary_dlya_kompyutera/klaviatury_i_myshi-ASgBAgICAUTGB7xO?cd=1&q=ibm+model+m"
all_texts = []

# Открываем первую страницу
driver.get(base_url)
time.sleep(5)  # Ждём загрузки страницы
soup = BeautifulSoup(driver.page_source, "html.parser")

# Определяем последнюю страницу
pagination = soup.find_all("span", {"data-marker": "page-link"})
last_page = int(pagination[-1].text.strip()) if pagination else 1
print(f"Найдено страниц: {last_page}")

# Парсим все страницы
for page in range(1, last_page + 1):
    page_url = f"{base_url}&p={page}" if page > 1 else base_url
    driver.get(page_url)
    time.sleep(5)  # Ждём загрузки страницы
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # Извлекаем элементы с классом
    elements = soup.find_all(class_="index-root-gtkvj")
    texts = [element.get_text(strip=True) for element in elements]
    all_texts.extend(texts)
    print(f"Страница {page}: найдено {len(texts)} элементов")

# Закрываем браузер
driver.quit()

# Сохраняем результаты
df = pd.DataFrame(all_texts, columns=["Текст элементов"])
df.to_csv("avito_texts.csv", index=False, encoding="utf-8-sig")
df.to_excel("avito_texts.xlsx", index=False, engine="openpyxl")
print("Тексты сохранены в avito_texts.csv и avito_texts.xlsx")
print(df)