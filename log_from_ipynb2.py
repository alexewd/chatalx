import pandas as pd
import io
from lars import apache, csv
from PyQt5 import QtWidgets, QtGui
import sys

class LogAnalyzer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Анализ логов Apache")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QtWidgets.QVBoxLayout()

        self.button = QtWidgets.QPushButton("Анализировать логи", self)
        self.button.clicked.connect(self.process_logs)
        self.layout.addWidget(self.button)

        self.table = QtWidgets.QTableWidget(self)
        self.layout.addWidget(self.table)

        self.setLayout(self.layout)

    def process_logs(self):
        log_file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите файл логов Apache", "", "Log files (*.log)")
        if not log_file_path:
            return

        output_file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Сохранить выходной файл", "", "CSV files (*.csv)")
        if not output_file_path:
            return

        try:
            # Чтение логов Apache и запись в CSV
            with io.open(log_file_path, 'r') as f, \
                 io.open(output_file_path, 'wb') as outfile:
                with apache.ApacheSource(f) as source, csv.CSVTarget(outfile) as target:
                    for row in source:
                        target.write(row)

            # Загрузка данных из CSV
            df_log = pd.read_csv(output_file_path)
            df_log.columns = ['IP', 'UN1', 'UN2', 'date_time', 'request', 'SA', 'UN3']

            # Обновление таблицы
            self.update_table(df_log)

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))

    def update_table(self, df):
        self.table.setRowCount(df.shape[0])
        self.table.setColumnCount(df.shape[1])
        self.table.setHorizontalHeaderLabels(df.columns)

        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                self.table.setItem(i, j, QtWidgets.QTableWidgetItem(str(df.iat[i, j])))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    analyzer = LogAnalyzer()
    analyzer.show()
    sys.exit(app.exec_())
