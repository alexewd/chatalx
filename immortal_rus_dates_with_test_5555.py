from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import cv2
import re
import os
from tqdm import tqdm
import logging
import pandas as pd

# Указываем путь к tesseract
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# tessdata_dir_config = r'--tessdata-dir C:\Program Files\Tesseract-OCR\tessdata'

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

# Обработка с прогресс-баром
print("Запуск обработки...")
with open('burials.txt', 'w', encoding='utf-8') as f:
    for i, page in tqdm(enumerate(pages), total=len(pages), desc="Обработка страниц"):
        img_path = f'page_{i}.png'
        logging.info(f"Сохранение страницы {i+1} как {img_path}")
        page.save(img_path, 'PNG')
        
        img = cv2.imread(img_path, 0)
        img = cv2.medianBlur(img, 5)
        img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        
        logging.info(f"Запуск OCR для страницы {i+1}")
        text = pytesseract.image_to_string(img, lang='rus')
        logging.info(f"Текст с OCR (страница {i+1}): {text[:200]}...")
        
        fio_pattern = r'^[А-Я]{4,}'
        years_pattern = r'\b\d{4}\b'
        
        text_lines = text.split('\n')
        fios = []
        for line in text_lines:
            fio_match = re.match(fio_pattern, line.strip())
            if fio_match:
                fios.append(fio_match.group(0))
        
        years = re.findall(years_pattern, text)
        
        logging.info(f"Страница {i+1}: найдено {len(fios)} фамилий и {len(years)} годов")
        print(f"Страница {i+1}: найдено {len(fios)} фамилий и {len(years)} годов")
        
        fio_idx = 0
        for line in text_lines:
            if fio_idx >= len(fios):
                break
            fio = fios[fio_idx]
            if line.strip().startswith(fio):
                years_in_line = re.findall(years_pattern, line)
                birth_year = "Не найдено"
                death_year = "Не найдено"
                
                if years_in_line:
                    if len(years_in_line) >= 1:
                        death_year = years_in_line[-1]
                    if len(years_in_line) >= 2:
                        birth_year = years_in_line[0]
                
                result = (fio, birth_year, death_year)
                results.append(result)
                f.write(f"ФИО: {fio}, Год рождения: {birth_year}, Год смерти: {death_year}\n")
                f.flush()
                logging.info(f"Добавлено: {fio}, {birth_year}-{death_year}")
                fio_idx += 1
        
        os.remove(img_path)

# Вывод результатов
print("\nРезультаты обработки:")
for fio, birth, death in results:
    print(f"ФИО: {fio}, Год рождения: {birth}, Год смерти: {death}")

df = pd.DataFrame(results, columns=['ФИО', 'Год рождения', 'Год смерти'])
df.to_csv('burials.csv', index=False, encoding='utf-8')
logging.info("Результаты сохранены в burials.csv")
df.to_excel('burials.xlsx', index=False)
logging.info("Результаты сохранены в burials.xlsx")

logging.info("Обработка завершена")
print("Обработка завершена")