import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd

class CSVSearcher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CSV Search")
        
        self.create_widgets()
        self.results_df = pd.DataFrame()  # DataFrame для хранения результатов поиска
    
    def create_widgets(self):
        # Create and place widgets
        self.load_button = ttk.Button(self, text="Load CSV File", command=self.load_file)
        self.load_button.grid(row=0, column=0, padx=10, pady=10)

        self.filename_label = ttk.Label(self, text="No file selected")
        self.filename_label.grid(row=0, column=1, padx=10, pady=10, columnspan=4)

        self.column_label = ttk.Label(self, text="Select Column:")
        self.column_label.grid(row=1, column=0, padx=10, pady=10)
        
        self.column_combo = ttk.Combobox(self, state="readonly")
        self.column_combo.grid(row=1, column=1, padx=10, pady=10)
        
        self.search_label = ttk.Label(self, text="Search Value:")
        self.search_label.grid(row=2, column=0, padx=10, pady=10)

        self.search_entry = ttk.Entry(self)
        self.search_entry.grid(row=2, column=1, padx=10, pady=10)

        # Добавляем обработчик для вставки текста
        self.search_entry.bind("<Control-v>", self.paste)

        self.search_button = ttk.Button(self, text="Search", command=self.search_value)
        self.search_button.grid(row=2, column=2, padx=10, pady=10)

        self.save_button = ttk.Button(self, text="Save Results", command=self.save_results)
        self.save_button.grid(row=2, column=3, padx=10, pady=10)

        self.clear_button = ttk.Button(self, text="Clear", command=self.clear_output)
        self.clear_button.grid(row=2, column=4, padx=10, pady=10)

        self.exit_button = ttk.Button(self, text="Exit", command=self.quit_app)
        self.exit_button.grid(row=2, column=5, padx=10, pady=10)

        self.result_frame = ttk.Frame(self)
        self.result_frame.grid(row=3, column=0, columnspan=6, padx=10, pady=10)
        
        self.result_text = tk.Text(self.result_frame, wrap="none", height=20, width=100)
        self.result_text.grid(row=0, column=0)

        self.result_scrollbar_y = ttk.Scrollbar(self.result_frame, orient="vertical", command=self.result_text.yview)
        self.result_scrollbar_y.grid(row=0, column=1, sticky="ns")

        self.result_scrollbar_x = ttk.Scrollbar(self.result_frame, orient="horizontal", command=self.result_text.xview)
        self.result_scrollbar_x.grid(row=1, column=0, sticky="ew")

        self.result_text.config(yscrollcommand=self.result_scrollbar_y.set, xscrollcommand=self.result_scrollbar_x.set)

        self.file_path = None
        self.df = None
        self.chunksize = 10000  # Define the chunk size for processing

    def load_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if self.file_path:
            try:
                self.df = pd.read_csv(self.file_path, encoding='utf-8', sep=';')
                self.column_combo['values'] = list(self.df.columns)
                self.column_combo.current(0)
                self.filename_label.config(text=self.file_path.split("/")[-1])  # Display file name
                messagebox.showinfo("Success", "File loaded successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")
        else:
            messagebox.showerror("Error", "No file selected.")

    def search_value(self):
        if self.df is None:
            messagebox.showerror("Error", "Please load a CSV file first.")
            return
        
        search_value = self.search_entry.get()
        selected_column = self.column_combo.get()
        if not search_value:
            messagebox.showerror("Error", "Please enter a value to search for.")
            return
        
        if not selected_column:
            messagebox.showerror("Error", "Please select a column to search in.")
            return
        
        results = []
        try:
            for chunk in pd.read_csv(self.file_path, encoding='utf-8', sep=';', chunksize=self.chunksize):
                result = chunk[selected_column].astype(str).str.contains(search_value, na=False)
                if result.any():
                    results.append(chunk[result])
            if results:
                new_results_df = pd.concat(results)  # Сохраняем новые результаты в DataFrame
                self.results_df = pd.concat([self.results_df, new_results_df]).drop_duplicates()  # Объединяем с предыдущими результатами и удаляем дубликаты
                self.display_results(self.results_df)
            else:
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, "No matching value found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while processing the file: {e}")

    def clear_output(self):
        self.result_text.delete(1.0, tk.END)
        self.results_df = pd.DataFrame()  # Очищаем результаты

    def display_results(self, results_df):
        self.result_text.delete(1.0, tk.END)
        # Форматируем вывод как таблицу
        formatted_results = results_df.to_string(index=False, header=True)
        self.result_text.insert(tk.END, formatted_results)

    def save_results(self):
        if self.results_df.empty:
            messagebox.showerror("Error", "No results to save.")
            return
        
        save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if save_path:
            try:
                self.results_df.to_csv(save_path, index=False, sep=';')
                messagebox.showinfo("Success", "Results saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save results: {e}")

    def paste(self, event):
        # Вставляем текст из буфера обмена
        try:
            # Очищаем текущее выделение
            self.search_entry.selection_clear(0, tk.END)
            # Вставляем текст из буфера обмена
            self.search_entry.insert(tk.END, self.clipboard_get())
        except tk.TclError:
            pass  # Если буфер обмена пуст, ничего не делаем

    def quit_app(self):
        self.quit()
        self.destroy()

if __name__ == "__main__":
    app = CSVSearcher()
    app.mainloop()

