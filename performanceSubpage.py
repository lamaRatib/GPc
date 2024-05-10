import streamlit as st
import db 
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def performance(filter): 

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
            filtered_table=filtered_table[(filtered_table['date'] >= selected_start_date) & (filtered_table['date'] <= selected_end_date)]
        else:
            filtered_table=db.full_merged_data[(db.full_merged_data['date'] >= selected_start_date) & (db.full_merged_data['date'] <= selected_end_date)]

        date=True
        

    # Check selected_category filter
    if filter.get('selected_category') != 'All':
        if date  or subcategory or productid or city or review: 
            filtered_table=filtered_table[filtered_table['category'] == filter.get('selected_category')]
        else:
            filtered_table=db.full_merged_data[db.full_merged_data['category'] == filter.get('selected_category')]
        
        category=True

    # Check selected_subcategory filter
    if filter.get('selected_subcategory') != 'All':
        if date or category or productid or city or review:
            filtered_table=filtered_table[filtered_table['sub_category'] == filter.get('selected_subcategory')]
        else:
            filtered_table=db.full_merged_data[db.full_merged_data['sub_category'] == filter.get('selected_subcategory')]
        
        subcategory=True

    # Check selected_product filter
    if filter.get('selected_product') != 'All':
        if date or category or subcategory or city or review:
            filtered_table = filtered_table[filtered_table['product_id'] == filter.get('selected_product')]
        else:
            filtered_table = db.full_merged_data[db.full_merged_data['product_id'] == filter.get('selected_product')]
        
        productid=True

    # Check selected_city filter
    if filter.get('selected_city') != 'All':
        if date or category or subcategory or productid or review:
            filtered_table=filtered_table[filtered_table['city'] == filter.get('selected_city')]
        else:
            filtered_table=db.full_merged_data[db.full_merged_data['city'] == filter.get('selected_city')]
        
        city=True


    # Check selected_min_rating and selected_max_rating filters
    if filter.get('selected_min_rating') != 5.0:
        if filter.get('selected_min_rating') == 0.0 and filter.get('selected_max_rating') == 5.0:
            pass
        else:
            if category or subcategory or productid or city or date:
                filtered_table=filtered_table[(filtered_table['rating'] >= filter.get('selected_min_rating')) & (filtered_table['rating'] <= filter.get('selected_max_rating'))]
            else:
                filtered_table=db.full_merged_data[(db.full_merged_data['rating'] >= filter.get('selected_min_rating')) & (db.full_merged_data['rating'] <= filter.get('selected_max_rating'))]
            
            review=True


    # Visual 1:
    if category or subcategory or productid or city or review or date:
        visual_1 = filtered_table.groupby('date')['discounted_price'].sum().reset_index()
    else:
        visual_1 = db.sales.groupby('date')['discounted_price'].sum().reset_index()
        
    visual_1.rename(columns={'date': 'Date', 'discounted_price':'Total Sales'}, inplace=True)

    # Result Ploting:
    fig= px.line(visual_1,x='Date',y='Total Sales',title='Total Sales Over Time',height=260,color_discrete_sequence=[ "LightSlateGray"])
    fig.layout.xaxis.fixedrange = True
    fig.layout.yaxis.fixedrange = True 
    fig.update_layout(margin=dict(t=20))
    config = {'displayModeBar': False,'dragMode':False}
    st.plotly_chart(fig,config=config,use_container_width=True)

    col=st.columns([4,1.5], gap="large")

    # Visual 2:
    with col[0]:
        if category or subcategory or productid or city or review or date:
            filtered_table['Price']= filtered_table['discounted_price'] / filtered_table['quantity']
            visual_2 = filtered_table.groupby('product_id')['Price'].mean().reset_index()
        else:
            db.sales['Price']= db.sales['discounted_price'] / db.sales['quantity']
            visual_2= db.sales.groupby('product_id')['Price'].mean().reset_index()
        fig_boxplot = px.box(visual_2, y='Price', height=250,title='Box Plot of Prices',color_discrete_sequence=[ "LightSlateGray"])
        fig_boxplot.layout.xaxis.fixedrange = True
        fig_boxplot.layout.yaxis.fixedrange = True 
        fig_boxplot.update_layout(margin=dict(t=20))

        config = {'displayModeBar': False,'dragMode':False}
        st.plotly_chart(fig_boxplot,config=config,use_container_width=True)

    
    # Visual 3:
    with col[1]:
        Target= 30000000
        Total_sales=db.sales['discounted_price'].sum()
        g = go.Figure(go.Indicator(domain = {'x': [0, 1], 'y': [0, 1]}, value = Total_sales, mode = "gauge+number+delta",
                title = {'text': "Target VS Total Sales"}, delta = {'reference': Target}, gauge = {'axis': {'range': [None, Target]}}))
        g.layout.xaxis.fixedrange = True
        g.layout.yaxis.fixedrange = True 
        g.update_layout(
                height=260,  # Specify the height
                width=400,   # Specify the width
                margin=dict(t=40)  # Set the top margin
            )
        config = {'displayModeBar': False,'dragMode':False}
        st.plotly_chart(g,config=config,use_container_width=True)


