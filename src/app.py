import os
import pandas as pd
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# --- 1. ΡΥΘΜΙΣΗ ΣΕΛΙΔΑΣ ---
st.set_page_config(page_title="EuroLeague Friends Fantasy", page_icon="🏀", layout="centered")

st.title("🏀 EuroLeague Friends League")
st.subheader("Η παρέα, οι προβλέψεις και η καζούρα!")

# --- 2. ΣΥΝΔΕΣΗ ΜΕ GOOGLE SHEETS ---
@st.cache_resource
def init_connection():
    scope = ["https://www.spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = dict(st.secrets["gcp_service_account"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
    
    # Ανοίγουμε το Google Sheet
    spreadsheet = client.open("Euroleague_Predictions")
    return spreadsheet

try:
    spreadsheet = init_connection()
    preds_sheet = spreadsheet.worksheet("predictions") # Tab για προβλέψεις
    users_sheet = spreadsheet.worksheet("user_creds")   # Tab για χρήστες
except Exception as e:
    st.error(f"Σφάλμα σύνδεσης με το Google Sheet (Βεβαιώσου ότι υπάρχουν τα tabs 'predictions' και 'user_creds'): {e}")
    st.stop()

# --- 3. ΦΟΡΤΩΣΗ ΠΡΟΓΡΑΜΜΑΤΟΣ ---
@st.cache_data
def load_schedule():
    paths_to_try = [
        "Euroleague_Perfect_Schedule.xlsx",
        "../data/Euroleague_Perfect_Schedule.xlsx",
        "data/Euroleague_Perfect_Schedule.xlsx"
    ]
    for path in paths_to_try:
        if os.path.exists(path):
            return pd.read_excel(path)
    raise FileNotFoundError("Δεν βρέθηκε το αρχείο Excel!")

try:
    df_schedule = load_schedule()
except Exception as e:
    st.error(f"Σφάλμα φόρτωσης προγράμματος: {e}")
    st.stop()

# --- 4. ΔΥΝΑΜΙΚΟ LOGIN ΑΠΟ GOOGLE SHEET ---
def get_users_db():
    try:
        users_data = users_sheet.get_all_records()
        return {str(row['username']).strip(): str(row['password']).strip() for row in users_data if 'username' in row}
    except Exception:
        return {}

users_db = get_users_db()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

if not st.session_state.logged_in:
    st.sidebar.subheader("🔐 Σύνδεση Χρήστη")
    username_input = st.sidebar.text_input("Username")
    password_input = st.sidebar.text_input("Password", type="password")
    
    if st.sidebar.button("Login"):
        if username_input in users_db and users_db[username_input] == password_input:
            st.session_state.logged_in = True
            st.session_state.username = username_input
            st.sidebar.success(f"Καλώς ήρθες, {username_input}!")
            st.rerun()
        else:
            st.sidebar.error("Λάθος στοιχεία ή άγνωστος χρήστης!")
    st.stop()

st.sidebar.write(f"👤 Συνδεδεμένος: **{st.session_state.username}**")
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()

# --- 5. ΚΥΡΙΩΣ ΕΦΑΡΜΟΓΗ & ΠΡΟΒΛΕΨΕΙΣ ---
st.divider()
rounds = df_schedule['Αγωνιστική'].unique()
selected_round = st.selectbox("Επιλέξτε Αγωνιστική:", rounds)

matches_to_play = df_schedule[df_schedule['Αγωνιστική'] == selected_round]

st.markdown(f"### 📋 Παιχνίδια για την {selected_round}")

with st.form(key="predictions_form"):
    user_predictions = {}
    
    for idx, row in matches_to_play.iterrows():
        home = row['Γηπεδούχος']
        away = row['Φιλοξενούμενος']
        
        st.write(f"**{home}** vs **{away}**")
        pred = st.radio(
            f"Νικητής αγώνα {home} - {away}",
            [home, "Ισοπαλία/Παράταση", away],
            key=f"match_{idx}",
            horizontal=True
        )
        user_predictions[(home, away)] = pred
        st.markdown("---")
        
    submit_button = st.form_submit_button(label="💾 Υποβολή Προβλέψεων Αγωνιστικής")
    
    if submit_button:
        try:
            for (home, away), pred in user_predictions.items():
                preds_sheet.append_row([st.session_state.username, selected_round, f"{home} vs {away}", pred])
            st.success(f"Οι προβλέψεις σου για την {selected_round} αποθηκεύτηκαν επιτυχώς στο Cloud!")
        except Exception as e:
            st.error(f"Απέτυχε η αποθήκευση: {e}")

# --- 6. LEADERBOARD (ΑΠΟ GOOGLE SHEETS) ---
st.divider()
st.subheader("🏆 Live Leaderboard")
try:
    data = preds_sheet.get_all_records()
    if data:
        df_preds = pd.DataFrame(data)
        st.dataframe(df_preds, use_container_width=True)
    else:
        st.info("Δεν υπάρχουν ακόμα αποθηκευμένες προβλέψεις.")
except Exception as e:
    st.warning("Δεν ήταν δυνατή η ανάκτηση του leaderboard.")