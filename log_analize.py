import pandas as pd
import re
import tkinter as tk
from tkinter import filedialog, messagebox

def parse_log_line(line):
    # Регулярное выражение для разбора строки лога
    log_pattern = re.compile(
        r'(?P<host>[\w.-]+) (?P<ip>[\d.]+) - - $$(?P<date>.+?)$$ "(?P<method>\w+) (?P<url>.+?) HTTP/\d\.\d" (?P<status>\d{3}) (?P<size>\d+) "(?P<referrer>.*)" "(?P<user_agent>.*)" (?P<time_taken>\d+) (?P<other_info>.*)'
    )
    match = log_pattern.match(line)
    if match:
        # Собираем все остальные данные в один столбец
        other_info = ' '.join([match.group('method'), match.group('url'), match.group('status'), match.group('size'), match.group('referrer'), match.group('user_agent'), match.group('time_taken')])
        return {
            'host': match.group('host'),
            'ip': match.group('ip'),
            'other': other_info
        }
    return None

def analyze_logs(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:  # Указываем кодировку UTF-8
        log_lines = file.readlines()

    parsed_logs = []
    unparsed_lines = []

    for line in log_lines:
        parsed_line = parse_log_line(line)
        if parsed_line:
            parsed_logs.append(parsed_line)
        else:
            unparsed_lines.append(line.strip())  # Сохраняем неразобранные строки

    if not parsed_logs:
        raise ValueError("Не удалось разобрать логи. Проверьте формат файла.")
    
    if unparsed_lines:
        print("Не удалось разобрать следующие строки:")
        for line in unparsed_lines:
            print(line)

    df = pd.DataFrame(parsed_logs)

    return df

def open_file():
    file_path = filedialog.askopenfilename(title="Выберите файл логов", filetypes=[("Log files", "*.log")])
    if file_path:
        try:
            df = analyze_logs(file_path)
            messagebox.showinfo("Результаты анализа", df.to_string(index=False))
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

# Создание графического интерфейса
root = tk.Tk()
root.title("Анализ логов Apache/Nginx")

open_button = tk.Button(root, text="Открыть файл логов", command=open_file)
open_button.pack(pady=20)

root.mainloop()
