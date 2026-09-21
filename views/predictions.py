import streamlit as st
import pandas as pd
from datetime import datetime

@st.cache_data
def load_schedule():
    try:
        df = pd.read_excel("data/Euroleague_Perfect_Schedule.xlsx")
        return df
    except Exception as e:
        st.error(f"Δεν βρέθηκε το αρχείο Excel. Σφάλμα: {e}")
        return pd.DataFrame()

def render_predictions(preds_sheet, username):
    st.subheader("🎯 Οι Προβλέψεις μου")
    
    df = load_schedule()
    
    if df.empty:
        st.warning("Βεβαιώσου ότι το αρχείο 'Euroleague_Perfect_Schedule.xlsx' βρίσκεται στον φάκελο 'data'.")
        return

    round_col = df.columns[0]
    home_col = df.columns[1]
    away_col = df.columns[2]

    rounds = df[round_col].unique().tolist()
    selected_round = st.selectbox("Επίλεξε Αγωνιστική", rounds)

    # 1. Παίρνουμε ΟΛΕΣ τις εγγραφές από το Google Sheet
    try:
        all_preds = preds_sheet.get_all_records()
    except Exception:
        all_preds = []

    # 2. Φιλτράρουμε για τον χρήστη και την αγωνιστική
    user_round_preds = [
        p for p in all_preds 
        if str(p.get("Username", "")).strip() == str(username).strip() 
        and str(p.get("Round", "")).strip() == str(selected_round).strip()
    ]

    edit_key = f"edit_{selected_round}"
    if edit_key not in st.session_state:
        st.session_state[edit_key] = False

    # ΑΝ ΥΠΑΡΧΟΥΝ ΗΔΗ ΠΡΟΒΛΕΨΕΙΣ ΚΑΙ ΔΕΝ ΕΧΕΙ ΠΑΤΗΣΕΙ "ΑΛΛΑΓΗ"
    if user_round_preds and not st.session_state[edit_key]:
        st.success(f"✅ Έχεις ήδη υποβάλλει τις προβλέψεις σου για την **{selected_round}**!")
        st.info("Δεν μπορείς να κάνεις νέα υποβολή για αυτή την αγωνιστική. Οι προβλέψεις σου:")
        
        for p in user_round_preds:
            game_name = p.get('Game') or p.get('game')
            winner_name = p.get('Prediction') or p.get('predicted winner') or p.get('Winner')
            st.markdown(f"• **{game_name}** ➔ Νικητής: *{winner_name}*")
        
        st.write("")
        if st.button("🔄 Θέλετε να γίνουν αλλαγές;", type="secondary"):
            st.session_state[edit_key] = True
            st.rerun()
            
        return

    # ΑΝ ΘΕΛΕΙ ΝΑ ΚΑΝΕΙ ΑΛΛΑΓΗ Ή ΔΕΝ ΥΠΑΡΧΟΥΝ ΠΡΟΒΛΕΨΕΙΣ
    if st.session_state[edit_key]:
        st.info("✏️ Λειτουργία Τροποποίησης: Επεξεργαστείτε τις επιλογές σας και πατήστε αποθήκευση.")
    
    round_games = df[df[round_col] == selected_round]
    st.markdown(f"### Αγώνες: {selected_round}")
    
    with st.form("predictions_form"):
        predictions = {}
        
        for index, row in round_games.iterrows():
            home_team = str(row[home_col])
            away_team = str(row[away_col])
            game_str = f"{home_team} - {away_team}"
            
            default_index = 0
            if user_round_preds:
                existing_p = next((p for p in user_round_preds if str(p.get("Game") or p.get("game")) == game_str), None)
                if existing_p:
                    saved_winner = str(existing_p.get("Prediction") or existing_p.get("predicted winner") or existing_p.get("Winner"))
                    if saved_winner == away_team:
                        default_index = 1

            predicted_winner = st.radio(
                f"**{game_str}**", 
                [home_team, away_team], 
                index=default_index,
                key=f"win_{index}", 
                horizontal=True
            )
            predictions[game_str] = predicted_winner
            
        st.markdown("---")
        submitted = st.form_submit_button("Αποθήκευση Προβλέψεων", type="primary", use_container_width=True)

        if submitted:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            try:
                if user_round_preds:
                    cell_list = preds_sheet.get_all_records()
                    rows_to_delete = []
                    # Διόρθωση: Αφαιρέθηκε το σχόλιο από την παρένθεση
                    for idx, row in enumerate(cell_list, start=2):
                        if str(row.get("Username", "")).strip() == str(username).strip() and str(row.get("Round", "")).strip() == str(selected_round).strip():
                            rows_to_delete.append(idx)
                    
                    for r_idx in sorted(rows_to_delete, reverse=True):
                        preds_sheet.delete_rows(r_idx)

                rows_to_add = []
                for game, winner in predictions.items():
                    rows_to_add.append([timestamp, username, str(selected_round), game, winner])
                
                preds_sheet.append_rows(rows_to_add)
                
                st.session_state[edit_key] = False
                st.success("Οι προβλέψεις σας αποθηκεύτηκαν επιτυχώς! 🍀")
                st.rerun()
                
            except Exception as e:
                st.error(f"Σφάλμα κατά την αποθήκευση: {e}")