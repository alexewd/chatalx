# # import requests
# # import pandas as pd
# # from bs4 import BeautifulSoup

# # # URL страницы
# # url = "https://aa-online.ru/raspisanie/"

# # # Получаем содержимое страницы
# # response = requests.get(url)
# # soup = BeautifulSoup(response.content, 'html.parser')

# # # Находим таблицу по ID
# # table = soup.find('table', id='tablepress-8')

# # # Используем pandas для чтения таблицы
# # df = pd.read_html(str(table))[0]

# # # Сохраняем в CSV
# # df.to_csv('table.csv', index=False, encoding='utf-8-sig', sep=',',header=True)

# # print("Таблица сохранена в table.csv")

# # print(df)
# import requests
# from bs4 import BeautifulSoup
# import pandas as pd

# # URL страницы
# url = "https://aa-online.ru/raspisanie/"

# # Заголовки для имитации браузера (иногда сайты блокируют запросы без них)
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
# }

# # Получаем содержимое страницы
# response = requests.get(url, headers=headers)
# response.raise_for_status()  # Проверка на ошибки при запросе

# # Парсим HTML
# soup = BeautifulSoup(response.text, "html.parser")

# # Находим таблицу по ID
# table = soup.find("table", {"id": "tablepress-8"})

# # Извлекаем заголовки таблицы
# headers = []
# for th in table.find("thead").find_all("th"):
#     headers.append(th.text.strip())

# # Извлекаем данные из строк таблицы
# rows = []
# for tr in table.find("tbody").find_all("tr"):
#     row = [td.text.strip() for td in tr.find_all("td")]
#     rows.append(row)

# # Создаем DataFrame с помощью pandas
# df = pd.DataFrame(rows, columns=headers)

# # Сохраняем в CSV-файл
# df.to_csv("raspisanije2.csv", index=False, encoding="utf-8-sig")
# print("Таблица успешно сохранена в raspisanije.csv")
# print(df)

import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL страницы
url = "https://aa-online.ru/raspisanie/"

# Заголовки для имитации браузера
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Получаем содержимое страницы
response = requests.get(url, headers=headers)
response.raise_for_status()  # Проверка на ошибки при запросе

# Парсим HTML
soup = BeautifulSoup(response.text, "html.parser")

# Находим таблицу по ID
table = soup.find("table", {"id": "tablepress-8"})

# Извлекаем заголовки таблицы
headers = []
for th in table.find("thead").find_all("th"):
    headers.append(th.text.strip())

# Извлекаем данные из строк таблицы
rows = []
for tr in table.find("tbody").find_all("tr"):
    row = [td.text.strip() for td in tr.find_all("td")]
    rows.append(row)

# Создаем DataFrame с помощью pandas
df = pd.DataFrame(rows, columns=headers)

# Сохраняем в CSV-файл
df.to_csv("raspisanije.csv", index=False, encoding="utf-8-sig")
print("Таблица успешно сохранена в raspisanije.csv")

# Сохраняем в Excel-файл
df.to_excel("raspisanije.xlsx", index=False, engine="openpyxl")
print("Таблица успешно сохранена в raspisanije.xlsx")