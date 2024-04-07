import streamlit as st
from MultiApp import MultiApp
import dashboard, sentiment 
from streamlit_option_menu import option_menu


app = MultiApp()

st.markdown("""
# Multi-Page App

This multi-page app is using the [streamlit-multiapps](https://github.com/upraneelnihar/streamlit-multiapps) framework developed by [Praneel Nihar](https://medium.com/@u.praneel.nihar). Also check out his [Medium article](https://medium.com/@u.praneel.nihar/building-multi-page-web-app-using-streamlit-7a40d55fa5b4).

""")
selected = option_menu(
        menu_title=None,
        options=[ "Dashboard page", "Sentiment page"], 
        icons=["graph-up", "emoji-smile"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal")

# Add all your application here
app.add_app("Home", dashboard.app)
app.add_app("Data", sentiment.app)
# The main app
app.run()