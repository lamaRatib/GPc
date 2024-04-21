import streamlit as st
import extra_streamlit_components as stx
import session5
from db import DB
import pandas as pd
import plotly.express as px
import datetime

def visuals(filter): 
    col1, col2, col3, col4 = st.columns(4)
    
    # Card1: Total Sales:
    total_sales = DB().query("SELECT SUM(discounted_price) AS total_amount FROM sales; ")
    card1= [row[0] for row in total_sales ]
    formatted_sales = f"${card1[0] / 1000000:.1f}M" if card1[0] >= 1000000 else card1[0]
    col1.metric(value=formatted_sales,label="Total Sales")

    # Card2: Average Rating (rounded to two decimal positions)
    average_rating = DB().query("SELECT AVG(rating) FROM review; ")
    card2= [row[0] for row in average_rating ]
    col2.metric(value=round(card2[0], 2),label="Average Rating")

    # Card3: Number of Products Sold
    num_products_sold =  DB().query("SELECT Sum(quantity) FROM sales;")
    card3=[row[0] for row in num_products_sold ]
    formatted_sales = f"{card3[0] / 1000:.1f}K" if card3[0] >= 1000 else card3[0]
    col3.metric(value=formatted_sales,label="Number of Products Sold" )

    # Card4: Number of Customers
    num_customers = DB().query("SELECT Count(DISTINCT customer_id) FROM sales;")
    card4=[row[0] for row in num_customers]
    col4.metric(value=int(card4[0]),label="Number of Customers")


   

def slicers():
    # Date Slicer
    min_date = DB().query("SELECT MIN(date) FROM sales;")
    max_date = DB().query("SELECT MAX(date) FROM sales;")
    mindate = [row[0] for row in min_date]
    maxdate = [row[0] for row in max_date]
    selected_start_date = st.date_input("Select Start Date:", min_value=mindate[0], max_value=maxdate[0], value=mindate[0])
    selected_end_date = st.date_input("Select End Date:", min_value=mindate[0], max_value=maxdate[0], value=maxdate[0])

    # Category Slicer
    category=DB().query("SELECT DISTINCT category FROM products;")
    category_list = [row[0] for row in category]
    selected_category = st.selectbox("Select Category:",['All'] +category_list, key='category_selectbox')

    # Sub-Category Slicer
    subcategory=DB().query("SELECT DISTINCT sub_category FROM products;")
    subcategory_list = [row[0] for row in subcategory]
    if selected_category!='All':
        subcategory=DB().query("SELECT DISTINCT sub_category FROM products WHERE category=\""+selected_category+"\";")
        subcategory_list = [row[0] for row in subcategory]
    selected_subcategory = st.selectbox("Select Sub-Category:", ['All'] + subcategory_list, key='subcategory_selectbox')

    # Product Slicer
    product=DB().query("SELECT DISTINCT product_name FROM products;")
    product_list = [row[0] for row in product]
    if selected_category!='All':
        product=DB().query("SELECT DISTINCT product_name FROM products WHERE category=\""+selected_category+"\";")
        product_list = [row[0] for row in product]
    if selected_subcategory!='All':
        product=DB().query("SELECT DISTINCT product_name FROM products WHERE sub_category=\""+selected_subcategory+"\";")
        product_list = [row[0] for row in product]
    selected_product = st.selectbox("Select Product:", ['All'] + product_list, key='product_selectbox')

    # City Slicer
    city=DB().query("SELECT DISTINCT city FROM customer;")
    city_list = [row[0] for row in city]
    if selected_category!='All':
        city=DB().query("""SELECT DISTINCT city FROM customer AS c 
                            JOIN sales AS s ON s.customer_id = c.customer_id 
                            JOIN products AS p ON s.product_id = p.product_id WHERE p.category =\""""+selected_category+"\";")
        city_list = [row[0] for row in city]
    if selected_subcategory!='All':
        city=DB().query("""SELECT DISTINCT city FROM customer AS c
                            JOIN sales AS s ON s.customer_id = c.customer_id 
                            JOIN products AS p ON s.product_id = p.product_id WHERE p.sub_category=\""""+selected_subcategory+"\";")
        city_list = [row[0] for row in city]
    if selected_product!='All':
        city=DB().query("""SELECT DISTINCT city FROM customer AS c 
                            JOIN sales AS s ON s.customer_id = c.customer_id 
                            JOIN products AS p ON s.product_id = p.product_id WHERE p.product_name=\""""+selected_product+"\";")
        city_list = [row[0] for row in city]
    selected_city = st.selectbox("Select City:", ['All'] + city_list, key='city_selectbox')

    # Rating Slicer
    selected_min_rating = st.sidebar.slider("Select Minimum Rating:", min_value=0.0, max_value=5.0, step=0.1, value=0.0)
    if selected_min_rating!=5.0:
        selected_max_rating = st.sidebar.slider("Select Maximum Rating:", min_value=selected_min_rating, max_value=5.0, step=0.1, value=5.0)
    else:
        selected_max_rating=5.0 
        
    selected={"selected_start_date":selected_start_date,"selected_end_date":selected_end_date,
              "selected_category":selected_category,"selected_subcategory":selected_subcategory,
              "selected_product":selected_product,"selected_min_rating":selected_min_rating,"selected_max_rating":selected_max_rating}
    
    return selected


    

