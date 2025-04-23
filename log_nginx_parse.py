import pandas as pd
import re

# Функция для парсинга строки лога
def parse_log_line(line):
    log_pattern = r'(?P<ip>[\d\.]+) - - $$(?P<date>[^$$]+)\] "(?P<method>\w+) (?P<url>.+?) HTTP\/\d\.\d" (?P<status>\d{3}) (?P<size>\d+) "(?P<referrer>.*?)" "(?P<user_agent>.*?)"'
    match = re.match(log_pattern, line)
    if match:
        return match.groupdict()
    return None

# Чтение логов из файла
def read_logs(file_path):
    with open(file_path, 'r') as file:
        logs = file.readlines()
    
    parsed_logs = [parse_log_line(line) for line in logs]
    print(f"Parsed logs count: {len(parsed_logs)}")
    return [log for log in parsed_logs if log is not None]

# Анализ логов
def analyze_logs(logs):
    df = pd.DataFrame(logs)
    
    # Проверяем, какие столбцы есть в DataFrame
    print("Columns in DataFrame:", df.columns.tolist())
    
    # Преобразование столбцов
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], format='%d/%b/%Y:%H:%M:%S %z')
    else:
        print("Column 'date' not found in DataFrame.")
    
    if 'status' in df.columns:
        df['status'] = df['status'].astype(int)
    else:
        print("Column 'status' not found in DataFrame.")
    
    if 'size' in df.columns:
        df['size'] = df['size'].astype(int)
    else:
        print("Column 'size' not found in DataFrame.")

    # Переупорядочивание столбцов
    df = df[['ip', 'date', 'method', 'url', 'status', 'size', 'referrer', 'user_agent']]

    # Основные метрики
    total_requests = len(df)
    status_counts = df['status'].value_counts()
    top_urls = df['url'].value_counts().head(10)
    
    print(f"Total requests: {total_requests}")
    print("Status code counts:")
    print(status_counts)
    print("Top 10 requested URLs:")
    print(top_urls)

    # Вывод DataFrame
    print("\nDataFrame with logs:")
    print(df.head())  # Вывод первых 5 строк DataFrame

# Путь к файлу с логами
log_file_path = 'mobesk.ru.access_log'

# Выполнение анализа
logs = read_logs(log_file_path)
analyze_logs(logs)
