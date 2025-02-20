import sys
import os
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox

# Определение пути к директории, где находится исполняемый файл
if getattr(sys, 'frozen', False):
    # Если запущено как исполняемый файл
    base_path = sys._MEIPASS
else:
    # Если запущено как скрипт
    base_path = os.path.dirname(os.path.abspath(__file__))

# Загрузка данных
mb = pd.read_csv(os.path.join(base_path, "mb_2025_01.csv"),
                 sep=";",
                 encoding="utf-8", usecols=["Artikel", "Benennung DE", "Gewicht", "Preis EUR"])



class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mercedes-Benz-Preisliste PKW MB-2025-01")
        self.setFixedSize(800, 600)  # Установка фиксированного размера окна

        # Создание компоновки
        layout = QVBoxLayout()

        # Поле ввода
        self.e1 = QLineEdit(self)
        self.e1.setPlaceholderText("Введите номер PKW MB")  # Подсказка в поле ввода
        layout.addWidget(self.e1)

        # Компоновка для кнопок
        button_layout = QHBoxLayout()

        # Кнопка выбора файла
        self.btnLoadFile = QPushButton('Выбрать файл прайс-листа', self)
        self.btnLoadFile.setFixedWidth(200)  # Установка фиксированной ширины кнопки
        self.btnLoadFile.clicked.connect(self.load_file)
        button_layout.addWidget(self.btnLoadFile)

        # Кнопка поиска
        self.b1 = QPushButton('Поиск по номеру PKW MB', self)
        self.b1.setFixedWidth(200)  # Установка фиксированной ширины кнопки
        self.b1.clicked.connect(self.search_df)
        button_layout.addWidget(self.b1)

        # Кнопка очистки
        self.btnClear = QPushButton('Очистить!', self)
        self.btnClear.setFixedWidth(200)  # Установка фиксированной ширины кнопки
        self.btnClear.clicked.connect(self.clearTextInput)
        button_layout.addWidget(self.btnClear)

        # Кнопка сохранения
        self.btnSave = QPushButton('Сохранить в CSV', self)
        self.btnSave.setFixedWidth(200)  # Установка фиксированной ширины кнопки
        self.btnSave.clicked.connect(self.save_to_csv)
        button_layout.addWidget(self.btnSave)

        # Кнопка выхода
        self.exit_btn = QPushButton('Выходим!', self)
        self.exit_btn.setFixedWidth(200)  # Установка фиксированной ширины кнопки
        self.exit_btn.clicked.connect(self.close)
        button_layout.addWidget(self.exit_btn)

        # Добавление компоновки кнопок в основной макет
        layout.addLayout(button_layout)

        # Таблица для отображения результатов
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)  # Установка количества столбцов
        self.table.setHorizontalHeaderLabels(["Artikel", "Benennung DE", "Gewicht", "Preis EUR"])  # Заголовки столбцов
        layout.addWidget(self.table)

        self.setLayout(layout)

        self.mb = None  # Переменная для хранения загруженного DataFrame

    def load_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите файл прайс-листа", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_name:
            try:
                self.mb = pd.read_csv(file_name, sep=";", encoding="utf-8", usecols=["Artikel", "Benennung DE", "Gewicht", "Preis EUR"])
                QMessageBox.information(self, "Успех", "Файл успешно загружен!")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить файл: {e}")

    def search_df(self):
        if self.mb is None:
            QMessageBox.warning(self, "Предупреждение", "Сначала выберите файл прайс-листа!")
            return

        search_term = self.e1.text().strip()  # Убираем пробелы в начале и конце
        if not search_term:  # Проверка на пустой ввод
            QMessageBox.warning(self, "Предупреждение", "Введите номер PKW MB для поиска!")
            return

        try:
            search_result = self.mb.loc[self.mb['Artikel'].str.contains(search_term, na=False, case=False)]
            
            if not search_result.empty:  # Проверка, есть ли результаты
                self.table.setRowCount(0)  # Очистка таблицы перед добавлением новых данных
                for row in range(len(search_result)):
                    for col in range(4):  # Заполнение таблицы данными
                        item = QTableWidgetItem(str(search_result.iloc[row, col]))
                        self.table.setItem(row, col, item)  # Добавляем новые строки в таблицу
            else:
                QMessageBox.information(self, "Результаты поиска", "Ничего не найдено.")
        except Exception as e:
            print(f"Ошибка в search_df: {e}")

    def clearTextInput(self):
        self.table.setRowCount(0)  # Очистка таблицы
        self.e1.clear()  # Очистка поля ввода

    def save_to_csv(self):
        if self.table.rowCount() == 0:
            QMessageBox.warning(self, "Предупреждение", "Нет данных для сохранения!")
            return

        # Открытие диалогового окна для выбора места сохранения
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "CSV Files (*.csv);;All Files (*)", options=options)
        
        if file_name:
            # Сохранение данных в CSV файл
            with open(file_name, 'w', encoding='utf-8') as f:
                for row in range(self.table.rowCount()):
                    line = []
                    for col in range(4):
                        item = self.table.item(row, col)
                        if item is not None:
                            line.append(item.text())
                        else:
                            line.append("")  # Если ячейка пустая, добавляем пустую строку
                    f.write(";".join(line) + "\n")  # Записываем строку в файл, разделяя значения точкой с запятой

            QMessageBox.information(self, "Успех", "Данные успешно сохранены в файл!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
