import pytest
import numpy as np
import db 
import overviewSubpage, sidbar


@pytest.fixture
def mock_tables():
    return {
        'sales': db.sales,
        'full_merged_data': db.full_merged_data,
        'review': db.review,
        'product': db.products,
        'customer': db.customer,
    }


def test_overview_no_filters(mock_tables):
    """
        Tests overview function with no filters applied.
    """
    filter = {}
    filter = sidbar.visuals().slicers() # will return selected as = 'All'
    result = overviewSubpage.overview(filter)
    

    assert result['date'] == False
    assert result['category']  == False
    assert result['subcategory']  == False
    assert result['productid']  == False
    assert result['city']  == False
    assert result['rating']  == False

    # Assert expected values for cards based on mock data
    assert result['card1'] == mock_tables['sales']['discounted_price'].sum()
    assert result['card2'] == mock_tables['sales']['quantity'].sum()
    assert result['card3'] == mock_tables['review']['rating'].mean()
    assert result['card4'] == mock_tables['customer']['customer_id'].nunique()

    # Assert visuals 
    merged_df = mock_tables['sales'].merge(mock_tables['product'], on='product_id', how='inner')
    assert result['visual_2']['Category'].tolist() == merged_df.groupby('category')['quantity'].sum().reset_index()['category'].tolist()
    assert 'City' in result['result_df_top10'].columns  # Check for presence of city column
    assert len(result['result_df_top10']) == 10  # Top 10 cities

    
def test_overview_category_filter(mock_tables):
    filter = {}
    filter = sidbar.visuals().slicers()

    filter['selected_category'] = mock_tables['product']['category'][700] #Random category
    
    result = overviewSubpage.overview(filter)

    filtered_table= mock_tables['full_merged_data'][mock_tables['full_merged_data']['category'] == filter.get('selected_category')]


    assert result['date'] == False
    assert result['category']  == True
    assert result['subcategory']  == False
    assert result['productid']  == False
    assert result['city']  == False
    assert result['rating']  == False

    # Assert expected values for cards based on mock data
    assert result['card1'] == filtered_table['discounted_price'].sum()
    assert result['card2'] == filtered_table['quantity'].sum()
    assert result['card3'] == filtered_table['rating'].mean()
    assert result['card4'] == filtered_table['customer_id'].nunique()

    # Assert visuals 
    assert result['visual_2']['Category'].tolist() == filtered_table.groupby('category')['quantity'].sum().reset_index()['category'].tolist()
    assert 'City' in result['result_df_top10'].columns  # Check for presence of city column
    assert len(result['result_df_top10']) <= 10  # Top 10 cities


def test_overview_date_filter(mock_tables):
    filter = {}
    filter = sidbar.visuals().slicers()

    # This Handled in UI, so rewrite it here again:
    if mock_tables['sales']['date'][9] < mock_tables['sales']['date'][876]:
        filter['selected_start_date'] = mock_tables['sales']['date'][9] #Random Date
        filter['selected_end_date'] = mock_tables['sales']['date'][876] #Random Date
    else:
        filter['selected_start_date'] = mock_tables['sales']['date'][876] #Random Date
        filter['selected_end_date'] = mock_tables['sales']['date'][9] #Random Date

    result = overviewSubpage.overview(filter)

    filtered_table= mock_tables['full_merged_data'][(mock_tables['full_merged_data']['date'] >= filter['selected_start_date']) & (mock_tables['full_merged_data']['date'] <= filter['selected_end_date'])]


    assert result['date'] == True
    assert result['category']  == False
    assert result['subcategory']  == False
    assert result['productid']  == False
    assert result['city']  == False
    assert result['rating']  == False

    # Assert expected values for cards based on mock data
    assert result['card1'] == filtered_table['discounted_price'].sum()
    assert result['card2'] == filtered_table['quantity'].sum()
    assert result['card3'] == filtered_table['rating'].mean()
    assert result['card4'] == filtered_table['customer_id'].nunique()

    # Assert visuals 
    assert result['visual_2']['Category'].tolist() == filtered_table.groupby('category')['quantity'].sum().reset_index()['category'].tolist()
    assert 'City' in result['result_df_top10'].columns  # Check for presence of city column
    assert len(result['result_df_top10']) <= 10  # Top 10 cities


def test_overview_subcategory_filter(mock_tables):
    filter = {}
    filter = sidbar.visuals().slicers()

    filter['selected_subcategory'] = mock_tables['product']['sub_category'][18] #Random subcategory
    
    result = overviewSubpage.overview(filter)

    filtered_table= mock_tables['full_merged_data'][mock_tables['full_merged_data']['sub_category'] == filter.get('selected_subcategory')]


    assert result['date'] == False
    assert result['category']  == False
    assert result['subcategory']  == True
    assert result['productid']  == False
    assert result['city']  == False
    assert result['rating']  == False

    # Assert expected values for cards based on mock data
    assert result['card1'] == filtered_table['discounted_price'].sum()
    assert result['card2'] == filtered_table['quantity'].sum()
    assert result['card3'] == filtered_table['rating'].mean()
    assert result['card4'] == filtered_table['customer_id'].nunique()

    # Assert visuals 
    assert result['visual_2']['Category'].tolist() == filtered_table.groupby('category')['quantity'].sum().reset_index()['category'].tolist()
    assert 'City' in result['result_df_top10'].columns  # Check for presence of city column
    assert len(result['result_df_top10']) <= 10  # Top 10 cities


