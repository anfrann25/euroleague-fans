import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# --- 1. ΡΥΘΜΙΣΗ ΣΕΛΙΔΑΣ ---
st.set_page_config(page_title="EuroLeague Friends Fantasy", page_icon="🏀", layout="centered")

st.title("🏀 EuroLeague Friends League")
st.subheader("Η παρέα, οι προβλέψεις και η καζούρα!")

# --- 2. ΣΥΝΔΕΣΗ ΜΕ GOOGLE SHEETS ---
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

try:
    spreadsheet = init_connection()
    preds_sheet = spreadsheet.worksheet("predictions") # Tab για προβλέψεις
    users_sheet = spreadsheet.worksheet("user_creds")   # Tab για χρήστες
except Exception as e:
    st.error(f"Σφάλμα σύνδεσης με το Google Sheet (Βεβαιώσου ότι υπάρχουν τα tabs 'predictions' και 'user_creds'): {e}")
    st.stop()

# @st.cache_resource
# def init_connection():
#     scope = ["https://www.googleapis.com/auth/spreadsheets"]
#     creds_dict = dict(st.secrets["gcp_service_account"])
#     creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
#     client = gspread.authorize(creds)
    
#     # Ανοίγουμε το Google Sheet
#     spreadsheet = client.open("Euroleague_Predictions")
#     return spreadsheet

# try:
#     spreadsheet = init_connection()
#     preds_sheet = spreadsheet.worksheet("Sheet1") # Tab για προβλέψεις
#     users_sheet = spreadsheet.worksheet("Users")   # Tab για χρήστες
# except Exception as e:
#     st.error(f"Σφάλμα σύνδεσης με το Google Sheet (Βεβαιώσου ότι υπάρχουν τα tabs 'Sheet1' και 'Users'): {e}")
#     st.stop()


# --- 3. ΚΥΡΙΩΣ ΕΦΑΡΜΟΓΗ ---
st.success("Επιτυχής σύνδεση με το Google Sheet! 🚀")

# Εδώ μπορείς να συνεχίσεις με την υπόλοιπη λογική της εφαρμογής σου (φόρμες, αγώνες κλπ.)