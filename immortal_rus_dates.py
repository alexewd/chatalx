from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import cv2
import re
import os
from tqdm import tqdm
import logging
import pandas as pd  # Добавляем pandas

# Настройка логирования
logging.basicConfig(
    filename='pdf_processing.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Путь к файлу
pdf_path = 'your_file.pdf'  # Замени на имя твоего файла

# Конвертируем PDF в изображения
logging.info("Начало конвертации PDF в изображения")
pages = convert_from_path(pdf_path, 300, poppler_path=r'C:\poppler\Library\bin')  # Укажи свой путь
logging.info(f"Конвертировано {len(pages)} страниц")

results = []

# Открываем файл для промежуточной записи
with open('burials.txt', 'w', encoding='utf-8') as f:
    for i, page in tqdm(enumerate(pages), total=len(pages), desc="Обработка страниц"):
        img_path = f'page_{i}.png'
        page.save(img_path, 'PNG')
        
        # Предобработка изображения
        img = cv2.imread(img_path, 0)
        img = cv2.medianBlur(img, 5)
        img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        
        # OCR
        logging.info(f"Запуск OCR для страницы {i+1}")
        text = pytesseract.image_to_string(img, lang='rus')
        
        # Регулярные выражения
        fio_pattern = r'[А-Я][а-я]+ [А-Я][а-я]+ [А-Я][а-я]+'
        dates_pattern = r'\(\d{4}.*?-\s*\d{4}'
        
        fios = re.findall(fio_pattern, text)
        dates = re.findall(dates_pattern, text)
        
        logging.info(f"Страница {i+1}: найдено {len(fios)} ФИО и {len(dates)} дат")
        
        for fio, date in zip(fios, dates):
            years = re.findall(r'\d{4}', date)
            if len(years) == 2:
                birth_year, death_year = years
                result = (fio, birth_year, death_year)
                results.append(result)
                f.write(f"ФИО: {fio}, Год рождения: {birth_year}, Год смерти: {death_year}\n")
                f.flush()
                logging.info(f"Добавлено: {fio}, {birth_year}-{death_year}")
        
        os.remove(img_path)

# Вывод результатов в консоль
for fio, birth, death in results:
    print(f"ФИО: {fio}, Год рождения: {birth}, Год смерти: {death}")

# Создание таблицы pandas
df = pd.DataFrame(results, columns=['ФИО', 'Год рождения', 'Год смерти'])

# Сохранение в CSV
df.to_csv('burials.csv', index=False, encoding='utf-8')
logging.info("Результаты сохранены в burials.csv")

# Сохранение в Excel (опционально)
df.to_excel('burials.xlsx', index=False)
logging.info("Результаты сохранены в burials.xlsx")

logging.info("Обработка завершена")