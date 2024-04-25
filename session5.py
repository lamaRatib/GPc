import streamlit as st 
from streamlit_modal import Modal
import time

def check_activity():
    """  
        Each time sleep (2mins) it test if the last activity time and current time 
        if more than 5min should st.session_state['session_ends'] = True
        else sleep and check again untill it log out by himself

    """
    while st.session_state['authentication_status']:
        elapsed_time = time.time() - st.session_state['last_activity_time']
        if elapsed_time > 20000:
            st.session_state['session_ends'] = True
            return
        time.sleep(5)  


def updateORend(key1,key2):
    """
        This func is added to whereever there is a click or activity on the page so 
        if the session_ends false then popup warning massage to logout 
        else update the last activity time
    """
    if st.session_state['session_ends']:
        modal = Modal("Warning", key=key1,padding=60,max_width=500)
        with modal.container():
                    st.write('You have been 5 mins or more without activity, login again please...')
                    col1, col2, col3 = st.columns([1, 4, 1.2])
                    with col3:
                        if st.button("Logout",key=key2):    
                            st.session_state['authentication_status'] = False
                            st.session_state['logged_out']=True
                            st.rerun()
    else:
        st.session_state['last_activity_time'] = time.time()
