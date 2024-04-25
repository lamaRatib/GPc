import streamlit as st
import db 
import pandas as pd
import plotly.express as px



def performance(filter): 
    col1, col2, col3, col4 = st.columns(4)