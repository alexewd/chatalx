import pandas as pd
import io
from lars import apache, csv
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

def process_logs():
    try:
        # Открытие диалогового окна для выбора файла логов
        log_file_path = filedialog.askopenfilename(title="Выберите файл логов Apache", filetypes=[("Log files", "*.log")])
        if not log_file_path:
            return  # Если файл не выбран, выходим из функции

        # Открытие диалогового окна для выбора имени выходного файла
        output_file_path = filedialog.asksaveasfilename(title="Сохранить выходной файл", defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not output_file_path:
            return  # Если имя файла не указано, выходим из функции

        # Чтение логов Apache и запись в CSV
        with io.open(log_file_path, 'r') as f, \
             io.open(output_file_path, 'wb') as outfile:
            with apache.ApacheSource(f) as source, csv.CSVTarget(outfile) as target:
                for row in source:
                    target.write(row)

        # Загрузка данных из CSV
        df_log = pd.read_csv(output_file_path)
        df_log.columns = ['IP', 'UN1', 'UN2', 'date_time', 'request', 'SA', 'UN3']

        # Подсчет уникальных IP
        unique_ips = df_log['IP'].nunique()
        ip_counts = df_log['IP'].value_counts().head(10)

        # Вывод результатов
        result = f"Количество уникальных IP: {unique_ips}\n\n"
        result += "Топ 10 IP-адресов:\n"
        result += ip_counts.to_string()

        messagebox.showinfo("Результаты анализа", result)

    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

# Создание графического интерфейса
root = tk.Tk()
root.title("Анализ логов Apache")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

button = tk.Button(frame, text="Анализировать логи", command=process_logs)
button.pack()

root.mainloop()
