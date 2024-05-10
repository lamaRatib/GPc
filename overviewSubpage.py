import streamlit as st
import db 
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

    
    # Card1: Total Sales
    if date or category or subcategory or productid or city or review:
        card1 = filtered_table['discounted_price'].sum()
    else:
        card1 = db.sales['discounted_price'].sum() 

    if card1 != None:
        formatted_sales = f"${card1 / 1000:.1f}K" if card1 >= 1000 else card1
        formatted_sales = f"${card1 / 1000000:.1f}M" if card1 >= 1000000 else formatted_sales
    elif card2 > 0:
        formatted_pro=f"${card1}"
    else:
        formatted_sales="$0"
    col1.metric(value=str(formatted_sales), label="Total Sales")


    # Card2: Number of Products Sold
    if category or subcategory or productid or city or review or date:
        card2 = filtered_table['quantity'].sum() 
    else:
        card2 = db.sales['quantity'].sum() 

    if card2 != None:
        formatted_pro = f"{card2 / 1000:.1f}K" if card2 >= 1000 else card2
        formatted_pro = f"{card2 / 1000000:.1f}M" if card2 >= 1000000 else formatted_pro
    else:
        formatted_pro="0"
    col2.metric(value=str(formatted_pro), label="Number of Products Sold")


    # Card3: Average Rating
    if category or subcategory or productid or city or review or date:
        card3 = filtered_table['rating'].mean()
    else:
        card3 = db.review['rating'].mean()

    if card3 is None:
        card3=0
    else:
        card3=round(card3, 2)
    col3.metric(value= str(card3), label="Average Rating")


    # Card4: Number of Customers with applying related filter if exist:
    if category or subcategory or productid or city or review or date:
        card4 = filtered_table['customer_id'].nunique()
    else:
        card4 = db.customer['customer_id'].nunique()
    col4.metric(value=int(card4), label="Number of Customers")

    col=st.columns(2)

    # Visual1:
    with col[0]:
        # Data preparing & Filter Reflicting:
        if category or subcategory or productid or city or review or date:
            visual_2 = filtered_table.groupby('category')['quantity'].sum().reset_index()
        else:
            merged_df = db.sales.merge(db.products, on='product_id', how='inner')
            visual_2 = merged_df.groupby('category')['quantity'].sum().reset_index()
        visual_2.rename(columns={'category': 'Category', 'quantity':'Count of Sales'}, inplace=True)

        # Result Ploting:
        fig= px.pie(visual_2, names='Category', values='Count of Sales', title='# of Sales per Category',height=400,color_discrete_sequence=["LightGray", "Silver", "DimGray", "LightSlateGray","DarkSlateGray","Black"])
        fig.layout.xaxis.fixedrange = True
        fig.layout.yaxis.fixedrange = True
        config = {'displayModeBar': False,'dragMode':False}
        st.plotly_chart(fig,config=config,use_container_width=True)

    # Visual2:
    with col[1]:
        # Data preparing & Filter Reflicting:
        if category or subcategory or productid or city or review or date:
            visual_1 = filtered_table.groupby('city')['rating'].mean().reset_index()
        else:
            merged_df = db.review.merge(db.products, on='product_id', how='inner')
            merged_df = merged_df.merge(db.customer, on='customer_id', how='inner')
            visual_1 = merged_df.groupby('city')['rating'].mean().reset_index()
        
        result_df_top10 = visual_1.sort_values(by='rating', ascending=False).head(10)
        result_df_top10.rename(columns={'city': 'City', 'rating':'Avg Rating'}, inplace=True)

        # Result Ploting:
        fig= px.bar(result_df_top10,x='City',y='Avg Rating',title='Top 10 AVG Rating by City',height=350,color_discrete_sequence=[ "LightSlateGray"])
        fig.layout.xaxis.fixedrange = True
        fig.layout.yaxis.fixedrange = True 
        config = {'displayModeBar': False,'dragMode':False}
        st.plotly_chart(fig,config=config,use_container_width=True)

    
    
    st.markdown(
        """
        <style>
            div[data-testid=stToast] {
                background-color: #2C2C2C;
                width: 25%;
            }
             
            [data-testid=toastContainer] [data-testid=stMarkdownContainer] > p {
                font-size: 15px; font-style: normal; font-weight: 450;
                foreground-color: #565654;
            }
        </style>
        """, unsafe_allow_html=True
    )

    # Slicers updates notification:
    if category:
        st.toast(':level_slider: The displayed data is filtered by category: '+filter.get('selected_category')) 
    