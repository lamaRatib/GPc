import database.db as db 


def performance(filter): 

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


    re = {}

    # Visual 1:
    if category or subcategory or productid or city or rating or date:
        visual_1 = filtered_table.groupby('date')['discounted_price'].sum().reset_index()
    else:
        visual_1 = db.sales.groupby('date')['discounted_price'].sum().reset_index()
        
    visual_1.rename(columns={'date': 'Date', 'discounted_price':'Total Sales'}, inplace=True)

    re['visual_1'] = visual_1
    

    # Visual 2:
    if category or subcategory or productid or city or rating or date:
        if 'Price' not in filtered_table:
            filtered_table['Price']= filtered_table['discounted_price'] / filtered_table['quantity']
        visual_2 = filtered_table.groupby('product_id')['Price'].mean().reset_index()
    else:
        db.sales['Price']= db.sales['discounted_price'] / db.sales['quantity']
        visual_2= db.sales.groupby('product_id')['Price'].mean().reset_index()
    
    re['visual_2'] = visual_2

    
    # Visual 3:
    Target= 30000000
    Total_sales=db.sales['discounted_price'].sum()

    re['Target'] = Target
    re['Total_sales'] = Total_sales


    re['date'] = date
    re['category'] = category
    re['subcategory'] = subcategory
    re['productid'] = productid
    re['city'] = city
    re['rating'] = rating

    return re


