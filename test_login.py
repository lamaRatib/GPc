import pytest
from unittest.mock import patch
import streamlit as st

def mock_login(data):
    """
    Mocked login function that returns expected credentials.

    Args:
        data (dict): Login data containing email and password.

    Returns:
        dict: Dictionary with email, password, and credentials (mocked).
    """
    credentials = {"user1@example.com": {"name": "John Doe", "password": "password123"}}
    return {"email": data["email"], "password": data["password"], "credentials": credentials}

def login():
    """
    Login function with mocked login flow.

    Returns:
        dict: Login information (email, password, credentials).
    """
    data={}
    data["email"] =  "user1@example.com"
    data["password"] = "password"
    placeholder = st.empty()
    st.markdown("""
        <style>
            section.main > div {max-width:60rem}
        </style>
    """, unsafe_allow_html=True)

    # Simulate login flow using mocked data
    info = mock_login(data)

    # Login form (replace with your actual form logic)
    if st.session_state['authentication_status'] == False:
        with placeholder.form("login"):
            st.header("Login")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")

    return info

# Test functions
@pytest.mark.parametrize("email, password, expected_message", [
    ("", "", ""),  # Test for empty email and password (no warning message)
    ("user1@example.com", "wrong_password", "Invalid email/password"),
    ("user1@example.com", "password123", None),  # Test for successful login (no error message)
])
def test_login_form(email, password, expected_message):
    """
    Test for login form with various inputs.

    Args:
        email (str): Email input value.
        password (str): Password input value.
        expected_message (str): Expected error message (None for successful login).
    """

    with patch("your_app.login", mock_login):
        # Simulate login flow
        login()

        # Simulate form submission
        st.session_state['authentication_status'] = False  # Reset authentication status
        email_element = st.empty().text_input("Email", value=email)
        password_element = st.empty().text_input("Password", type="password", value=password)
        st.empty().form_submit_button("Login").click()

        # Assert error message (if expected)
        if expected_message:
            assert expected_message in st.text
        else:
            # Assert absence of warning message (for empty email/password)
            assert "Please enter your email and password" not in st.text

# Simulate app execution (replace with your main app logic)
if __name__ == "__main__":
    pytest.main()
