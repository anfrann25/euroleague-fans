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

# 3. ΣΥΣΤΗΜΑ ΧΡΗΣΤΩΝ
if "logged_in_user" not in st.session_state:
    st.subheader("🔑 Πύλη Σύνδεσης")
    tab_login, tab_signup = st.tabs(["Είσοδος", "Εγγραφή"])
    
    with tab_login:
        login_user = st.text_input("Όνομα Χρήστη", key="l_user")
        login_pass = st.text_input("Κωδικός", type="password", key="l_pass")
        if st.button("Σύνδεση", use_container_width=True, type="primary"):
            try:
                users_data = users_sheet.get_all_records()
            except:
                users_data = []
            
            if any(str(u.get("username")) == login_user and str(u.get("password")) == login_pass for u in users_data):
                st.session_state["logged_in_user"] = login_user
                st.rerun()
            else:
                st.error("Λάθος όνομα χρήστη ή κωδικός!")

    with tab_signup:
        new_user = st.text_input("Νέο Όνομα Χρήστη", key="s_user")
        new_pass = st.text_input("Νέος Κωδικός", type="password", key="s_pass")
        if st.button("Δημιουργία Λογαριασμού", use_container_width=True):
            if new_user and new_pass:
                try:
                    users_data = users_sheet.get_all_records()
                    usernames = [str(u.get("username")) for u in users_data]
                except:
                    usernames = []
                    
                if new_user in usernames:
                    st.error("Αυτό το όνομα υπάρχει ήδη!")
                else:
                    users_sheet.append_row([new_user, new_pass])
                    st.success("Η εγγραφή ολοκληρώθηκε! Πήγαινε στην 'Είσοδο'.")
            else:
                st.warning("Συμπλήρωσε όλα τα πεδία.")

else:
    st.sidebar.write(f"👤 Συνδεδεμένος ως: **{st.session_state['logged_in_user']}**")
    if st.sidebar.button("🚪 Αποσύνδεση", use_container_width=True):
        del st.session_state["logged_in_user"]
        st.rerun()
        
    st.success(f"Καλώς ήρθες, **{st.session_state['logged_in_user']}**! 🚀")
    st.info("Είσαι συνδεδεμένος. Έτοιμοι για την προσθήκη των αγώνων;")