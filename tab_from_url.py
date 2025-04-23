import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL страницы с диапазонами IP-адресов
url = "https://lite.ip2location.com/russian-federation-ip-address-ranges?lang=ru"

# Получаем содержимое страницы
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Находим div с id 'ip-address_wrapper'
wrapper = soup.find('div', id='ip-address_wrapper')

# Проверяем, был ли найден div
if wrapper is None:
    print("Div с id 'ip-address_wrapper' не найден. Проверьте структуру HTML страницы.")
else:
    # Находим таблицу внутри этого div
    table = wrapper.find('table')

    # Проверяем, была ли найдена таблица
    if table is None:
        print("Таблица не найдена. Проверьте структуру HTML страницы.")
    else:
        # Извлекаем заголовки таблицы
        headers = [header.text.strip() for header in table.find_all('th')]

        # Извлекаем строки таблицы
        data = []
        for row in table.find_all('tr')[1:]:  # Пропускаем заголовок
            cols = row.find_all('td')
            if cols:
                data.append([col.text.strip() for col in cols])

        # Создаём DataFrame с нужными именами полей
        df = pd.DataFrame(data, columns=["Начальный IP-адрес", "Конечный IP-адрес", "Общее количество"])
        df.sample(n=10)
        # Указываем имя файла для сохранения
        csv_file = 'ip_ranges.csv'

        # Сохраняем DataFrame в CSV файл
        df.to_csv(csv_file, index=False, encoding='utf-8')

        print(f"Данные успешно сохранены в {csv_file}")
