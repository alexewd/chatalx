import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QMessageBox, QScrollArea

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
        layout.addWidget(self.e1)

        # Кнопка поиска
        self.b1 = QPushButton('Поиск по номеру PKW MB', self)
        self.b1.clicked.connect(self.search_df)
        layout.addWidget(self.b1)

        # Кнопка очистки
        self.btnClear = QPushButton('Очистить!', self)
        self.btnClear.clicked.connect(self.clearTextInput)
        layout.addWidget(self.btnClear)

        # Кнопка выхода
        self.exit_btn = QPushButton('Выходим!', self)
        self.exit_btn.clicked.connect(self.close)
        layout.addWidget(self.exit_btn)

        # Текстовое поле с прокруткой
        self.scr = QTextEdit(self)
        self.scr.setReadOnly(True)  # Делаем текстовое поле только для чтения
        layout.addWidget(self.scr)

        self.setLayout(layout)

    def search_df(self):
        search_term = self.e1.text()
        search_result = mb.loc[mb['Artikel'].str.contains(search_term, na=False, case=False)]
        self.scr.clear()  # Очистка текстового поля перед выводом результатов
        self.scr.append(str(search_result))  # Вывод результатов в текстовое поле

    def clearTextInput(self):
        self.scr.clear()  # Очистка текстового поля

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
