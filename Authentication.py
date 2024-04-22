import streamlit as st 
from streamlit_modal import Modal
import time
import threading
import db
from front import uif
import session5

# The first page that will be run by streamlit 

st.set_page_config(page_title="Amazon Sales Dashboard", page_icon=":bar_chart:",layout='wide')

# Intitialize the st.session_state:
if 'authentication_status' not in st.session_state:
    st.session_state={}
    st.session_state['authentication_status'] = False
    st.session_state['logged_out'] = True
    st.session_state['session_ends'] = True

# Load credentials from the database
sql = "SELECT email,password,user_name FROM user"
data = db.DB().query(sql)
credentials = {"usernames": {}}
for user in data:
    email, password, uname = user[0], user[1], user[2]
    credentials["usernames"][email] = {"name": uname, "password": password}


placeholder = st.empty()

st.markdown("""
        <style>
            section.main > div {max-width:60rem}
            
        </style>
        """, unsafe_allow_html=True)

# If authentication_status is false that means its not logged in else means logged in successfuly 
if st.session_state['authentication_status']==False:
    # Login Form:
    with placeholder.form("login") :
        st.header("Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
    
    # If inputted email and pass is correct then start session checking and display the main page:
    if email in credentials["usernames"] and credentials["usernames"][email]["password"] == password:
        placeholder.empty()
        st.session_state['authentication_status']=True
        st.session_state['logged_out']=False
        st.session_state['session_ends'] = False
        st.session_state['last_activity_time'] = time.time()
        activity_thread = threading.Thread(target=session5.check_activity)
        activity_thread.start()
        uif()
        
    # If none of them inputted then display warning massage:
    elif email==''and password=='':
        st.warning("Please enter your email and password")
    # Else where is the email or pass is wrong
    else:
        st.error("invalid email/password")
else:
    uif()
    
    
    
