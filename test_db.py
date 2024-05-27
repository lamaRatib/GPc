import db


def test_get_sales():
    db_instance = db.DB()
    sales = db_instance.get_sales()

    assert not sales.empty
    expected_columns = ['sale_id', 'product_id', 'discounted_price', 'actual_price', 'discounted_percentage', 'customer_id', 'date', 'quantity']
    assert list(sales.columns) == expected_columns
    
        
def test_get_product():
    db_instance = db.DB()
    products = db_instance.get_product()
    
    assert not products.empty
    expected_columns = ['product_id', 'product_name', 'category', 'sub_category']
    assert list(products.columns) == expected_columns


def test_get_customer():
    db_instance = db.DB()
    customers = db_instance.get_customer()
    
    assert not customers.empty    
    expected_columns = ['customer_id', 'customer_name', 'city']
    assert list(customers.columns) == expected_columns


def test_get_review():
    db_instance = db.DB()    
    reviews = db_instance.get_review()
    
    assert not reviews.empty    
    expected_columns = ['review_id', 'product_id', 'customer_id', 'review_title', 'review_content', 'rating']
    assert list(reviews.columns) == expected_columns

def test_full_join():
    db_instance = db.DB()
    sales = db_instance.get_sales()
    products = db_instance.get_product()
    customers = db_instance.get_customer()
    reviews = db_instance.get_review()
    
    full_merged_data = db.full_merged_data
    
    assert not full_merged_data.empty
    
    expected_columns = list(sales.columns) + list(products.columns) + list(customers.columns) + list(reviews.columns)
    assert set(full_merged_data.columns) == set(expected_columns)