def test_overview_productid_filter(mock_tables):
    filter = {}
    filter = sidbar.visuals().slicers()

    filter['selected_product'] = mock_tables['product']['product_id'][50] #Random productid
    
    result = overviewSubpage.overview(filter)

    filtered_table= mock_tables['full_merged_data'][mock_tables['full_merged_data']['product_id'] == filter.get('selected_product')]


    assert result['date'] == False
    assert result['category']  == False
    assert result['subcategory']  == False
    assert result['productid']  == True
    assert result['city']  == False
    assert result['rating']  == False

    # Assert expected values for cards based on mock data
    assert result['card1'] == filtered_table['discounted_price'].sum()
    assert result['card2'] == filtered_table['quantity'].sum()
    assert result['card3'] == filtered_table['rating'].mean()
    assert result['card4'] == filtered_table['customer_id'].nunique()

    # Assert visuals 
    assert result['visual_2']['Category'].tolist() == filtered_table.groupby('category')['quantity'].sum().reset_index()['category'].tolist()
    assert 'City' in result['result_df_top10'].columns  # Check for presence of city column
    assert len(result['result_df_top10']) <= 10  # Top 10 cities



def test_overview_city_filter(mock_tables):
    filter = {}
    filter = sidbar.visuals().slicers()

    filter['selected_city'] = mock_tables['customer']['city'][73] #Random city
    
    result = overviewSubpage.overview(filter)

    filtered_table= mock_tables['full_merged_data'][mock_tables['full_merged_data']['city'] == filter.get('selected_city')]


    assert result['date'] == False
    assert result['category']  == False
    assert result['subcategory']  == False
    assert result['productid']  == False
    assert result['city']  == True
    assert result['rating']  == False

    # Assert expected values for cards based on mock data
    assert result['card1'] == filtered_table['discounted_price'].sum()
    assert result['card2'] == filtered_table['quantity'].sum()
    assert result['card3'] == filtered_table['rating'].mean()
    assert result['card4'] == filtered_table['customer_id'].nunique()

    # Assert visuals 
    assert result['visual_2']['Category'].tolist() == filtered_table.groupby('category')['quantity'].sum().reset_index()['category'].tolist()
    assert 'City' in result['result_df_top10'].columns  # Check for presence of city column
    assert len(result['result_df_top10']) <= 10  # Top 10 cities


def test_overview_rating_filter(mock_tables):
    filter = {}
    filter = sidbar.visuals().slicers()

    # This Handled in UI, so rewrite it here again:
    if mock_tables['review']['rating'][69] < mock_tables['review']['rating'][356]:
        filter['selected_min_rating'] = mock_tables['review']['rating'][69] #Random rating
        filter['selected_max_rating'] = mock_tables['review']['rating'][876] #Random rating
    else:
        filter['selected_min_rating'] = mock_tables['review']['rating'][356] #Random rating
        filter['selected_max_rating'] = mock_tables['review']['rating'][69] #Random rating
    
    result = overviewSubpage.overview(filter)

    filtered_table = mock_tables['full_merged_data'][(mock_tables['full_merged_data']['rating'] >= filter.get('selected_min_rating')) & (mock_tables['full_merged_data']['rating'] <= filter.get('selected_max_rating'))]


    assert result['date'] == False
    assert result['category']  == False
    assert result['subcategory']  == False
    assert result['productid']  == False
    assert result['city']  == False
    assert result['rating']  == True

    # Assert expected values for cards based on mock data
    assert result['card1'] == filtered_table['discounted_price'].sum()
    assert result['card2'] == filtered_table['quantity'].sum()
    assert result['card3'] == filtered_table['rating'].mean()
    assert result['card4'] == filtered_table['customer_id'].nunique()

    # Assert visuals 
    assert result['visual_2']['Category'].tolist() == filtered_table.groupby('category')['quantity'].sum().reset_index()['category'].tolist()
    assert 'City' in result['result_df_top10'].columns  # Check for presence of city column
    assert len(result['result_df_top10']) <= 10  # Top 10 cities


def test_overview_all_filter(mock_tables):
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
    

    result = overviewSubpage.overview(filter)
    
    
    filtered_table= mock_tables['full_merged_data'][mock_tables['full_merged_data']['category'] == filter.get('selected_category')]
    filtered_table = filtered_table[(filtered_table['rating'] >= filter.get('selected_min_rating')) & (filtered_table['rating'] <= filter.get('selected_max_rating'))]
    filtered_table= filtered_table[(filtered_table['date'] >= filter['selected_start_date']) & (filtered_table['date'] <= filter['selected_end_date'])]
    filtered_table= filtered_table[filtered_table['sub_category'] == filter.get('selected_subcategory')]
    filtered_table= filtered_table[filtered_table['product_id'] == filter.get('selected_product')]
    filtered_table= filtered_table[filtered_table['city'] == filter.get('selected_city')]

    assert result['date'] == True
    assert result['category']  == True
    assert result['subcategory']  == True
    assert result['productid']  == True
    assert result['city']  == True
    assert result['rating']  == True

    # Assert expected values for cards based on mock data
    assert result['card1'] == filtered_table['discounted_price'].sum()
    assert result['card2'] == filtered_table['quantity'].sum()
    
    # based on selected filters the result is nan, so this is a handle to nan results:
    if filtered_table['rating'].empty:
        assert np.isnan(result['card3'])
    else:
        assert result['card3'] == filtered_table['rating'].mean()

    assert result['card4'] == filtered_table['customer_id'].nunique()

    # Assert visuals 
    assert result['visual_2']['Category'].tolist() == filtered_table.groupby('category')['quantity'].sum().reset_index()['category'].tolist()
    assert 'City' in result['result_df_top10'].columns  # Check for presence of city column
    assert len(result['result_df_top10']) <= 10  # Top 10 cities


