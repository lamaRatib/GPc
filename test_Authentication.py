import pytest
import streamlit as st
from unittest.mock import patch  
import time

# Assuming login.py returns a dictionary with email, password, and credentials
def mock_login(data):
    credentials = {"user1@example.com": {"name": "John Doe", "password": "password123"}}
    return {"email": data["email"], "password": data["password"], "credentials": credentials}

def setUp():
    # Reset session state before test
    st.session_state = {}
    st.session_state['authentication_status']=False
    st.session_state['session_ends'] = True
    st.session_state['logged_out']= True

def mock_uif():
    return None

def mock_Authentication(info):
    if st.session_state['authentication_status']==False:
   
        # If inputted email and pass is correct then start session checking and display the main page:
        if info["email"] in info['credentials'] and info['credentials'][info["email"]]["password"] == info["password"]:
            st.session_state['authentication_status']=True
            st.session_state['logged_out']=False
            st.session_state['session_ends'] = False
            st.session_state['last_activity_time'] = time.time()
            mock_uif()
            return "uif"
            
        # If none of them inputted then display warning massage:
        elif info["email"]==''and info["password"]=='':
            return "Please enter your email and password"
        # Else where is the email or pass is wrong
        else:
            return "invalid email/password"
    else:
        mock_uif()
        return "uif"
        
        

def test_successful_login():
    setUp()
    data={}
    data["email"] =  "user1@example.com"
    data["password"] = "password123"
    
    info= mock_login(data)
    result= mock_Authentication(info)

    # Assertions 
    assert result is "uif"
    assert st.session_state["authentication_status"] is True
    assert st.session_state["logged_out"] is False


def test_unsuccessful_login():
    setUp()
    data={}
    data["email"] =  "user1@example.com"
    data["password"] = "password"
    
    info= mock_login(data)
    result= mock_Authentication(info)

    # Assertions 
    assert result is "invalid email/password"
    assert st.session_state["authentication_status"] is False
    assert st.session_state["logged_out"] is True

def test_no_input_login():
    setUp()
    data={}
    data["email"] =  ""
    data["password"] = ""
    
    info= mock_login(data)
    result= mock_Authentication(info)

    # Assertions 
    assert result is "Please enter your email and password"
    assert st.session_state["authentication_status"] is False
    assert st.session_state["logged_out"] is True


if __name__ == '__main__':
    pytest.main()