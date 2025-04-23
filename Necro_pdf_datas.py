from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import cv2
import re
import os

print(os.environ['PATH'])

# Путь к файлу
pdf_path = r'c:\bac_c\nekropol\1_a_b.pdf'  # Замени на имя твоего файла
pages = convert_from_path(pdf_path, 300, poppler_path=r'C:\poppler\Library\bin')  # Укажи свой путь
# Конвертируем PDF в изображения
# pages = convert_from_path(pdf_path, 300)

results = []

for i, page in enumerate(pages):
    img_path = f'page_{i}.png'
    page.save(img_path, 'PNG')
    
    # Предобработка изображения
    img = cv2.imread(img_path, 0)
    img = cv2.medianBlur(img, 5)  # Убираем шум
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    
    # OCR
    text = pytesseract.image_to_string(img, lang='rus')
    
    # Регулярные выражения
    # ФИО: "АБАЦИЕВ Михаил Николаевич"
    fio_pattern = r'[А-Я][а-я]+ [А-Я][а-я]+ [А-Я][а-я]+'
    # Даты: "(1890 (ненужное) - 1983, Париж)"
    dates_pattern = r'\(\d{4}.*?-\s*\d{4}'
    
    fios = re.findall(fio_pattern, text)
    dates = re.findall(dates_pattern, text)
    
    # Обрабатываем даты, чтобы вытащить только годы
    for fio, date in zip(fios, dates):
        # Извлекаем годы: "1890" и "1983"
        years = re.findall(r'\d{4}', date)
        if len(years) == 2:  # Убеждаемся, что нашли оба года
            birth_year, death_year = years
            results.append((fio, birth_year, death_year))
    
    os.remove(img_path)

# Вывод результатов
for fio, birth, death in results:
    print(f"ФИО: {fio}, Год рождения: {birth}, Год смерти: {death}")

# Сохранение в файл
with open('burials.txt', 'w', encoding='utf-8') as f:
    for fio, birth, death in results:
        f.write(f"ФИО: {fio}, Год рождения: {birth}, Год смерти: {death}\n")