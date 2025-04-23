import os

def find_venvs(start_path):
    for root, dirs, files in os.walk(start_path):
        # Проверяем наличие папки Scripts и папки с файлами Python
        if 'Scripts' in dirs and 'python.exe' in os.listdir(root):
            print(f"Virtual environment found: {root}")

# Указываем путь к папке Users
find_venvs(r'C:\Users')