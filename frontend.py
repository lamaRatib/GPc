import streamlit as st 
from streamlit_option_menu import option_menu
import mysql.connector
import streamlit_authenticator as stauth

st.set_page_config(page_title="Amazon Sales Dashboard", page_icon=":bar_chart:")

placeholder = st.empty()

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="0000",
    database="amazonsales"
)

cursor = conn.cursor()

# Fetch users from the database
query = "SELECT * FROM user"
cursor.execute(query)
users = cursor.fetchall()

credentials = {"usernames":{}}
        
for user in users:
    uname, email, pwd = user[1], user[2], user[3]
    user_dict = {"name": uname, "password": pwd}
    credentials["usernames"].update({email: user_dict})

authenticator = stauth.Authenticate(credentials, "cokkie_name", "random_key" , cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("main")

if authentication_status == False:
    st.error("Email/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your email and password")

if authentication_status:
    placeholder.empty()
    authenticator.logout("Logout", "sidebar")
    selected = option_menu(
        menu_title=None,
        options=[ "Dashboard page", "Sentiment page"], 
        icons=["graph-up", "emoji-smile"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal")
    
    with st.sidebar:
        st.title('🏂 Amazon Sales Dashboard') 
        color_theme_list = ['blues', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
        selected_color_theme = st.selectbox('Select a color theme', color_theme_list)
