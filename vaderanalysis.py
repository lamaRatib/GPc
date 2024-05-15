import streamlit as st
import database.db as db
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def sentimentClassification(avgcompound):
    if avgcompound >= 0.05:
        return "Positive"
    elif avgcompound <= - 0.05:
        return "Negative"
    else:
        return "Neutral"
 
def applyfilter(filter):
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
    
    if date or category or subcategory or productid or city or review:
        data = filtered_table['review_content']
    else:
        data = db.review['review_content']

    return data 

def vaderanalysis(filter,txt):
    analyzer = SentimentIntensityAnalyzer()
    data = applyfilter(filter)
    if isinstance(txt, bool):
        sum=0
        for review in data:
            sentiment_dict = analyzer.polarity_scores(str(review))
            sum+=sentiment_dict['compound'] 
        avgcompound=sum/len(data)      # /0 handl
        st.write(avgcompound)

    elif isinstance(txt, str):
        if txt=='':
            pass
        else:
            sentiment_dict = analyzer.polarity_scores(txt)
            compound=sentiment_dict['compound'] 
            st.write(sentimentClassification(compound))
        


 
    