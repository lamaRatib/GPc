import pytest
import pandas as pd
import db 
import performanceSubpage, sidbar


@pytest.fixture
def mock_tables():
    return {
        'sales': db.sales,
        'full_merged_data': db.full_merged_data,
        'review': db.review,
        'product': db.products,
        'customer': db.customer,
    }


def test_performance_no_filters(mock_tables):
    """
        Tests performance function with no filters applied.
    """
    filter = {}
    filter = sidbar.visuals().slicers() # will return selected as = 'All'
    result = performanceSubpage.performance(filter)
            
    expected_df_visual1=  mock_tables['sales'].groupby('date')['discounted_price'].sum().reset_index()
    expected_df_visual1.rename(columns={'date': 'Date', 'discounted_price':'Total Sales'}, inplace=True)

    mock_tables['sales']['Price']= mock_tables['sales']['discounted_price'] / mock_tables['sales']['quantity']
    expected_df_visual2= mock_tables['sales'].groupby('product_id')['Price'].mean().reset_index()
    
    assert result['date'] == False
    assert result['category']  == False
    assert result['subcategory']  == False
    assert result['productid']  == False
    assert result['city']  == False
    assert result['rating']  == False

    # Assert visuals 
    pd.testing.assert_frame_equal(result['visual_1'], expected_df_visual1)
    pd.testing.assert_frame_equal(result['visual_2'], expected_df_visual2)
    

def test_performance_category_filter(mock_tables):
    filter = {}
    filter = sidbar.visuals().slicers()

    filter['selected_category'] = mock_tables['product']['category'][54] #Random category
    
    result = performanceSubpage.performance(filter)

    filtered_table= mock_tables['full_merged_data'][mock_tables['full_merged_data']['category'] == filter.get('selected_category')]

    expected_df_visual1=  filtered_table.groupby('date')['discounted_price'].sum().reset_index()
    expected_df_visual1.rename(columns={'date': 'Date', 'discounted_price':'Total Sales'}, inplace=True)

    filtered_table['Price']= filtered_table['discounted_price'] / filtered_table['quantity']
    expected_df_visual2= filtered_table.groupby('product_id')['Price'].mean().reset_index()

    assert result['date'] == False
    assert result['category']  == True
    assert result['subcategory']  == False
    assert result['productid']  == False
    assert result['city']  == False
    assert result['rating']  == False

    # Assert visuals 
    pd.testing.assert_frame_equal(result['visual_1'], expected_df_visual1)
    pd.testing.assert_frame_equal(result['visual_2'], expected_df_visual2)


def test_performance_date_filter(mock_tables):
    filter = {}
    filter = sidbar.visuals().slicers()

    # This Handled in UI, so rewrite it here again:
    if mock_tables['sales']['date'][9] < mock_tables['sales']['date'][876]:
        filter['selected_start_date'] = mock_tables['sales']['date'][9] #Random Date
        filter['selected_end_date'] = mock_tables['sales']['date'][876] #Random Date
    else:
        filter['selected_start_date'] = mock_tables['sales']['date'][876] #Random Date
        filter['selected_end_date'] = mock_tables['sales']['date'][9] #Random Date

    result = performanceSubpage.performance(filter)

    filtered_table= mock_tables['full_merged_data'][(mock_tables['full_merged_data']['date'] >= filter['selected_start_date']) & (mock_tables['full_merged_data']['date'] <= filter['selected_end_date'])]

    expected_df_visual1=  filtered_table.groupby('date')['discounted_price'].sum().reset_index()
    expected_df_visual1.rename(columns={'date': 'Date', 'discounted_price':'Total Sales'}, inplace=True)

    filtered_table['Price']= filtered_table['discounted_price'] / filtered_table['quantity']
    expected_df_visual2= filtered_table.groupby('product_id')['Price'].mean().reset_index()

    assert result['date'] == True
    assert result['category']  == False
    assert result['subcategory']  == False
    assert result['productid']  == False
    assert result['city']  == False
    assert result['rating']  == False

    # Assert visuals 
    pd.testing.assert_frame_equal(result['visual_1'], expected_df_visual1)
    pd.testing.assert_frame_equal(result['visual_2'], expected_df_visual2)



def test_performance_subcategory_filter(mock_tables):
    filter = {}
    filter = sidbar.visuals().slicers()

    filter['selected_subcategory'] = mock_tables['product']['sub_category'][76] #Random subcategory
    
    result = performanceSubpage.performance(filter)

    filtered_table= mock_tables['full_merged_data'][mock_tables['full_merged_data']['sub_category'] == filter.get('selected_subcategory')]

    expected_df_visual1=  filtered_table.groupby('date')['discounted_price'].sum().reset_index()
    expected_df_visual1.rename(columns={'date': 'Date', 'discounted_price':'Total Sales'}, inplace=True)

    filtered_table['Price']= filtered_table['discounted_price'] / filtered_table['quantity']
    expected_df_visual2= filtered_table.groupby('product_id')['Price'].mean().reset_index()

    assert result['date'] == False
    assert result['category']  == False
    assert result['subcategory']  == True
    assert result['productid']  == False
    assert result['city']  == False
    assert result['rating']  == False

    # Assert visuals 
    pd.testing.assert_frame_equal(result['visual_1'], expected_df_visual1)
    pd.testing.assert_frame_equal(result['visual_2'], expected_df_visual2)



