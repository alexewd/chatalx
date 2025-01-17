import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# Укажите область доступа
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Укажите путь к вашему JSON-ключу
credentials = ServiceAccountCredentials.from_json_keyfile_name("e:/teract_ipynb/mydasch-197308-ce756751640a.json" , scope)

# Авторизация
gc = gspread.authorize(credentials)

# Открываем таблицу по ID
file_id = "1SXp5NDvINT5qPEztbnxjOgD3yniXHmyFeWFj8D7rpxg"
spreadsheet = gc.open_by_key(file_id)

# Работа с первым листом
sheet = spreadsheet.sheet1

# Читаем все данные
data = sheet.get_all_values()

# Преобразуем в DataFrame
df = pd.DataFrame(data[1:], columns=data[0])
print(df)