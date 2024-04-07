import streamlit as st
from streamlit_option_menu import option_menu


def app():
    selected = option_menu(
        menu_title=None,
        options=[ "Dashboard page", "Sentiment page"], 
        icons=["graph-up", "emoji-smile"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal")
    with st.sidebar:
        st.title('🏂 US Population Dashboard') 
        color_theme_list = ['blues', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
        selected_color_theme = st.selectbox('Select a color theme', color_theme_list)
