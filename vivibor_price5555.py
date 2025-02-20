import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Поиск по прайс-листу")
        self.setFixedSize(800, 600)

        # Создание компоновки
        layout = QVBoxLayout()

        # Поле ввода
        self.e1 = QLineEdit(self)
        self.e1.setPlaceholderText("Введите номер PKW MB")
        layout.addWidget(self.e1)

        # Компоновка для кнопок
        button_layout = QHBoxLayout()

        # Кнопка выбора файла
        self.btnLoadFile = QPushButton('Выбрать файл прайс-листа', self)
        self.btnLoadFile.clicked.connect(self.load_file)
        button_layout.addWidget(self.btnLoadFile)

        # Кнопка поиска
        self.b1 = QPushButton('Поиск по номеру PKW MB', self)
        self.b1.clicked.connect(self.search_df)
        button_layout.addWidget(self.b1)

        layout.addLayout(button_layout)

        # Таблица для отображения результатов
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Artikel", "Benennung DE", "Gewicht", "Preis EUR"])
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

        search_term = self.e1.text().strip()
        if not search_term:
            QMessageBox.warning(self, "Предупреждение", "Введите номер PKW MB для поиска!")
            return

        # Поиск по DataFrame
        search_result = self.mb[self.mb['Artikel'].str.contains(search_term, na=False, case=False)]

        if not search_result.empty:
            # Получаем текущее количество строк в таблице
            current_row_count = self.table.rowCount()
            self.table.setRowCount(current_row_count + len(search_result))  # Увеличиваем количество строк

            for row in range(len(search_result)):
                for col in range(4):  # Заполнение таблицы данными
                    item = QTableWidgetItem(str(search_result.iloc[row, col]))
                    self.table.setItem(current_row_count + row, col, item)  # Добавляем новые строки в таблицу
            QMessageBox.information(self, "Результаты поиска", "Результаты найдены.")
        else:
            QMessageBox.information(self, "Результаты поиска", "Ничего не найдено.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
