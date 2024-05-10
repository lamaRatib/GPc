import streamlit as st 
import time
import threading
from front import uif
import session5 
from ui import login

# The first page that will be run by streamlit 

st.set_page_config(page_title="Amazon Sales Dashboard", page_icon=":bar_chart:",layout='wide')

# Intitialize the st.session_state:
if 'authentication_status' not in st.session_state:
    st.session_state={}
    st.session_state['authentication_status'] = False
    st.session_state['logged_out'] = True
    st.session_state['session_ends'] = True

st.markdown("""
            <style>
                section.main > div {max-width:60rem}
                
            </style>
            """, unsafe_allow_html=True)

placeholder = st.empty()

# If authentication_status is false that means its not logged in else means logged in successfuly 
if st.session_state['authentication_status']==False:
    # Login Form:
    with placeholder:
        info=login.login()
    
    # If inputted email and pass is correct then start session checking and display the main page:
    if info["email"] in info['credentials'] and info['credentials'][info["email"]]["password"] == info["password"]:
        placeholder.empty()
        st.session_state['authentication_status']=True
        st.session_state['logged_out']=False
        st.session_state['session_ends'] = False
        st.session_state['last_activity_time'] = time.time()
        activity_thread = threading.Thread(target=session5.check_activity)
        activity_thread.start()
        uif()
        
    # If none of them inputted then display warning massage:
    elif info["email"]==''and info["password"]=='':
        st.warning("Please enter your email and password")
    # Else where is the email or pass is wrong
    else:
        st.error("invalid email/password")
else:
    uif()
    
    
    
