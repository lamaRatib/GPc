import streamlit as st 
from streamlit_option_menu import option_menu
import streamlit_authenticator as stauth
import db
import subprocess

st.set_page_config(page_title="Amazon Sales Dashboard", page_icon=":bar_chart:")

def run_login_script():
    result = subprocess.run(["python", "Authentication.py"], capture_output=True, text=True)
    return result.stdout

sql = "SELECT email,password,user_name FROM user"
data = db.DB().query(sql)
credentials = {"usernames": {}}
for user in data:
    uname, email, pwd = user[2], user[0], user[1]
    user_dict = {"name": uname, "password": pwd}
    credentials["usernames"].update({email: user_dict})

if 'authentication_status' not in st.session_state:
            st.session_state = {}

authenticator = stauth.Authenticate(
    credentials, "cookie_name", "random_key", cookie_expiry_days=1
)


name, authentication_status, username = authenticator.login("main")
if authentication_status == False:
    st.error("Email/password is incorrect")
elif authentication_status == None:
    st.warning("Please enter your email and password")
else:   
    st.markdown("""
        <style>
            .block-container {
                padding-top: 1rem;
                padding-bottom: 0rem;
                padding-left: 5rem;
                padding-right: 5rem;
            }
            .sidebar .sidebar-content {
                padding-top: 0px !important;
                padding-bottom: 0px !important;
            }
            .sidebar .stImage {
                margin-top: -10px !important;
                margin-bottom: -10px !important;
            }
        </style>
        """, unsafe_allow_html=True)

    with st.sidebar:
        st.image("AmazonLogo2.svg", use_column_width=True)
        st.markdown('<hr>', unsafe_allow_html=True)
        st.subheader(':level_slider: Slicers:')
        color_theme_list = ['blues', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
        selected_color_theme = st.selectbox('Select a color theme', color_theme_list)
       
            # Reset the session state to simulate logging out
        authenticator.logout()


    selected = option_menu(
        menu_title=None,
        options=["Dashboard page", "Sentiment page"], 
        icons=["graph-up", "emoji-smile"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal")



