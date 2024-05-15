import streamlit as st
from sidbar import visuals
import database.db as db
from vaderanalysis import vaderanalysis
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def app():
    filter={}
    # Sidebar code which contains (sidebar func, slicers func):
    with st.sidebar:
        sidebar_top=visuals().sidebar_top()
        filter=visuals().slicers()
    
    # Sentiment Analysis code:
    st.subheader("Stored Customer Reviews ")
    option1_selected = st.radio("Choose an option", ["Stored Customer Reviews","Input a Review"], index=0)
    if option1_selected == "Stored Customer Reviews":
        vaderanalysis(filter,txt=False)
    elif option1_selected == "Input a Review":
        txt=st.text_input(label='Write a Review')
        vaderanalysis(filter,txt)