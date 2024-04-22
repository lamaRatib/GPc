import streamlit as st
import extra_streamlit_components as stx
import session5
from db import DB
import pandas as pd
import plotly.express as px
import datetime
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression


def visuals(filter): 
    col1, col2, col3, col4 = st.columns(4)
    
    # Card1: Total Sales with applying related filter if exist:
    selected_start_date = filter.get('selected_start_date').strftime('%Y-%m-%d')
    selected_end_date = filter.get('selected_end_date').strftime('%Y-%m-%d')
    where_conditions = []
    if filter.get('selected_category') != 'All':
        where_conditions.append(f"p.category = '{filter.get('selected_category')}'")

    if filter.get('selected_subcategory') != 'All':
        where_conditions.append(f"p.sub_category = '{filter.get('selected_subcategory')}'")

    if filter.get('selected_product') != 'All':
        where_conditions.append(f"p.product_id = '{filter.get('selected_product')}'")

    if filter.get('selected_min_rating') and filter.get('selected_max_rating'):
        where_conditions.append(f"r.rating >= {filter.get('selected_min_rating')} AND r.rating <= {filter.get('selected_max_rating')}")

    where_clause = " AND ".join(where_conditions)
    sql = f"""
        SELECT SUM(s.discounted_price) AS total_amount 
        FROM sales AS s
        JOIN products AS p ON s.product_id = p.product_id
        JOIN review AS r ON s.product_id = r.product_id
        WHERE s.date >= '{selected_start_date}' AND s.date <= '{selected_end_date}'
        {'AND ' + where_clause if where_clause else ''}
    """
    total_sales = DB().query(sql)
    card1 = [row[0] for row in total_sales]
    if card1[0]!=None:
        formatted_sales = f"${card1[0] / 1000:.1f}K" if card1[0] >= 1000 else card1[0]
        formatted_sales = f"${card1[0] / 1000000:.1f}M" if card1[0] >= 1000000 else formatted_sales
    else:
        formatted_sales="$0"
    col1.metric(value=formatted_sales, label="Total Sales")


    # Card2: Number of Products Sold with applying related filter if exist:
    num_products_sold =  DB().query("SELECT Sum(quantity) FROM sales WHERE date>=\""+selected_start_date+
                                    "\" AND date<=\""+selected_end_date+"\";")
    card2=[row[0] for row in num_products_sold ]
    formatted_pro = f"{card2[0] / 1000:.1f}K" if card2[0] >= 1000 else card2[0]
    col2.metric(value=formatted_pro, label="Number of Products Sold" )

    # Card3: Average Rating (rounded to two decimal positions) with applying related filter if exist:
    average_rating = DB().query("SELECT AVG(rating) FROM review; ")
    card3= [row[0] for row in average_rating ]
    col3.metric(value=round(card3[0], 2), label="Average Rating")

    # Card4: Number of Customers with applying related filter if exist:
    num_customers = DB().query("SELECT Count(DISTINCT customer_id) FROM sales WHERE date>=\""+selected_start_date+
                              "\" AND date<=\""+selected_end_date+"\";")
    card4=[row[0] for row in num_customers]
    col4.metric(value=int(card4[0]), label="Number of Customers")


   

def slicers():
    # Date Slicer
    min_date = DB().query("SELECT MIN(date) FROM sales;")
    max_date = DB().query("SELECT MAX(date) FROM sales;")
    mindate = [row[0] for row in min_date]
    maxdate = [row[0] for row in max_date]
    selected_start_date = st.date_input("Select Start Date:", min_value=mindate[0], max_value=maxdate[0], value=mindate[0])
    selected_end_date = st.date_input("Select End Date:", min_value=selected_start_date, max_value=maxdate[0], value=maxdate[0])

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
    product=DB().query("SELECT DISTINCT product_id FROM products;")
    product_list = [row[0] for row in product]
    if selected_category!='All':
        product=DB().query("SELECT DISTINCT product_id FROM products WHERE category=\""+selected_category+"\";")
        product_list = [row[0] for row in product]
    if selected_subcategory!='All':
        product=DB().query("SELECT DISTINCT product_id FROM products WHERE sub_category=\""+selected_subcategory+"\";")
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

    # Tabs:
    chosen_id = stx.tab_bar(data=[
    stx.TabBarItemData(id="tab1", title="🌐 Overview",description=''),
    stx.TabBarItemData(id="tab2", title="💸 Performance",description=''),
    stx.TabBarItemData(id="tab3", title="📆 Sales Prediction",description='') ], default="tab1")
    st.markdown('<hr style="margin-top: 5px;">', unsafe_allow_html=True)
    
    filter={}

    # Each tab has its own code:
    # Tab1: Overview:
    if chosen_id == "tab1":
        # Sidebar code which contains (image, logout button, slicers func):
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
        # Visuals calling func:
        visuals(filter)
    
    # Tab2: Performance:
    elif chosen_id == "tab2":
        # Sidebar code which contains (image, logout button, slicers func):
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
        data = DB().query(sql) 
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
                    # Errorrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr
                    dfSelected = pd.DataFrame({'Month': month_num, 'Year': selected_year})
                    xpred= df[['Month', 'Year']].values
                    inputted=polynomial_features.fit_transform(xpred)
                    pred = model.predict(inputted)

                    container2.write(pred)
        


    
        
    
 