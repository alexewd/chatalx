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

# Определяем количество страниц в PDF
from pdf2image import pdfinfo_from_path
try:
    pdf_info = pdfinfo_from_path(pdf_path, poppler_path=r'C:\poppler\Library\bin')
    total_pages = pdf_info["Pages"]
    logging.info(f"Всего страниц в PDF: {total_pages}")
    print(f"Всего страниц в PDF: {total_pages}")
except Exception as e:
    logging.error(f"Ошибка при получении информации о PDF: {str(e)}")
    raise

results = []
output_file = r'c:\bac_c\nekropol\burials.txt'
batch_size = 20  # Записываем каждые 20 страниц

# Функция для записи порции результатов
def save_batch(results, output_file):
    with open(output_file, 'a', encoding='utf-8') as f:  # 'a' — добавление, а не перезапись
        for fio, birth, death in results:
            f.write(f"ФИО: {fio}, Год рождения: {birth}, Год смерти: {death}\n")
        f.flush()
    logging.info(f"Сохранена порция из {len(results)} записей в {output_file}")

# Обработка с прогресс-баром по одной странице
print("Запуск обработки всего файла...")
logging.info("Запуск обработки всего файла...")
for i in tqdm(range(total_pages), desc="Обработка страниц"):
    logging.info(f"Конвертация страницы {i+1}")
    pages = convert_from_path(pdf_path, 200, poppler_path=r'C:\poppler\Library\bin', 
                             first_page=i+1, last_page=i+1)
    if not pages:
        logging.warning(f"Страница {i+1} не была конвертирована")
        continue
    
    img_path = f'page_{i}.png'
    logging.info(f"Сохранение страницы {i+1} как {img_path}")
    pages[0].save(img_path, 'PNG')
    
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
    
    if fios:
        logging.info(f"Найденные фамилии: {', '.join(fios)}")
    if years:
        logging.info(f"Найденные годы: {', '.join(years)}")
    if not fios and not years:
        logging.warning(f"На странице {i+1} ничего не найдено!")
    
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
            logging.info(f"Добавлено в память: {fio}, {birth_year}-{death_year}")
            print(f"Добавлено: {fio}, {birth_year}-{death_year}")
            fio_idx += 1
    
    # Сохраняем порцию каждые 20 страниц
    if (i + 1) % batch_size == 0 or (i + 1) == total_pages:
        save_batch(results, output_file)
        results = []  # Очищаем память после сохранения
    
    os.remove(img_path)

# Финальное сохранение остатка (если остался)
if results:
    save_batch(results, output_file)

# Вывод результатов
print("\nРезультаты обработки всего файла:")
with open(output_file, 'r', encoding='utf-8') as f:
    print(f.read())

df = pd.DataFrame(results, columns=['ФИО', 'Год рождения', 'Год смерти'])
df.to_csv(r'c:\bac_c\nekropol\burials.csv', index=False, encoding='utf-8')
logging.info("Результаты сохранены в burials.csv")
df.to_excel(r'c:\bac_c\nekropol\burials.xlsx', index=False)
logging.info("Результаты сохранены в burials.xlsx")

logging.info("Обработка завершена")
print("Обработка завершена")