import streamlit as st
from core.database import init_connection
from views.login import render_login
from views.predictions import render_predictions

# 1. ΡΥΘΜΙΣΕΙΣ ΣΕΛΙΔΑΣ
st.set_page_config(page_title="EuroLeague Friends Fantasy", page_icon="🏀", layout="centered")

st.title("🏀 EuroLeague Friends League")
st.write("Η παρέα, οι προβλέψεις και η καζούρα!")

# 2. ΣΥΝΔΕΣΗ ΜΕ ΒΑΣΗ ΔΕΔΟΜΕΝΩΝ
try:
    spreadsheet = init_connection()
    users_sheet = spreadsheet.worksheet("user_creds")
    preds_sheet = spreadsheet.worksheet("predictions") 
except Exception as e:
    st.error(f"Σφάλμα σύνδεσης με το Google Sheet: {e}")
    st.stop()

# 3. ΕΛΕΓΧΟΣ ΣΥΝΔΕΣΗΣ & ΕΜΦΑΝΙΣΗ ΣΕΛΙΔΩΝ
if "logged_in_user" not in st.session_state:
    render_login(users_sheet)
else:
    st.sidebar.write(f"👤 Συνδεδεμένος ως: **{st.session_state['logged_in_user']}**")
    if st.sidebar.button("🚪 Αποσύνδεση", use_container_width=True):
        del st.session_state["logged_in_user"]
        st.rerun()
        
    st.success(f"Καλώς ήρθες, **{st.session_state['logged_in_user']}**! 🚀")
    
    # Εμφάνιση της φόρμας προβλέψεων!
    render_predictions(preds_sheet, st.session_state['logged_in_user'])