import streamlit as st
import pytest
from unittest.mock import patch  
import time


def mock_updateORend(key1, key2):
    """
        This mock function simulates the logic within updateORend for testing purposes.
    """

    if st.session_state['session_ends']:
        st.session_state['authentication_status'] = False
        st.session_state['logged_out'] = True
    else:
        st.session_state['last_activity_time'] = time.time()


def mock_check_activity():
    """
        This mock function simulates the behavior of check_activity for testing purposes.
    """

    elapsed_time = time.time() - st.session_state['last_activity_time']
    if elapsed_time > 300:
        st.session_state['session_ends'] = True
    return



def setUp():
    # Reset session state before test
    st.session_state = {}
    st.session_state['authentication_status']=True
    st.session_state['session_ends'] = False


def test_session_timeout():
    setUp()
    st.session_state['last_activity_time'] = time.time() - 309 

    with patch('session5.check_activity', mock_check_activity()):
        mock_updateORend("test_key1", "test_key2")

    assert st.session_state['session_ends'] == True, "Session should be marked as ended after inactivity"
    assert st.session_state['authentication_status'] == False, "User should be logged out"


def test_session_not_timed_out():
    setUp()
    st.session_state['last_activity_time'] = time.time() - 60 

    with patch('session5.check_activity', mock_check_activity()):
        mock_updateORend("test_key1", "test_key2")

    assert st.session_state['session_ends'] == False, "Session should not be timed out with recent activity"
    assert st.session_state['authentication_status'] == True, "User should be logged in"


if __name__ == '__main__':
    pytest.main()