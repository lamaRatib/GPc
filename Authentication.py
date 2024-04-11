import streamlit as st 
from streamlit_modal import Modal
import time
import threading
import db
from front import uif
import session5




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

# Initialize login form
placeholder = st.empty()

if st.session_state['authentication_status']==False:

    with placeholder.form("login"):
        st.header("Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
    if email in credentials["usernames"] and credentials["usernames"][email]["password"] == password:
        placeholder.empty()
        st.session_state['authentication_status']=True
        st.session_state['logged_out']=False
        st.session_state['session_ends'] = False
        st.session_state['last_activity_time'] = time.time()
        activity_thread = threading.Thread(target=session5.check_activity)
        activity_thread.start()
        uif()
        
        
    elif email==''and password=='':
        st.warning("Please enter your email and password")
    else:
        st.error("invalid email/password")
else:
    uif()
    session5.updateORend()
    
    
