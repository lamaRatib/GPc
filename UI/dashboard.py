import streamlit as st
import extra_streamlit_components as stx
import Database.db as db 
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import numpy as np
import UI.overviewSubpage as overviewSubpage 
from Business.visual import visuals


def app():

    # Tabs:
    chosen_id = stx.tab_bar(data=[
    stx.TabBarItemData(id="tab1", title="🌐 Overview",description=''),
    stx.TabBarItemData(id="tab2", title="💸 Performance",description=''),
    stx.TabBarItemData(id="tab3", title="📆 Sales Prediction",description='') ], default="tab1")
    st.markdown('<hr style="margin-top: -25px; margin-bottom: 0px;">', unsafe_allow_html=True)
    
    filter={}

    # Each tab has its own code:
    # Tab1: Overview:
    if chosen_id == "tab1":
        # Sidebar code which contains (sidebar func, slicers func):
        with st.sidebar:
            sidebar_top=visuals().sidebar_top()
            filter=visuals().slicers()
        # Visuals calling func:
        overviewSubpage.vis(filter)
    
    # Tab2: Performance:
    elif chosen_id == "tab2":
        # Sidebar code which contains (sidebar func, slicers func):
        with st.sidebar:
            sidebar_top=visuals().sidebar_top()
            filter=visuals().slicers()

        # Visuals calling func:


    # Tab3: Sales Prediction:
    else:
        # Loading sales over time data:
        sql = """
                SELECT DATE_FORMAT(date, '%Y-%m') AS month,
                    SUM(discounted_price) AS total_sales
                FROM sales
                GROUP BY DATE_FORMAT(date, '%Y-%m')
                ORDER BY DATE_FORMAT(date, '%Y-%m');
            """
        data = db.datab.query(sql) 
        df=pd.DataFrame(data,columns=['Date','total_sales'])
        df['Date'] = pd.to_datetime(df['Date'])
        df['Month'] = df['Date'].dt.month
        df['Year'] = df['Date'].dt.year
        x = df[['Month', 'Year']].values
        y = df['total_sales'].values

        # Scatter plot of original data:
        fig = px.scatter(df, x='Date', y='total_sales', title='Sales Over Time')
        fig.layout.xaxis.fixedrange = True
        fig.layout.yaxis.fixedrange = True
        config = {'displayModeBar': False,'dragMode':False}

        # Polynomial reg: Train data to get the modal:
        polynomial_features= PolynomialFeatures(degree=5)
        x_poly = polynomial_features.fit_transform(x)
        model = LinearRegression()
        model.fit(x_poly, y)

        # Line plot of regression line:
        y_poly_pred = model.predict(x_poly)
        fig=fig.add_scatter(x=df['Date'], y=y_poly_pred, mode='lines', name='Predicted line')

        # 2 Columns for plot fig and for prediction:
        col1,col2=st.columns([2,1],gap='large')

        # First column: Ploting:
        with col1:
            st.plotly_chart(fig,theme="streamlit",config=config,use_container_width=True)
        
        # Second column: Prediction:
        # Prediction box styling:
        month = {'Select a month': 0, 'Jan': 1, 'Feb': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 
                    'July': 7, 'Aug': 8, 'Sept': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
        month_num=[1,2,3,4,5,6,7,8,9,10,11,12]
        year= ['Select a year',2022,2023,2024,2025,2026,2027,2028,2029,2030]
        with col2:
            container2 = st.container(border=True,height=410)
            container2.subheader('Prediction:')
            container2.markdown('<hr style="margin-top: 0px; margin-bottom: 7px">', unsafe_allow_html=True)
            with container2:
                selected_month = st.selectbox('Select a month:', month)
                selected_year = st.selectbox('Select a year:',year)
                st.write('Predict Sales of selected date:')
                container2 = st.container(border=True,height=90)
                # If not chosen the result will be empty, else predict the sales upon selected Date(month and year):
                if selected_month=='Select a month' or selected_year=='Select a year':
                    container2.write('')
                else:
                    xpred=np.array([[month.get(selected_month),selected_year]])
                    inputted=polynomial_features.fit_transform(xpred)
                    pred = model.predict(inputted)
                    if pred[0]!=None:
                        formatted_pred = f"${pred[0] / 1000:.1f}K" if pred[0] >= 1000 else pred[0]
                        formatted_pred = f"${pred[0] / 1000000:.1f}M" if pred[0] >= 1000000 else formatted_pred
                    else:
                        formatted_pred="$0"
                    
                    container2.write(formatted_pred)
        


    
        
    
 