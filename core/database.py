import streamlit as st
from google.oauth2.service_account import Credentials 
import gspread

@st.cache_resource
def init_connection():
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    # Χρησιμοποιούμε το τοπικό αρχείο credentials (ή μπορείς να το αλλάξεις αν θες secrets)
    creds = Credentials.from_service_account_file("creds.json", scopes=scope)
    client = gspread.authorize(creds)
    
    # Άνοιγμα απευθείας με το Sheet ID που δουλεύει εγγυημένα
    sheet_id = "180YR2hX6lUQTETaDdKlpHjVTwqbCPslXKkqdft9ISNk"
    spreadsheet = client.open_by_key(sheet_id)
    return spreadsheet