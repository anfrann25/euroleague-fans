import gspread
from google.oauth2.service_account import Credentials

scope = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("creds.json", scopes=scope)
client = gspread.authorize(creds)

# Δοκιμή ανοίγματος
sheet_id = "180YR2hX6lUQTETaDdKlpHjVTwqbCPslXKkqdft9ISNk"
sheet = client.open_by_key(sheet_id)


vals = sheet.title
print(vals)
