import streamlit as st
import db 
import pandas as pd
import plotly.express as px




def overview(filter): 
    col1, col2, col3, col4 = st.columns(4)

    # Filter Condition preparation:
    selected_start_date =filter.get('selected_start_date')
    selected_end_date = filter.get('selected_end_date')
   
    date=False
    category=False
    subcategory=False
    productid=False
    city=False
    review=False

    # Check selected_start_date & selected_end_date filter
    if selected_start_date != db.sales['date'].min() or selected_end_date != db.sales['date'].max():
        if category or subcategory or productid or city or review:
            filtered_sales_product=db.filtered_sales_product[(db.filtered_sales_product['date'] >= selected_start_date) & (db.filtered_sales_product['date'] >= selected_end_date)]
            filtered_sales_product_customer=db.filtered_sales_product_customer[(db.filtered_sales_product_customer['date'] >= selected_start_date) & (db.filtered_sales_product_customer['date'] >= selected_end_date)]
            filtered_sales_product_customer_review=db.filtered_sales_product_customer_review[(db.filtered_sales_product_customer_review['date'] >= selected_start_date) & (db.filtered_sales_product_customer_review['date'] >= selected_end_date)]
        else:   
            filtered_sales_product=db.sales_product[(db.sales_product['date'] >= selected_start_date) & (db.sales_product['date'] >= selected_end_date)]
            filtered_sales_product_customer=db.sales_product_customer[(db.sales_product_customer['date'] >= selected_start_date) & (db.sales_product_customer['date'] >= selected_end_date)]
            filtered_sales_product_customer_review=db.sales_product_customer_review[(db.sales_product_customer_review['date'] >= selected_start_date) & (db.sales_product_customer_review['date'] >= selected_end_date)] 
        date=True
        

    # Check selected_category filter
    if filter.get('selected_category') != 'All':
        if date  or subcategory or productid or city:
            filtered_sales_product=db.filtered_sales_product[db.filtered_sales_product['category'] == filter.get('selected_category')]
            filtered_sales_product_customer=db.filtered_sales_product_customer[db.filtered_sales_product_customer['category'] == filter.get('selected_category')]
            filtered_sales_product_customer_review=db.filtered_sales_product_customer_review[db.filtered_sales_product_customer_review['category'] == filter.get('selected_category')]
        else:
            filtered_sales_product=db.sales_product[db.sales_product['category'] == filter.get('selected_category')]
            filtered_sales_product_customer=db.sales_product_customer[db.sales_product_customer['category'] == filter.get('selected_category')]
            filtered_sales_product_customer_review=db.sales_product_customer_review[db.sales_product_customer_review['category'] == filter.get('selected_category')]
        
        if subcategory or productid:
            filter_product=db.filter_product[db.filter_product['category'] == filter.get('selected_category')]
        else:
            filter_product=db.products[db.products['category'] == filter.get('selected_category')]

        if review:
            filtered_review_product=db.filtered_review_product[db.filtered_review_product['category'] == filter.get('selected_category')]
            filtered_review_product_customer=db.filtered_review_product_customer[db.filtered_review_product_customer['category'] == filter.get('selected_category')]
        else:
            filtered_review_product=db.review_product[db.review_product['category'] == filter.get('selected_category')]
            filtered_review_product_customer=db.review_product_customer[db.review_product_customer['category'] == filter.get('selected_category')]
        
        category=True

    # Check selected_subcategory filter
    if filter.get('selected_subcategory') != 'All':
        if category or date:
            filter_product=filter_product[filter_product['sub_category'] == filter.get('selected_subcategory')]
            filtered_sales_product=filtered_sales_product[filtered_sales_product['sub_category'] == filter.get('selected_subcategory')]
            filtered_sales_product_customer=filtered_sales_product_customer[filtered_sales_product_customer['sub_category'] == filter.get('selected_subcategory')]
            filtered_sales_product_customer_review=filtered_sales_product_customer_review[filtered_sales_product_customer_review['sub_category'] == filter.get('selected_subcategory')]
            filtered_review_product=filtered_review_product[filtered_review_product['sub_category'] == filter.get('selected_subcategory')]
            filtered_review_product_customer=filtered_review_product_customer[filtered_review_product_customer['sub_category'] == filter.get('selected_subcategory')]
        else:
            filter_product=db.products[db.products['sub_category'] == filter.get('selected_subcategory')]
            filtered_sales_product=db.sales_product[db.sales_product['sub_category'] == filter.get('selected_subcategory')]
            filtered_sales_product_customer=db.sales_product_customer[db.sales_product_customer['sub_category'] == filter.get('selected_subcategory')]
            filtered_sales_product_customer_review=db.sales_product_customer_review[db.sales_product_customer_review['sub_category'] == filter.get('selected_subcategory')]
            filtered_review_product=db.review_product[db.review_product['sub_category'] == filter.get('selected_subcategory')]
            filtered_review_product_customer=db.review_product_customer[db.review_product_customer['sub_category'] == filter.get('selected_subcategory')]
        subcategory=True

    # Check selected_product filter
    if filter.get('selected_product') != 'All':
        if category or subcategory or date:
            filter_product=filter_product[filter_product['product_id'] == filter.get('selected_product')]
            filtered_sales_product=filtered_sales_product[filtered_sales_product['product_id'] == filter.get('selected_product')]
            filtered_sales_product_customer=filtered_sales_product_customer[filtered_sales_product_customer['product_id'] == filter.get('selected_product')]
            filtered_sales_product_customer_review=filtered_sales_product_customer_review[filtered_sales_product_customer_review['product_id'] == filter.get('selected_product')]
            filtered_review_product=filtered_review_product[filtered_review_product['product_id'] == filter.get('selected_product')]
            filtered_review_product_customer=filtered_review_product_customer[filtered_review_product_customer['product_id'] == filter.get('selected_product')]
        else:
            filter_product=db.products[db.products['product_id'] == filter.get('selected_product')]
            filtered_sales_product=db.sales_product[db.sales_product['product_id'] == filter.get('selected_product')]
            filtered_sales_product_customer=db.sales_product_customer[db.sales_product_customer['product_id'] == filter.get('selected_product')]
            filtered_sales_product_customer_review=db.sales_product_customer_review[db.sales_product_customer_review['product_id'] == filter.get('selected_product')]
            filtered_review_product=db.review_product[db.review_product['product_id'] == filter.get('selected_product')]
            filtered_review_product_customer=db.review_product_customer[db.review_product_customer['product_id'] == filter.get('selected_product')]
        productid=True

    # Check selected_city filter
    if filter.get('selected_city') != 'All':
        if category or subcategory or productid or date:
            filtered_sales_product_customer=filtered_sales_product_customer[filtered_sales_product_customer['city'] == filter.get('selected_city')]
            filtered_sales_product_customer_review=filtered_sales_product_customer_review[filtered_sales_product_customer_review['city'] == filter.get('selected_city')]
            filtered_review_product_customer=filtered_review_product_customer[filtered_review_product_customer['city'] == filter.get('selected_city')]
        else:
            filtered_sales_product_customer=db.sales_product_customer[db.sales_product_customer['city'] == filter.get('selected_city')]
            filtered_sales_product_customer_review=db.sales_product_customer_review[db.sales_product_customer_review['city'] == filter.get('selected_city')]
            filtered_review_product_customer=db.review_product_customer[db.review_product_customer['city'] == filter.get('selected_city')]
        filtered_customer=db.customer[db.customer['city'] == filter.get('selected_city')]
        city=True


    # Check selected_min_rating and selected_max_rating filters
    if filter.get('selected_min_rating') != 5.0:
        if filter.get('selected_min_rating') == 0.0 and filter.get('selected_max_rating') == 5.0:
            pass
        else:
            if category or subcategory or productid or city or date:
                filtered_sales_product_customer_review=filtered_sales_product_customer_review[(filtered_sales_product_customer_review['rating'] >= filter.get('selected_min_rating')) & (filtered_sales_product_customer_review['rating'] <= filter.get('selected_max_rating'))]
                filtered_review_product=filtered_review_product[(filtered_review_product['rating'] >= filter.get('selected_min_rating')) & (filtered_review_product['rating'] <= filter.get('selected_max_rating'))]
                filtered_review_product_customer=filtered_review_product_customer[(filtered_review_product_customer['rating']>= filter.get('selected_min_rating')) & (filtered_review_product_customer['rating'] <= filter.get('selected_max_rating'))]
            else:
                filtered_sales_product_customer_review=db.sales_product_customer_review[(db.sales_product_customer_review['rating'] >= filter.get('selected_min_rating')) & (db.sales_product_customer_review['rating'] <= filter.get('selected_max_rating'))]
                filtered_review_product=db.review_product[(db.review_product['rating'] >= filter.get('selected_min_rating')) & (db.review_product['rating'] <= filter.get('selected_max_rating'))]
                filtered_review_product_customer=db.review_product_customer[(db.review_product_customer['rating']>= filter.get('selected_min_rating')) & (db.review_product_customer['rating'] <= filter.get('selected_max_rating'))]
            filtered_review=db.review[(db.review['rating'] >= filter.get('selected_min_rating')) & (db.review['rating'] <= filter.get('selected_max_rating'))]
            review=True


    # Card1: Total Sales
    if category or subcategory or productid or city or review:
        if category or subcategory or productid or date:
            card1 = filtered_sales_product['discounted_price'].sum() 
        if city:
            card1 = filtered_sales_product_customer['discounted_price'].sum()
        if review:
            card1 = filtered_sales_product_customer_review['discounted_price'].sum()
    else:
        card1 = db.sales['discounted_price'].sum() 

    if card1 != None:
        formatted_sales = f"${card1 / 1000:.1f}K" if card1 >= 1000 else card1
        formatted_sales = f"${card1 / 1000000:.1f}M" if card1 >= 1000000 else formatted_sales
    else:
        formatted_sales="$0"
    col1.metric(value=str(formatted_sales), label="Total Sales")


    # Card2: Number of Products Sold
    if category or subcategory or productid or city or review or date:
        if category or subcategory or productid or date:
            card2 = filtered_sales_product['quantity'].sum()  
        if city:
            card2 = filtered_sales_product_customer['quantity'].sum() 
        if review:
            card2 = filtered_sales_product_customer_review['quantity'].sum() 
    else:
        card2 = db.sales['quantity'].sum() 

    if card2 != None:
        formatted_pro = f"${card2 / 1000:.1f}K" if card2 >= 1000 else card2
        formatted_pro = f"${card2 / 1000000:.1f}M" if card2 >= 1000000 else formatted_pro
    else:
        formatted_pro="$0"
    col2.metric(value=str(formatted_pro), label="Number of Products Sold")


    # Card3: Average Rating
    if category or subcategory or productid or city or review or date:
        if category or subcategory or productid:
            card3 = filtered_review_product['rating'].mean() 
        if city:
            card3 = filtered_review_product_customer['rating'].mean()
        if review:
            card3 = filtered_review['rating'].mean()
        if date: 
            card3 = filtered_sales_product_customer_review['rating'].mean()
    else:
        card3 = db.review['rating'].mean()
    col3.metric(value=round(card3, 2), label="Average Rating")


    # Card4: Number of Customers with applying related filter if exist:
    if category or subcategory or productid or city or review or date:
        if category or subcategory or productid or date:
            card4 = filtered_sales_product_customer['customer_id'].nunique() 
        if city:
            card4 = filtered_customer['customer_id'].nunique()
        if review:
            card4 = filtered_review_product_customer['customer_id'].nunique()
    else:
        card4 = db.customer['customer_id'].nunique()
    col4.metric(value=int(card4), label="Number of Customers")


    # Visual1:
    col=st.columns(2)

    # Plot bar chart for Number of Sales per Category
    with col[0]:
        sql5=f"""
            SELECT Count(sale_id), p.category FROM sales AS s
            JOIN products AS p ON s.product_id = p.product_id
             WHERE s.date >= '{selected_start_date}' AND s.date <= '{selected_end_date}'
            GROUP BY p.category
        """
        chart1_data = db.DB().query(sql5) 
        df=pd.DataFrame(chart1_data,columns=['# of Sales','Category'])
        fig= px.pie(df, names='Category', values='# of Sales', title='# of Sales per Category',height=400,color_discrete_sequence=["LightGray", "Silver", "DimGray", "LightSlateGray","DarkSlateGray","Black"])
        fig.layout.xaxis.fixedrange = True
        fig.layout.yaxis.fixedrange = True
        config = {'displayModeBar': False,'dragMode':False}
        st.plotly_chart(fig,config=config,use_container_width=True)

    # Visual2:
    with col[1]:
        # Data preparing:
        merged_df = db.review.merge(db.products, on='product_id', how='inner')
        merged_df = merged_df.merge(db.customer, on='customer_id', how='inner')
        # Filter Reflicting:


        result_df = merged_df.groupby('city')['rating'].mean().reset_index()
        result_df_top10 = result_df.sort_values(by='rating', ascending=False).head(10)
        
        # Data Ploting:
        fig= px.bar(result_df_top10,x='city',y='rating',title='Top 10 AVG Rating by City',height=350,color_discrete_sequence=[ "LightSlateGray"])
        fig.layout.xaxis.fixedrange = True
        fig.layout.yaxis.fixedrange = True 
        config = {'displayModeBar': False,'dragMode':False}
        st.plotly_chart(fig,config=config,use_container_width=True)

    



    