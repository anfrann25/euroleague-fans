import streamlit as st

def render_login(users_sheet):
    st.subheader("🔑 Πύλη Σύνδεσης")
    tab_login, tab_signup = st.tabs(["Είσοδος", "Εγγραφή"])
    
    # --- TAB ΕΙΣΟΔΟΣ ---
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

    # --- TAB ΕΓΓΡΑΦΗ ---
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