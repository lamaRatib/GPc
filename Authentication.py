import streamlit as st 
import streamlit_authenticator as stauth
import db


class Authen:
    def __init__(self):
        self.placeholder = st.empty()
        self.db = db.DB()
        self.credentials = self._fetch_credentials()
        self.authenticator=None

    def _fetch_credentials(self):
        sql = "SELECT email,password,user_name FROM user"
        data = self.db.query(sql)
        credentials = {"usernames": {}}
        for user in data:
            uname, email, pwd = user[2], user[0], user[1]
            user_dict = {"name": uname, "password": pwd}
            credentials["usernames"].update({email: user_dict})
        return credentials
    
    def authenticate(self):
        if 'authentication_status' not in st.session_state:
            st.session_state = {}
        self.placeholder.empty()
        self.authenticator = stauth.Authenticate(
            self.credentials, "cookie_name", "random_key", cookie_expiry_days=1
        )
        name, authentication_status, username = self.authenticator.login("main")
        
        if authentication_status == False:
            st.error("Email/password is incorrect")
        elif authentication_status == None:
            st.warning("Please enter your email and password")
        else:
            self.placeholder.empty()

    
    def logout(self):
        self.authenticator.logout()
        self.placeholder.empty()
        self.sidebarholder.empty()

        

    