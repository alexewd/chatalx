import pandas as pd

sheet_id = "1SXp5NDvINT5qPEztbnxjOgD3yniXHmyFeWFj8D7rpxg"
sheet_name = "titanic"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

df = pd.read_csv(url)
df.sample(6)