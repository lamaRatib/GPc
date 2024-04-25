import streamlit as st
from sidbar import visuals


def app():
    filter={}
    # Sidebar code which contains (sidebar func, slicers func):
    with st.sidebar:
        sidebar_top=visuals().sidebar_top()
        filter=visuals().slicers()
    
    # Sentiment Analysis code:
    st.title('Sentiment')