import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QTableWidget, QTableWidgetItem

import os

# Установите текущий рабочий каталог на каталог, где находится скрипт
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Загрузка данных
mb = pd.read_csv("MB-2025-01(10)-Kunde(Customer).csv",
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

    def search_df(self):
        search_term = self.e1.text()
        search_result = mb.loc[mb['Artikel'].str.contains(search_term, na=False, case=False)]
        
        if not search_result.empty:  # Проверка, есть ли результаты
            current_row_count = self.table.rowCount()  # Получаем текущее количество строк
            new_row_count = current_row_count + len(search_result)  # Общее количество строк после добавления новых результатов
            self.table.setRowCount(new_row_count)  # Установка нового количества строк

            for row in range(len(search_result)):
                for col in range(4):  # Заполнение таблицы данными
                    item = QTableWidgetItem(str(search_result.iloc[row, col]))
                    self.table.setItem(current_row_count + row, col, item)  # Добавляем новые строки в конец таблицы

    def clearTextInput(self):
        self.table.setRowCount(0)  # Очистка таблицы

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
