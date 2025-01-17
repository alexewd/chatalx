import pandas as pd
from gspread_pandas import Spread
from gspread_pandas.conf import get_config, get_creds

import gspread
import pandas as pd
# from google.colab import auth
# auth.authenticate_user()
# from google.auth import default

# creds, _ = default()






secret = get_config(
    conf_dir= "e:/teract_ipynb/",
    file_name='mydasch-197308-ce756751640a.json'
)

creds = get_creds(config=secret)
gc = gspread.authorize(creds)

spreadsheet_link = 'https://docs.google.com/spreadsheets/d/1yWkkUxk-pFLzJI05-7WGfcd_3nR1uN1ezXm8W3XAHtc/edit?gid=0#gid=0'
spread = Spread(
    spreadsheet_link,
    creds=creds
)

worksheet = gc.open('f:\\chatepc\\chatalx\\work\\data\titanic.csv').sheet1
rows = worksheet.get_all_values()
pd.DataFrame.from_records(rows)


# # df = spread.sheet_to_df()
# spread.df_to_sheet
# # dat = pd.read_csv('f:\\chatepc\\chatalx\\work\\data\titanic.csv')
# dat = {'col1': [1, 2], 'col2': [3, 4]}
# df_test = pd.DataFrame(data=dat)
# df_test.head()

# # spread.df_to_sheet
# # df.sample(5)