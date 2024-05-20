import db 
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import csv

 
def applyfilter(filter):
    # Filter Condition preparation:
    selected_start_date =filter.get('selected_start_date')
    selected_end_date = filter.get('selected_end_date')
   
    date=False
    category=False
    subcategory=False
    productid=False
    city=False
    rating=False

    # Check selected_start_date & selected_end_date filter
    if selected_start_date != db.sales['date'].min() or selected_end_date != db.sales['date'].max():
        if category or subcategory or productid or city or rating:
            filtered_table=filtered_table[(filtered_table['date'] >= selected_start_date) & (filtered_table['date'] <= selected_end_date)]
        else:
            filtered_table=db.full_merged_data[(db.full_merged_data['date'] >= selected_start_date) & (db.full_merged_data['date'] <= selected_end_date)]

        date=True
        
    # Check selected_category filter
    if filter.get('selected_category') != 'All':
        if date  or subcategory or productid or city or rating: 
            filtered_table=filtered_table[filtered_table['category'] == filter.get('selected_category')]
        else:
            filtered_table=db.full_merged_data[db.full_merged_data['category'] == filter.get('selected_category')]
        
        category=True

    # Check selected_subcategory filter
    if filter.get('selected_subcategory') != 'All':
        if date or category or productid or city or rating:
            filtered_table=filtered_table[filtered_table['sub_category'] == filter.get('selected_subcategory')]
        else:
            filtered_table=db.full_merged_data[db.full_merged_data['sub_category'] == filter.get('selected_subcategory')]
        
        subcategory=True

    # Check selected_product filter
    if filter.get('selected_product') != 'All':
        if date or category or subcategory or city or rating:
            filtered_table = filtered_table[filtered_table['product_id'] == filter.get('selected_product')]
        else:
            filtered_table = db.full_merged_data[db.full_merged_data['product_id'] == filter.get('selected_product')]
        
        productid=True

    # Check selected_city filter
    if filter.get('selected_city') != 'All':
        if date or category or subcategory or productid or rating:
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
            
            rating=True
    
    if date or category or subcategory or productid or city or rating:
        data = filtered_table
        flag=True
    else:
        data = db.review
        flag=False

    
    re = {}
    re['date'] = date
    re['category'] = category
    re['subcategory'] = subcategory
    re['productid'] = productid
    re['city'] = city
    re['rating'] = rating

    return [data, flag, re] 

def vaderanalysis(filter,txt):
    """
        1. analyz stored reveiws and apply filter if exist
        2. analyz the inputted text
    """

    analyzer = SentimentIntensityAnalyzer()

    updateSentimentcsv()

    if isinstance(txt, bool):
        data, flag, re = applyfilter(filter)[0], applyfilter(filter)[1], applyfilter(filter)[2]
        
        sentiment_results = pd.read_csv('static/sentiment_results.csv')

        if flag:
            avgcompound = sentiment_results[sentiment_results['review_id'].isin(data['review_id'])]['compound_score'].mean()
        else:
            avgcompound = sentiment_results['compound_score'].mean()

        sentiment_results.to_csv('static/sentiment_results.csv', index=False)

        return [avgcompound, sentimentClass(avgcompound), re]

    elif isinstance(txt, str):
        dictionary_with_repeated_letters = read_dictionary_from_csv('static/doubled_words.csv')
        normalized_text = normalize_elongated_words(txt,dictionary_with_repeated_letters)        
        sentiment_dict = analyzer.polarity_scores(normalized_text)    
        return [sentiment_dict['compound'], sentimentClass(sentiment_dict['compound'])]
        

def sentimentClass(value):
    if value < -0.05:
        return ":disappointed: Negative"
    elif -0.05 <= value <= 0.05:
        return ":neutral_face: Neutral"
    else:
        return ":smile: Positive"

 
def updateSentimentcsv():
    """
        update sentiment_results.csv whenerver review table is updated 
    """
    analyzer = SentimentIntensityAnalyzer()
    sentiment_results = pd.read_csv('static/sentiment_results.csv')
    dictionary_with_repeated_letters = read_dictionary_from_csv('static/doubled_words.csv')
    missing_review_ids = db.review[~db.review['review_id'].isin(sentiment_results['review_id'])]
    for index, row in missing_review_ids.iterrows():
        review_content = row['review_content']
        normalized_text = normalize_elongated_words(review_content,dictionary_with_repeated_letters)
        sentiment_dict = analyzer.polarity_scores(normalized_text)
        compound = sentiment_dict['compound']
        new_row = {'review_id': row['review_id'], 'compound_score': compound}
        new_df = pd.DataFrame([new_row])
        sentiment_results = pd.concat([sentiment_results, new_df], ignore_index=True)
    
    sentiment_results.to_csv('static/sentiment_results.csv', index=False)



def read_dictionary_from_csv(csv_file):
    # Read Dict taht contains doubled letters words
    dictionary_with_repeated_letters = set()
    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            word = row[0].strip()  # Extract the word from the row
            dictionary_with_repeated_letters.add(word)
    return dictionary_with_repeated_letters



def normalize_elongated_words(text,dictionary_with_repeated_letters):
    def normalize_word(word):
        normalized_word = re.sub(r'(.)\1{2,}', r'\1\1', word)
    
    # Test if the normalized word is in the dictionary
        if normalized_word.lower() in dictionary_with_repeated_letters:
            return normalized_word
        else:
            # If not in dictionary, remove the second repeated character
            return re.sub(r'(.)\1', r'\1', normalized_word)
        
    return ' '.join(normalize_word(word) for word in text.split())

