import pytest
import pandas as pd
import db 
import vaderanalysis, sidbar
from unittest.mock import patch



@pytest.fixture
def mock_tables():
    return {
        'sales': db.sales,
        'full_merged_data': db.full_merged_data,
        'review': db.review,
        'product': db.products,
        'customer': db.customer,
    }

def test_apply_filter_no_filters(mock_tables):
    """
        Tests performance function with no filters applied.
    """
    filter = {}
    filter = sidbar.visuals().slicers() # will return selected as = 'All'
    result = vaderanalysis.applyfilter(filter)
            
    expected_df=  mock_tables['review']

    assert result[2]['date'] == False
    assert result[2]['category']  == False
    assert result[2]['subcategory']  == False
    assert result[2]['productid']  == False
    assert result[2]['city']  == False
    assert result[2]['rating']  == False
    assert result[1] == False

    # Assert visuals 
    pd.testing.assert_frame_equal(result[0], expected_df)

def test_apply_filter_all_filters(mock_tables):
    """
        Tests performance function with all filters applied.
    """
    filter = {}
    filter['selected_category'] = mock_tables['product']['category'][700] #Random category
    # This Handled in UI, so rewrite it here again:
    if mock_tables['sales']['date'][9] < mock_tables['sales']['date'][876]:
        filter['selected_start_date'] = mock_tables['sales']['date'][9] #Random Date
        filter['selected_end_date'] = mock_tables['sales']['date'][876] #Random Date
    else:
        filter['selected_start_date'] = mock_tables['sales']['date'][876] #Random Date
        filter['selected_end_date'] = mock_tables['sales']['date'][9] #Random Date
    # This Handled in UI, so rewrite it here again:
    if mock_tables['review']['rating'][69] < mock_tables['review']['rating'][356]:
        filter['selected_min_rating'] = mock_tables['review']['rating'][69] #Random rating
        filter['selected_max_rating'] = mock_tables['review']['rating'][876] #Random rating
    else:
        filter['selected_min_rating'] = mock_tables['review']['rating'][356] #Random rating
        filter['selected_max_rating'] = mock_tables['review']['rating'][69] #Random rating
    filter['selected_subcategory'] = mock_tables['product']['sub_category'][18] #Random subcategory
    filter['selected_product'] = mock_tables['product']['product_id'][50] #Random productid
    filter['selected_city'] = mock_tables['customer']['city'][73] #Random city
    
    result = vaderanalysis.applyfilter(filter)
    
    filtered_table= mock_tables['full_merged_data'][mock_tables['full_merged_data']['category'] == filter.get('selected_category')]
    filtered_table = filtered_table[(filtered_table['rating'] >= filter.get('selected_min_rating')) & (filtered_table['rating'] <= filter.get('selected_max_rating'))]
    filtered_table= filtered_table[(filtered_table['date'] >= filter['selected_start_date']) & (filtered_table['date'] <= filter['selected_end_date'])]
    filtered_table= filtered_table[filtered_table['sub_category'] == filter.get('selected_subcategory')]
    filtered_table= filtered_table[filtered_table['product_id'] == filter.get('selected_product')]
    filtered_table= filtered_table[filtered_table['city'] == filter.get('selected_city')]
            
    expected_df=  filtered_table

    assert result[2]['date'] == True
    assert result[2]['category']  == True
    assert result[2]['subcategory']  == True
    assert result[2]['productid']  == True
    assert result[2]['city']  == True
    assert result[2]['rating']  == True
    assert result[1] == True

    # Assert visuals 
    pd.testing.assert_frame_equal(result[0], expected_df)


def test_sentimentClass():
    # Test on the Boundary Values
    assert ":smile: Positive" == vaderanalysis.sentimentClass(0.051)
    assert ":disappointed: Negative" == vaderanalysis.sentimentClass(-0.051)
    assert ":neutral_face: Neutral" == vaderanalysis.sentimentClass(0.05)
    assert ":neutral_face: Neutral" == vaderanalysis.sentimentClass(-0.05)
    assert ":neutral_face: Neutral" == vaderanalysis.sentimentClass(0.03)
    assert ":neutral_face: Neutral" == vaderanalysis.sentimentClass(-0.03)


def test_updateSentimentcsv(mock_tables):
    # Test that the sentiment_results.csv has all the id in review table from db 
    vaderanalysis.updateSentimentcsv()
    sentiment_results = pd.read_csv('static/sentiment_results.csv')
    assert (mock_tables['review']['review_id'].isin(sentiment_results['review_id']).all())  == True


def test_vaderanalysis(mock_tables):
    # Test the sentiment_results of inputted txt 
    filter={}

    # Ex1: (negative ex)
    txt ='this product is so badddd'
    re = vaderanalysis.vaderanalysis(filter,txt)
    assert re[0] < -0.05
    assert re[1] == ":disappointed: Negative"

    # Ex2: (positive ex)
    txt ='nice product with good quality'
    re = vaderanalysis.vaderanalysis(filter,txt)
    assert re[0] > 0.05
    assert re[1] == ":smile: Positive"

    # Ex3: (natural ex)
    txt ='so so' #means half good and half bad
    re = vaderanalysis.vaderanalysis(filter,txt)
    assert re[0] >= -0.5 and re[0] <= 0.5
    assert re[1] == ":neutral_face: Neutral"


def test_normalize_elongated_words():
    # Test normalize func
    dictionary_with_repeated_letters = vaderanalysis.read_dictionary_from_csv('static/doubled_words.csv')

    txt='soooooo baaaddddd'
    expected_result='so bad'
    normalize_txt= vaderanalysis.normalize_elongated_words(txt,dictionary_with_repeated_letters)

    txt1='tooooo goooood'
    expected_result1='too good'
    normalize_txt1= vaderanalysis.normalize_elongated_words(txt1,dictionary_with_repeated_letters)

    # Assertions
    assert normalize_txt == expected_result
    assert normalize_txt1 == expected_result1

    
