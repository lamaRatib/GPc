import streamlit as st
import Database.db as db 
import pandas as pd
import plotly.express as px




def vis(filter): 
    col1, col2, col3, col4 = st.columns(4)

    # Filter Condition preparation:
    selected_start_date = filter.get('selected_start_date').strftime('%Y-%m-%d')
    selected_end_date = filter.get('selected_end_date').strftime('%Y-%m-%d')
    where_conditions = []
    product_join_ONS=''
    customer_join=''
    review_join=''
    
    
    if filter.get('selected_category') != 'All':
        where_conditions.append(f"p.category = '{filter.get('selected_category')}'")
        product_join_ONS="JOIN products AS p ON s.product_id = p.product_id"

    if filter.get('selected_subcategory') != 'All':
        where_conditions.append(f"p.sub_category = '{filter.get('selected_subcategory')}'")
        if product_join_ONS=='':
            product_join_ONS="JOIN products AS p ON s.product_id = p.product_id"

    if filter.get('selected_product') != 'All':
        where_conditions.append(f"p.product_id = '{filter.get('selected_product')}'")
        if product_join_ONS=='':
            product_join_ONS="JOIN products AS p ON s.product_id = p.product_id"

    if filter.get('selected_city') != 'All':
        where_conditions.append(f"c.city = '{filter.get('selected_city')}'")
        customer_join="JOIN customer AS c ON s.customer_id = c.customer_id"
    
    if filter.get('selected_min_rating')==5.0:
        pass
    elif filter.get('selected_min_rating')== 0.0 and filter.get('selected_max_rating')==5.0:
        pass
    else:
        where_conditions.append(f"r.rating >= {filter.get('selected_min_rating')} AND r.rating <= {filter.get('selected_max_rating')}")
        review_join="JOIN review AS r ON s.product_id = r.product_id"

    where_clause = " AND ".join(where_conditions)

    # Card1: Total Sales with applying related filter if exist:
    sql1 = f"""
        SELECT SUM(s.discounted_price) FROM sales AS s
        { product_join_ONS +" "}{customer_join+" "}{review_join+" "}
        WHERE s.date >= '{selected_start_date}' AND s.date <= '{selected_end_date}'
        {'AND ' + where_clause if where_clause else ''}
    """
    card1=db.sales['discounted_price'].sum()
    if card1 != None:
        formatted_sales = f"${card1 / 1000:.1f}K" if card1 >= 1000 else card1
        formatted_sales = f"${card1 / 1000000:.1f}M" if card1 >= 1000000 else formatted_sales
    else:
        formatted_sales="$0"
    col1.metric(value=str(formatted_sales), label="Total Sales")


    # Card2: Number of Products Sold with applying related filter if exist:
    sql2 = f"""
        SELECT Sum(quantity) FROM sales AS s
        { product_join_ONS +" "}{customer_join+" "}{review_join+" "}
        WHERE s.date >= '{selected_start_date}' AND s.date <= '{selected_end_date}'
        {'AND ' + where_clause if where_clause else ''}
    """
    num_products_sold =  db.DB().query(sql2)
    card2=[row[0] for row in num_products_sold ]
    if card2[0]!=None:
        formatted_pro = f"{card2[0] / 1000:.1f}K" if card2[0] >= 1000 else card2[0]
        formatted_pro = f"{card2[0] / 1000000:.1f}M" if card2[0] >= 1000000 else formatted_pro
    else:
        formatted_pro="0"
    col2.metric(value=str(formatted_pro), label="Number of Products Sold" )

    # Card3: Average Rating (rounded to two decimal positions) with applying related filter if exist:
    sql3 = f"""
        SELECT AVG(rating) FROM review AS r        
    """
    average_rating =db.DB().query(sql3)
    card3= [row[0] for row in average_rating ]
    col3.metric(value=round(float(card3[0]), 2), label="Average Rating of all products")

    # Card4: Number of Customers with applying related filter if exist:
    sql4 = f"""
        SELECT Count(DISTINCT customer_id) FROM customer AS c
    """
    num_customers = db.DB().query(sql4)
    card4=[row[0] for row in num_customers]
    col4.metric(value=int(card4[0]), label="Number of Customers")

    # Visual1:
    col=st.columns(2)
    # Plot bar chart for Number of Sales per Category
    with col[0]:
        sql5=f"""
            SELECT Count(sale_id), p.category FROM sales AS s
            JOIN products AS p ON s.product_id = p.product_id
            {customer_join+" "}{review_join+" "}
             WHERE s.date >= '{selected_start_date}' AND s.date <= '{selected_end_date}'
            {'AND ' + where_clause if where_clause else ''}
            GROUP BY p.category
        """
        chart1_data = db.DB().query(sql5) 
        df=pd.DataFrame(chart1_data,columns=['# of Sales','Category'])
        fig= px.pie(df, names='Category', values='# of Sales', title='# of Sales per Category',height=400,color_discrete_sequence=["LightGray", "Silver", "DimGray", "LightSlateGray","DarkSlateGray","Black"])
        fig.layout.xaxis.fixedrange = True
        fig.layout.yaxis.fixedrange = True
        config = {'displayModeBar': False,'dragMode':False}
        st.plotly_chart(fig,config=config,use_container_width=True)

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

    
