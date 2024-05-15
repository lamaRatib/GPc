import streamlit as st 
import database.db as db

def login():
    sql = "SELECT email,password,user_name FROM user"
    data = db.datab.query(sql)
    credentials = {}
    for user in data:
        email, password, uname = user[0], user[1], user[2]
        credentials[email] = {"name": uname, "password": password}

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

    info={'email': email, 'password': password, 'credentials': credentials}
    
    return info

