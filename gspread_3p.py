from google import auth
auth.authenticate_user()
import gspread_pandas
from google.auth import default
import pandas as pd
creds, _ = default()

df = pd.DataFrame([1,2,3,4], columns=['T'])
##create new sheet and dump dataframe
spread = gspread_pandas.Spread('New Spreadsheet Name', creds=creds, create_spread=True)
spread.df_to_sheet(df, index=False, headers=True, start='A1',)
## open existing spreadsheet
spreadsheetId = '1DayucszOBJhOT1rNdfdft919tp20os'
spread = gspread_pandas.Spread(spreadsheetId, creds=creds,)
##grab data into dataframe
df = spread.sheet_to_df(index=0,start_row=2)