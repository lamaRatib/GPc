import streamlit as st 
from streamlit_option_menu import option_menu
import mysql.connector
import streamlit_authenticator as stauth
import hydralit_components as hc


st.set_page_config(page_title="Amazon Sales Dashboard", page_icon=":bar_chart:",)

placeholder = st.empty()

@st.cache_resource
def init_connection():
    host = "localhost"
    database = "amazonsales"
    user = "root"
    password = "0000"
    return mysql.connector.connect(host=host, database=database, user=user, password=password)

conn = init_connection()
cursor = conn.cursor()

query = "SELECT * FROM user"
cursor.execute(query)
users = cursor.fetchall()

credentials = {"usernames":{}}

for user in users:
    uname, email, pwd = user[1], user[2], user[3]
    user_dict = {"name": uname, "password": pwd}
    credentials["usernames"].update({email: user_dict})


authenticator = stauth.Authenticate(credentials, "cokkie_name", "random_key" , cookie_expiry_days=1)

name, authentication_status, username = authenticator.login("main")

if authentication_status == False:
    st.error("Email/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your email and password")

if authentication_status:
    
    menu_data = [
        {'icon': "far fa-copy", 'label':"Left End"},
        {'id':'Copy','icon':"🐙",'label':"Copy"},
        {'icon': "fa-solid fa-radar",'label':"Dropdown1", 'submenu':[{'id':' subid11','icon': "fa fa-paperclip", 'label':"Sub-item 1"},{'id':'subid12','icon': "💀", 'label':"Sub-item 2"},{'id':'subid13','icon': "fa fa-database", 'label':"Sub-item 3"}]},
        {'icon': "far fa-chart-bar", 'label':"Chart"},#no tooltip message
        {'id':' Crazy return value 💀','icon': "💀", 'label':"Calendar"},
        {'icon': "fas fa-tachometer-alt", 'label':"Dashboard",'ttip':"I'm the Dashboard tooltip!"}, #can add a tooltip message
        {'icon': "far fa-copy", 'label':"Right End"},
        {'icon': "fa-solid fa-radar",'label':"Dropdown2", 'submenu':[{'label':"Sub-item 1", 'icon': "fa fa-meh"},{'label':"Sub-item 2"},{'icon':'🙉','label':"Sub-item 3",}]},
    ]

    over_theme = {'txc_inactive': '#FFFFFF'}
    menu_id = hc.nav_bar(
        menu_definition=menu_data,
        override_theme=over_theme,
        home_name='Home',
        login_name='Logout',
        hide_streamlit_markers=False, #will show the st hamburger as well as the navbar now!
        sticky_nav=True, #at the top or not
        sticky_mode='pinned', #jumpy or not-jumpy, but sticky or pinned
    )

    with st.sidebar:
        authenticator.logout("Logout", "sidebar")
        st.title('🏂 Amazon Sales Dashboard') 
        color_theme_list = ['blues', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
        selected_color_theme = st.selectbox('Select a color theme', color_theme_list)

    selected = option_menu(
        menu_title=None,
        options=[ "Dashboard page", "Sentiment page"], 
        icons=["graph-up", "emoji-smile"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal")
    
    
    if selected == "Dashboard page":
        st.title(f"You have selected {selected}")
    if selected == "Sentiment page":
        st.title(f"You have selected {selected}")
   
    
conn.close() 