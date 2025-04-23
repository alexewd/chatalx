from pdf2image import convert_from_path
import logging

# Настройка логирования
logging.basicConfig(
    filename='pdf_processing.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)

# Путь к файлу
pdf_path = r'c:\bac_c\nekropol\1_a_b.pdf'
logging.info(f"Проверка пути к файлу: {pdf_path}")

# Тестовая конвертация одной страницы
logging.info("Тест: конвертация первой страницы")
try:
    pages = convert_from_path(pdf_path, 300, poppler_path=r'C:\poppler\Library\bin', first_page=1, last_page=1)
    logging.info(f"Успешно конвертирована 1 страница, всего страниц: {len(pages)}")
    pages[0].save('test_page_1.png', 'PNG')
    logging.info("Первая страница сохранена как test_page_1.png")
except Exception as e:
    logging.error(f"Ошибка при конвертации: {str(e)}")
""" Запусти этот код.
Если он выполнится быстро и создаст test_page_1.png, значит, проблема в объёме данных.
Если зависнет или выдаст ошибку, проблема в poppler или файле.
2. Уменьшим нагрузку
Если тест прошёл успешно, вернёмся к основному коду, но:
Уменьшим DPI (с 300 до 200 или 150).
Ограничим количество страниц для конвертации.
Обновлённый код с ограничением
python
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import cv2
import re
import os
from tqdm import tqdm
import logging
import pandas as pd

# Настройка логирования
logging.basicConfig(
    filename='pdf_processing.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)

# Путь к файлу
pdf_path = r'c:\bac_c\nekropol\1_a_b.pdf'
logging.info(f"Проверка пути к файлу: {pdf_path}")
if not os.path.exists(pdf_path):
    logging.error(f"Файл {pdf_path} не найден!")
    raise FileNotFoundError(f"Файл {pdf_path} не найден!")

# Конвертируем PDF в изображения (ограничим первые 10 страниц)
logging.info("Начало конвертации PDF в изображения")
try:
    pages = convert_from_path(pdf_path, 200, poppler_path=r'C:\poppler\Library\bin', first_page=1, last_page=10)
    logging.info(f"Конвертировано {len(pages)} страниц")
except Exception as e:
    logging.error(f"Ошибка при конвертации PDF: {str(e)}")
    raise

results = []

# Проверка на первых 20 записях
max_entries = 20
logging.info("Запуск проверки на первых 20 записях...")
print("Запуск проверки на первых 20 записях...")
with open('burials_preview.txt', 'w', encoding='utf-8') as f_preview:
    for i, page in tqdm(enumerate(pages), total=len(pages), desc="Проверка страниц"):
        if len(results) >= max_entries:
            break
        
        img_path = f'page_{i}.png'
        logging.info(f"Сохранение страницы {i+1} как {img_path}")
        page.save(img_path, 'PNG')
        
        img = cv2.imread(img_path, 0)
        img = cv2.medianBlur(img, 5)
        img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        
        logging.info(f"Запуск OCR для страницы {i+1}")
        text = pytesseract.image_to_string(img, lang='rus')
        logging.info(f"Текст с OCR (страница {i+1}): {text[:100]}...")  # Первые 100 символов для проверки
        
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
                f_preview.write(f"ФИО: {fio}, Год рождения: {birth_year}, Год смерти: {death_year}\n")
                f_preview.flush()
                logging.info(f"Добавлено: {fio}, {birth_year}-{death_year}")
                if len(results) >= max_entries:
                    break
        
        os.remove(img_path)

# Вывод результатов проверки
print("\nРезультаты проверки первых 20 записей:")
for fio, birth, death in results:
    print(f"ФИО: {fio}, Год рождения: {birth}, Год смерти: {death}")

df_preview = pd.DataFrame(results, columns=['ФИО', 'Год рождения', 'Год смерти'])
df_preview.to_csv('burials_preview.csv', index=False, encoding='utf-8')
logging.info("Проверка сохранена в burials_preview.csv")

logging.info("Обработка завершена") """