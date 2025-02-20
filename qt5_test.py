import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

def on_button_click():
    print("Кнопка нажата!")

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Пример приложения на PyQt")

layout = QVBoxLayout()
button = QPushButton("Нажми меня")
button.clicked.connect(on_button_click)

layout.addWidget(button)
window.setLayout(layout)

window.show()
sys.exit(app.exec_())
