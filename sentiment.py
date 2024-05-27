import streamlit as st
from sidbar import visuals
import session5
from vaderanalysis import vaderanalysis
import plotly.graph_objects as go


def app():
    filter={}
    col=st.columns([3.5,3],gap='small')

    # Sentiment Analysis code:
    with col[0]:
        with st.container(border=True, height=120):
            option1_selected = st.radio("Choose an option:", ["Stored Customer Reviews","Personalized Review"], index=0)
        
        if option1_selected == "Stored Customer Reviews":

            # Sidebar code which contains (sidebar func, slicers func):
            with st.sidebar:
                sidebar_top=visuals().sidebar_top()
                filter=visuals().slicers()
            
            session5.updateORend("modal4","logout4")
            value, name, par= vaderanalysis(filter,txt=False)[0], vaderanalysis(filter,txt=False)[1], vaderanalysis(filter,txt=False)[2]
            st.write('')
            st.write('')
            st.write('')
            with st.container(border=True):
                st.write('The result of sentiment analysis is: '+ name)

            visuals().toastNotificate(par,filter)
         
        elif option1_selected == "Personalized Review":
            session5.updateORend("modal5","logout5")
            st.markdown("""
            <style>
            .element-container:has(>.stTextArea), .stTextArea { width: 475px !important;}
            .stTextArea textarea { height: 60px !important; }
            </style> """, unsafe_allow_html=True)
            
            cont= st.container(border=True)
            with cont:
                txt=st.text_area(label='Write a Review')
            value, name= vaderanalysis(filter,txt)[0], vaderanalysis(filter,txt)[1]
            cont.write('The result of sentiment analysis is: '+ name)

            
    with col[1]:
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = value,
            domain = {'x': [0.2, 0.9], 'y': [0.9, .56]},
            title = {'text': "Sentiment Gauge"},
            gauge = {
                'axis': {'range': [-1, 1]},
                'bar': {'color': "black"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps' : [
                    {'range': [-1, -0.05], 'color': "red", 'name': "Negative"},
                    {'range': [-0.05, 0.05], 'color': "orange", 'name': "Neutral"},
                    {'range': [0.05, 1], 'color': "green", 'name': "Positive"}
                ],
                'threshold' : {
                    'line': {'color': "black", 'width': 5},
                    'thickness': 0.75,
                    'value': value
                },
                
            }
        ))        

        fig.layout.xaxis.fixedrange = True
        fig.layout.yaxis.fixedrange = True 
        config = {'displayModeBar': False,'dragMode':False}
        st.plotly_chart(fig,config=config,use_container_width=True)
            
        
