import pandas as pd
import re
from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import warnings

# Подавляем предупреждение о sipPyTypeDict
warnings.filterwarnings("ignore", category=DeprecationWarning)

class LogAnalyzer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Анализ логов Apache")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QtWidgets.QVBoxLayout()
        
        # Добавляем выпадающий список для выбора хостера
        self.hoster_selection = QtWidgets.QComboBox(self)
        self.hoster_selection.addItems(["Beget", "Nic"])
        self.layout.addWidget(self.hoster_selection)

        self.button = QtWidgets.QPushButton("Анализировать логи", self)
        self.button.clicked.connect(self.process_logs)
        self.layout.addWidget(self.button)

        # Таблица с настройкой размера
        self.table = QtWidgets.QTableWidget(self)
        self.table.setMinimumHeight(400)
        self.layout.addWidget(self.table, stretch=1)

        # Панель статистики с горизонтальной компоновкой
        self.stats_layout = QtWidgets.QHBoxLayout()

        # Левая колонка статистики
        self.left_stats = QtWidgets.QVBoxLayout()
        self.unique_ips_label = QtWidgets.QLabel("Количество уникальных IP: 0", self)
        self.left_stats.addWidget(self.unique_ips_label)

        self.top_ips_label = QtWidgets.QLabel("Топ 10 IP-адресов:\n", self)
        self.left_stats.addWidget(self.top_ips_label)

        self.status_codes_label = QtWidgets.QLabel("Статистика кодов ответов:\n", self)
        self.left_stats.addWidget(self.status_codes_label)

        self.stats_layout.addLayout(self.left_stats)

        # Правая колонка статистики
        self.right_stats = QtWidgets.QVBoxLayout()
        self.bots_label = QtWidgets.QLabel("Статистика ботов:\n", self)
        self.right_stats.addWidget(self.bots_label)

        self.request_methods_label = QtWidgets.QLabel("Статистика методов запросов:\n", self)
        self.right_stats.addWidget(self.request_methods_label)

        # Диапазон дат
        self.datetime_range_label = QtWidgets.QLabel("Диапазон дат:\nНе загружено", self)
        self.right_stats.addWidget(self.datetime_range_label)

        self.right_stats.addStretch()
        self.stats_layout.addLayout(self.right_stats)

        self.layout.addLayout(self.stats_layout)
        self.setLayout(self.layout)

    def process_logs(self):
        log_file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите файл логов Apache", "", "Log files (*.log)")
        if not log_file_path:
            return

        # Устанавливаем курсор ожидания
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)

        try:
            # Получаем выбранный хостер
            hoster = self.hoster_selection.currentText()

            # Определяем регулярное выражение и базовые колонки в зависимости от хостера
            if hoster == "Beget":
                pattern = r'(\S+) (\S+) \S+ \S+ \[(.*?)\] "(.*?)" (\d+) (.*)'
                base_columns = ['HOST', 'IP', 'date_time', 'request', 'SA', 'post_sa_data']
            else:  # Nic
                pattern = r'(\S+) \S+ \S+ \[(.*?)\] "(.*?)" (\d+) (.*)'
                base_columns = ['IP', 'date_time', 'request', 'SA', 'post_sa_data']

            rows = []

            # Чтение логов напрямую из файла
            with open(log_file_path, 'r') as f:
                for line in f:
                    match = re.match(pattern, line.strip())
                    if match:
                        row_data = list(match.groups())
                        rows.append(row_data)

            # Создаем DataFrame с базовыми колонками
            df_log = pd.DataFrame(rows, columns=base_columns)

            # Очистка IP-адресов от лишних символов
            df_log['IP'] = df_log['IP'].str.strip().str.rstrip('-')

            # Парсинг post_sa_data для User-Agent
            df_log['user_agent'] = df_log['post_sa_data'].apply(self.extract_user_agent)

            # Переставляем столбцы: user_agent перед post_sa_data
            if hoster == "Beget":
                df_log = df_log[['HOST', 'IP', 'date_time', 'request', 'SA', 'user_agent', 'post_sa_data']]
            else:  # Nic
                df_log = df_log[['IP', 'date_time', 'request', 'SA', 'user_agent', 'post_sa_data']]

            # Обновление таблицы
            self.update_table(df_log)

            # Обновление статистики
            self.update_statistics(df_log)

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))

        finally:
            # Восстанавливаем обычный курсор независимо от успеха или ошибки
            QtWidgets.QApplication.restoreOverrideCursor()

    def extract_user_agent(self, post_sa_data):
        matches = re.findall(r'"([^"]*)"', post_sa_data)
        if len(matches) >= 2:
            return matches[1]
        elif len(matches) == 1:
            return matches[0]
        return ""

    def update_table(self, df):
        self.table.setRowCount(df.shape[0])
        self.table.setColumnCount(df.shape[1])
        self.table.setHorizontalHeaderLabels(df.columns)

        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                self.table.setItem(i, j, QtWidgets.QTableWidgetItem(str(df.iat[i, j])))

        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)

    def update_statistics(self, df):
        unique_ips = df['IP'].nunique()
        self.unique_ips_label.setText(f"Количество уникальных IP: {unique_ips}")

        top_ips = df['IP'].value_counts().head(10)
        top_ips_text = "\n".join([f"{ip}: {count}" for ip, count in top_ips.items()])
        self.top_ips_label.setText(f"Топ 10 IP-адресов:\n{top_ips_text}")

        status_counts = df['SA'].value_counts()
        status_text = "\n".join([f"{code}: {count}" for code, count in status_counts.items()])
        self.status_codes_label.setText(f"Статистика кодов ответов:\n{status_text}")

        request_methods = df['request'].str.split(' ', expand=True)[0]
        method_counts = request_methods.value_counts()
        method_text = "\n".join([f"{method}: {count}" for method, count in method_counts.items()])
        self.request_methods_label.setText(f"Статистика методов запросов:\n{method_text}")

        bots_count = df['user_agent'].str.lower().str.contains('bot', na=False).sum()
        top_bots = df[df['user_agent'].str.lower().str.contains('bot', na=False)]['user_agent'].value_counts().head(10)
        bots_text = f"Количество ботов: {bots_count}\nТоп 10 ботов:\n" + "\n".join([f"{bot[:50]}...: {count}" for bot, count in top_bots.items()])
        self.bots_label.setText(f"Статистика ботов:\n{bots_text}")

        # Добавляем первую и последнюю дату из столбца date_time
        if not df.empty:
            first_date = df['date_time'].iloc[0]
            last_date = df['date_time'].iloc[-1]
            datetime_text = f"Диапазон дат:\nНачало: {first_date}\nКонец: {last_date}"
        else:
            datetime_text = "Диапазон дат:\nНет данных"
        self.datetime_range_label.setText(datetime_text)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    analyzer = LogAnalyzer()
    analyzer.show()
    sys.exit(app.exec_())