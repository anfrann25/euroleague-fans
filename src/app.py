import pandas as pd
import streamlit as st

# --- 1. ΡΥΘΜΙΣΗ ΣΕΛΙΔΑΣ ---
st.set_page_config(
    page_title="EuroLeague Friends Fantasy", page_icon="🏀", layout="centered"
)

st.title("🏀 EuroLeague Friends League")
st.subheader("Η παρέα, οι προβλέψεις και η καζούρα!")

# --- 2. ΦΟΡΤΩΣΗ ΠΡΟΓΡΑΜΜΑΤΟΣ ---
@st.cache_data
def load_schedule():
  # Διαβάζουμε το τέλειο αρχείο excel που φτιάξαμε
  df = pd.read_excel("../data/Euroleague_Perfect_Schedule.xlsx")
  return df


try:
  df_schedule = load_schedule()
except FileNotFoundError:
  st.error(
      "Δεν βρέθηκε το αρχείο 'Euroleague_Perfect_Schedule.xlsx'. Βεβαιώσου ότι"
      " είναι στον ίδιο φάκελο!"
  )
  st.stop()

# --- 3. ΑΠΛΟ ΣΥΣΤΗΜΑ LOGIN ---
# Λίστα χρηστών και κωδικών της παρέας (μπορείς να τους αλλάξεις)
users_db = {
    "giannis": "1234",
    "michalis": "1234",
    "kostas": "1234",
}

if "logged_in" not in st.session_state:
  st.session_state.logged_in = False
  st.session_state.username = ""

if not st.session_state.logged_in:
  st.sidebar.subheader("🔐 Σύνδεση Χρήστη")
  username_input = st.sidebar.text_input("Username")
  password_input = st.sidebar.text_input("Password", type="password")

  if st.sidebar.button("Login"):
    if (
        username_input in users_db
        and users_db[username_input] == password_input
    ):
      st.session_state.logged_in = True
      st.session_state.username = username_input
      st.sidebar.success(f"Καλώς ήρθες, {username_input}!")
      st.rerun()
    else:
      st.sidebar.error("Λάθος στοιχεία!")
  st.stop()

# Αν είναι συνδεδεμένος:
st.sidebar.write(f"👤 Συνδεδεμένος: **{st.session_state.username}**")
if st.sidebar.button("Logout"):
  st.session_state.logged_in = False
  st.session_state.username = ""
  st.rerun()

# --- 4. ΚΥΡΙΩΣ ΕΦΑΡΜΟΓΗ ---
st.divider()
rounds = df_schedule["Αγωνιστική"].unique()
selected_round = st.selectbox("Επιλέξτε Αγωνιστική:", rounds)

# Φιλτράρισμα αγώνων για την αγωνιστική που επέλεξε
matches_to_play = df_schedule[df_schedule["Αγωνιστική"] == selected_round]

st.markdown(f"### 📋 Παιχνίδια για την {selected_round}")

# Φόρμα υποβολής προβλέψεων
with st.form(key="predictions_form"):
  user_predictions = {}

  for idx, row in matches_to_play.iterrows():
    home = row["Γηπεδούχος"]
    away = row["Φιλοξενούμενος"]

    st.write(**{home}** vs **{away}**")
    # Ο χρήστης επιλέγει νικητή
    pred = st.radio(
        f"Νικητής αγώνα {home} - {away}",
        [home, "Ισοπαλία/Παράταση", away],
        key=f"match_{idx}",
        horizontal=True,
    )
    user_predictions[(home, away)] = pred
    st.markdown("---")

  submit_button = st.form_submit_button(
      label="💾 Υποβολή Προβλέψεων Αγωνιστικής"
  )

  if submit_button:
    st.success(
        f"Οι προβλέψεις σου για την {selected_round} αποθηκεύτηκαν επιτυχώς!"
    )
    # Εδώ αργότερα θα αποθηκεύουμε τις προβλέψεις στη βάση/αρχείο του χρήστη

# --- 5. LEADERBOARD (ΠΡΟΣΩΡΙΝΟ) ---
st.divider()
st.subheader("🏆 Leaderboard Παρέας")
# Δείχνουμε έναν mock πίνακα βαθμολογίας για δοκιμή
leaderboard_data = {
    "Παίκτης": ["Γιάννης", "Μιχάλης", "Κώστας"],
    "Συνολικοί Πόντοι": [15, 12, 10],
}
st.table(pd.DataFrame(leaderboard_data))