def test_performance_productid_filter(mock_tables):
    filter = {}
    filter = sidbar.visuals().slicers()

    filter['selected_product'] = mock_tables['product']['product_id'][50] #Random productid
    
    result = performanceSubpage.performance(filter)

    filtered_table= mock_tables['full_merged_data'][mock_tables['full_merged_data']['product_id'] == filter.get('selected_product')]

    expected_df_visual1=  filtered_table.groupby('date')['discounted_price'].sum().reset_index()
    expected_df_visual1.rename(columns={'date': 'Date', 'discounted_price':'Total Sales'}, inplace=True)

    filtered_table['Price']= filtered_table['discounted_price'] / filtered_table['quantity']
    expected_df_visual2= filtered_table.groupby('product_id')['Price'].mean().reset_index()

    assert result['date'] == False
    assert result['category']  == False
    assert result['subcategory']  == False
    assert result['productid']  == True
    assert result['city']  == False
    assert result['rating']  == False

    # Assert visuals 
    pd.testing.assert_frame_equal(result['visual_1'], expected_df_visual1)
    pd.testing.assert_frame_equal(result['visual_2'], expected_df_visual2)



def test_performance_city_filter(mock_tables):
    filter = {}
    filter = sidbar.visuals().slicers()

    filter['selected_city'] = mock_tables['customer']['city'][73] #Random city
    
    result = performanceSubpage.performance(filter)

    filtered_table= mock_tables['full_merged_data'][mock_tables['full_merged_data']['city'] == filter.get('selected_city')]

    expected_df_visual1=  filtered_table.groupby('date')['discounted_price'].sum().reset_index()
    expected_df_visual1.rename(columns={'date': 'Date', 'discounted_price':'Total Sales'}, inplace=True)

    filtered_table['Price']= filtered_table['discounted_price'] / filtered_table['quantity']
    expected_df_visual2= filtered_table.groupby('product_id')['Price'].mean().reset_index()

    assert result['date'] == False
    assert result['category']  == False
    assert result['subcategory']  == False
    assert result['productid']  == False
    assert result['city']  == True
    assert result['rating']  == False

    # Assert visuals 
    pd.testing.assert_frame_equal(result['visual_1'], expected_df_visual1)
    pd.testing.assert_frame_equal(result['visual_2'], expected_df_visual2)


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
    
    result = performanceSubpage.performance(filter)

    filtered_table = mock_tables['full_merged_data'][(mock_tables['full_merged_data']['rating'] >= filter.get('selected_min_rating')) & (mock_tables['full_merged_data']['rating'] <= filter.get('selected_max_rating'))]

    expected_df_visual1=  filtered_table.groupby('date')['discounted_price'].sum().reset_index()
    expected_df_visual1.rename(columns={'date': 'Date', 'discounted_price':'Total Sales'}, inplace=True)

    filtered_table['Price']= filtered_table['discounted_price'] / filtered_table['quantity']
    expected_df_visual2= filtered_table.groupby('product_id')['Price'].mean().reset_index()

    assert result['date'] == False
    assert result['category']  == False
    assert result['subcategory']  == False
    assert result['productid']  == False
    assert result['city']  == False
    assert result['rating']  == True

    # Assert visuals 
    pd.testing.assert_frame_equal(result['visual_1'], expected_df_visual1)
    pd.testing.assert_frame_equal(result['visual_2'], expected_df_visual2)



def test_performance_all_filter(mock_tables):
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
    

    result = performanceSubpage.performance(filter)
    
    
    filtered_table= mock_tables['full_merged_data'][mock_tables['full_merged_data']['category'] == filter.get('selected_category')]
    filtered_table = filtered_table[(filtered_table['rating'] >= filter.get('selected_min_rating')) & (filtered_table['rating'] <= filter.get('selected_max_rating'))]
    filtered_table= filtered_table[(filtered_table['date'] >= filter['selected_start_date']) & (filtered_table['date'] <= filter['selected_end_date'])]
    filtered_table= filtered_table[filtered_table['sub_category'] == filter.get('selected_subcategory')]
    filtered_table= filtered_table[filtered_table['product_id'] == filter.get('selected_product')]
    filtered_table= filtered_table[filtered_table['city'] == filter.get('selected_city')]


    expected_df_visual1=  filtered_table.groupby('date')['discounted_price'].sum().reset_index()
    expected_df_visual1.rename(columns={'date': 'Date', 'discounted_price':'Total Sales'}, inplace=True)

    filtered_table['Price']= filtered_table['discounted_price'] / filtered_table['quantity']
    expected_df_visual2= filtered_table.groupby('product_id')['Price'].mean().reset_index()

    assert result['date'] == True
    assert result['category']  == True
    assert result['subcategory']  == True
    assert result['productid']  == True
    assert result['city']  == True
    assert result['rating']  == True
   
    # Assert visuals 
    pd.testing.assert_frame_equal(result['visual_1'], expected_df_visual1)
    pd.testing.assert_frame_equal(result['visual_2'], expected_df_visual2)
    


