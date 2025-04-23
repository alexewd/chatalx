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

        # Панель статистики
        self.stats_layout = QtWidgets.QVBoxLayout()
        self.unique_ips_label = QtWidgets.QLabel("Количество уникальных IP: 0", self)
        self.stats_layout.addWidget(self.unique_ips_label)

        self.top_ips_label = QtWidgets.QLabel("Топ 10 IP-адресов:\n", self)
        self.stats_layout.addWidget(self.top_ips_label)

        self.status_codes_label = QtWidgets.QLabel("Статистика кодов ответов:\n", self)
        self.stats_layout.addWidget(self.status_codes_label)

        self.request_methods_label = QtWidgets.QLabel("Статистика методов запросов:\n", self)
        self.stats_layout.addWidget(self.request_methods_label)

        self.layout.addLayout(self.stats_layout)
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
            df_log = pd.read_csv(output_file_path, header=None)
            df_log.columns = ['HOST', 'IP', 'UN2', 'date_time', 'request', 'SA', 'UN3']

            # Очистка IP-адресов от лишних символов
            df_log['IP'] = df_log['IP'].str.strip().str.rstrip('-')

            # Обновление таблицы
            self.update_table(df_log)

            # Обновление статистики
            self.update_statistics(df_log)

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))

    def update_table(self, df):
        self.table.setRowCount(df.shape[0])
        self.table.setColumnCount(df.shape[1])
        self.table.setHorizontalHeaderLabels(df.columns)

        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                self.table.setItem(i, j, QtWidgets.QTableWidgetItem(str(df.iat[i, j])))

    def update_statistics(self, df):
        unique_ips = df['IP'].nunique()
        self.unique_ips_label.setText(f"Количество уникальных IP: {unique_ips}")

        top_ips = df['IP'].value_counts().head(10)
        top_ips_text = "\n".join([f"{ip}: {count}" for ip, count in top_ips.items()])
        self.top_ips_label.setText(f"Топ 10 IP-адресов:\n{top_ips_text}")

        # Статистика кодов ответов
        status_counts = df['SA'].value_counts()
        status_text = "\n".join([f"{code}: {count}" for code, count in status_counts.items()])
        self.status_codes_label.setText(f"Статистика кодов ответов:\n{status_text}")

        # Статистика методов запросов
        request_methods = df['request'].str.split(' ', expand=True)[0]  # Получаем метод запроса (GET, POST и т.д.)
        method_counts = request_methods.value_counts()
        method_text = "\n".join([f"{method}: {count}" for method, count in method_counts.items()])
        self.request_methods_label.setText(f"Статистика методов запросов:\n{method_text}")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    analyzer = LogAnalyzer()
    analyzer.show()
    sys.exit(app.exec_())
