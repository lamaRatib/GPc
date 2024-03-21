import streamlit as st 
from streamlit_option_menu import option_menu
import mysql.connector
import time

# Function to authenticate user
def authenticate(email, password):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="0000",
        database="amazonsales"
    )
    cursor = conn.cursor()

    # Check if user exists in the database
    query = "SELECT * FROM user WHERE email = %s AND password = %s"
    cursor.execute(query, (email, password))
    user = cursor.fetchone()

    if user:
        return True
    else:
        return False

# Login page
def login_page():
    st.write("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate(email, password):
            st.success("Login successful")
            st.session_state.logged_in = True
            st.session_state.last_activity_time = time.time()
            st.session_state.remember_me = True
        else:
            st.error("Invalid username or password")

# Dashboard page
def dashboard():
    selected = option_menu(
        menu_title=None,
        options=[ "Dashboard page", "Sentiment page"], 
        icons=["graph-up", "emoji-smile"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal")
    with st.sidebar:
        st.title('🏂 US Population Dashboard') 
        color_theme_list = ['blues', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
        selected_color_theme = st.selectbox('Select a color theme', color_theme_list)

# Function to check for session timeout
def check_session_timeout():
    if st.session_state.logged_in:
        current_time = time.time()
        last_activity_time = st.session_state.get("last_activity_time", current_time)
        if current_time - last_activity_time > 300:  
            st.session_state.logged_in = False
            st.session_state.remember_me = False
            st.error("Session timed out. Please log in again.")
            st.experimental_rerun()

def main():
    if not st.session_state.get("logged_in", False):
        login_page()
    else:
        dashboard()
        check_session_timeout()  

if __name__ == "__main__":
    main()
