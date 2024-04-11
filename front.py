import streamlit as st 
from streamlit_option_menu import option_menu
import dashboard, sentiment, session5


def uif():
    st.markdown("""
        <style>
            .block-container {
                padding-top: 2rem;
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
            section[data-testid="stSidebar"] {
                width: 270px !important; # Set the width to your desired value
            }
        </style>
        """, unsafe_allow_html=True)
        
    selected = option_menu(
        menu_title=None,
        options=["Dashboard page", "Sentiment page"], 
        icons=["graph-up", "emoji-smile"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal")
    
    if selected=="Dashboard page":
        dashboard.app()
        session5.updateORend("modal2","logout2")
        
    else:
        sentiment.app()
        session5.updateORend("modal3","logout3")
        

