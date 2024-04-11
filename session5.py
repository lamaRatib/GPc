import streamlit as st 
from streamlit_modal import Modal
import time

def check_activity():
    while st.session_state['authentication_status']:
        elapsed_time = time.time() - st.session_state['last_activity_time']
        # If more than 20 seconds have elapsed, log out the user
        st.write(elapsed_time)
        if elapsed_time > 20:
            st.warning("You have been logged out due to inactivity.")
            st.session_state['session_ends'] = True
            return
        time.sleep(5)  


def updateORend():
    if st.session_state['session_ends']:
        modal = Modal("Warning", key="demo-modal",padding=60,max_width=500)
        with modal.container():
                    st.write('You have been 5 mins without activity, login again please...')
                    col1, col2, col3 = st.columns([1, 4, 1.2])
                    with col3:
                        if st.button("Logout",key="logout-modal"):    
                            st.session_state['authentication_status'] = False
                            st.session_state['logged_out']=True
                            st.experimental_rerun()
    else:
        st.session_state['last_activity_time'] = time.time()