def app():
    
    chosen_id = stx.tab_bar(data=[
    stx.TabBarItemData(id="tab1", title="🌐 Overview",description=''),
    stx.TabBarItemData(id="tab2", title="💸 Performance",description=''),
    stx.TabBarItemData(id="tab3", title="📆 Sales Prediction",description='') ], default="tab1")
    st.markdown('<hr style="margin-top: 5px;">', unsafe_allow_html=True)
    
    filter={}

    if chosen_id == "tab1":
        visuals(filter)
        with st.sidebar:
            container3 = st.container(border=True,height=70)
            with container3:
                col = st.columns([3.5, 3], gap="medium")
                with col[0]:
                    st.image("AmazonLogo2.svg", width=90)
                with col[1]:
                    if st.button('logout',key="logout-original"):
                        st.session_state['authentication_status'] = False
                        st.session_state['logged_out'] = True
                        st.session_state['session_ends'] = False
                        st.rerun()
        
            
            st.markdown('<hr style="margin-top: 5px; margin-bottom: 7px">', unsafe_allow_html=True)
            st.subheader(':level_slider: Slicers:')
            filter=slicers()
        
    elif chosen_id == "tab2":
        st.write("lkjhgfx")
        with st.sidebar:
            container3 = st.container(border=True,height=70)
            with container3:
                col = st.columns([3.5, 3], gap="medium")
                with col[0]:
                    st.image("AmazonLogo2.svg", width=90)
                with col[1]:
                    if st.button('logout',key="logout-original"):
                        st.session_state['authentication_status'] = False
                        st.session_state['logged_out'] = True
                        st.session_state['session_ends'] = False
                        st.rerun()
        
            
            st.markdown('<hr style="margin-top: 5px; margin-bottom: 7px">', unsafe_allow_html=True)
            st.subheader(':level_slider: Slicers:')
            filter=slicers()
    else:
        sql = """
                SELECT DATE_FORMAT(date, '%Y-%m') AS month,
                    SUM(discounted_price) AS total_sales
                FROM sales
                GROUP BY DATE_FORMAT(date, '%Y-%m')
                ORDER BY DATE_FORMAT(date, '%Y-%m');
            """
        data = DB().query(sql) 
        df=pd.DataFrame(data,columns=['Date','Total Sales'])
        fig = px.scatter(df, x='Date', y='Total Sales', 
                 title='Sales Over Time')
        fig.layout.xaxis.fixedrange = True
        fig.layout.yaxis.fixedrange = True
        config = {'displayModeBar': False,'dragMode':False}

        col1,col2=st.columns([2,1],gap='large')
        with col1:
            st.plotly_chart(fig,theme="streamlit",config=config,use_container_width=True)
        
        month = ['Select a month','Jan', 'Feb', 'March', 'April', 'May', 'June','July','Aug','Sept','Oct','Nov','Dec']
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
                if selected_month=='Select a month' or selected_year=='Select a year':
                    container2.write('')
                else:
                    container2.write('kjhg')
        


    
        
    
 