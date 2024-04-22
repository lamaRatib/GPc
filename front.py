import streamlit as st 
from streamlit_option_menu import option_menu
import dashboard, sentiment, session5


def uif():
    """
        This func is for display the main page after login successfuly
    """

    # Appling CSS styling on streamlit page
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
            section[data-testid="stSidebar"] {
                width: 270px !important; # Set the width to your desired value
            }
            section.main > div {max-width:70rem}
                
            button[title="View fullscreen"]{visibility: hidden;}

        </style>
        """, unsafe_allow_html=True)
    
    # Navigation menu of 2 pages:
    selected = option_menu(
        menu_title=None,
        options=["Dashboard page", "Sentiment page"], 
        icons=["graph-up", "emoji-smile"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal")
    
    # If selected first page display the app func of selected page and update the last activity time
    if selected=="Dashboard page":
        dashboard.app()
        session5.updateORend("modal2","logout2")
        
    elif selected=="Sentiment page":
        sentiment.app()
        session5.updateORend("modal3","logout3")
        

