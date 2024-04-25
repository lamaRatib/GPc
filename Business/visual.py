import streamlit as st
import pandas as pd
import numpy as np
from Database import db

class visuals:

    def slicers(self):
        all=pd.DataFrame(['All'])

        # Date Slicer
        min_date = db.sales['date'].min()
        max_date = db.sales['date'].max()
        selected_start_date = st.date_input("Select Start Date:", min_value=min_date, max_value=max_date, value=min_date)
        selected_end_date = st.date_input("Select End Date:", min_value=selected_start_date, max_value=max_date, value=max_date)

        # Category Slicer
        category=db.products['category'].unique()   
        category = np.append(all, category)
        selected_category = st.selectbox("Select Category:",category, key='category_selectbox') 

        # Sub-Category Slicer
        subcategory=db.products['sub_category'].unique()
        if selected_category!='All':
            subcategory=db.products[db.products['category']==selected_category]['sub_category'].unique()
        subcategory=np.append(all,subcategory)
        selected_subcategory = st.selectbox("Select Sub-Category:", subcategory , key='subcategory_selectbox')

        # Product Slicer
        product=db.products['product_id'].unique()
        if selected_category!='All':
            product=db.products[db.products['category']==selected_category]['product_id'].unique()
        if selected_subcategory!='All':
            product=db.products[db.products['sub_category']==selected_subcategory]['product_id'].unique()
        product= np.append(all,product)
        selected_product = st.selectbox("Select Product:", product, key='product_selectbox')

        # City Slicer
        city=db.customer['city'].unique()
        if selected_category!='All':
            merged_df = pd.merge(db.customer, db.sales, on='customer_id')
            merged_df = pd.merge(merged_df, db.products, on='product_id')
            city = merged_df[merged_df['category'] == selected_category]['city'].unique()

        if selected_subcategory!='All':
            merged_df = pd.merge(db.customer, db.sales, on='customer_id')
            merged_df = pd.merge(merged_df, db.products, on='product_id')
            filtered_df = merged_df[merged_df['sub_category'] == selected_subcategory]['city'].unique()

        if selected_product!='All':
            merged_df = pd.merge(db.customer, db.sales, on='customer_id')
            merged_df = pd.merge(merged_df, db.products, on='product_id')
            filtered_df = merged_df[merged_df['product_id'] == selected_product]['city'].unique()

        city= np.append(all,city)
        selected_city = st.selectbox("Select City:", city, key='city_selectbox')

        # Rating Slicer
        selected_min_rating = st.sidebar.slider("Select Minimum Rating:", min_value=0.0, max_value=5.0, step=0.1, value=0.0)
        if selected_min_rating!=5.0:
            selected_max_rating = st.sidebar.slider("Select Maximum Rating:", min_value=selected_min_rating, max_value=5.0, step=0.1, value=5.0)
        else:
            selected_max_rating=5.0 
            
        selected={"selected_start_date":selected_start_date,"selected_end_date":selected_end_date,
                "selected_category":selected_category,"selected_subcategory":selected_subcategory,"selected_city":selected_city,
                "selected_product":selected_product,"selected_max_rating":selected_max_rating,"selected_min_rating":selected_min_rating}
        
        return selected

    def sidebar_top(self):
        container3 = st.container(border=True,height=70)
        with container3:
            col = st.columns([3.2, 3], gap="medium")
            with col[0]:
                st.image("AmazonLogo2.svg", width=90)
            with col[1]:
                if st.button('logout',key="logout-original"):
                    st.session_state['authentication_status'] = False
                    st.session_state['logged_out'] = True
                    st.session_state['session_ends'] = False
                    st.rerun()
        st.markdown('<hr style="margin-top: 0px; margin-bottom: 7px">', unsafe_allow_html=True)
        st.subheader(':level_slider: Slicers:')
    


