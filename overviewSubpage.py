import db 


def overview(filter): 

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

    # Card1: Total Sales
    if date or category or subcategory or productid or city or rating:
        card1 = filtered_table['discounted_price'].sum()
    else:
        card1 = db.sales['discounted_price'].sum() 

    re['card1'] = card1


    # Card2: Number of Products Sold
    if category or subcategory or productid or city or rating or date:
        card2 = filtered_table['quantity'].sum() 
    else:
        card2 = db.sales['quantity'].sum() 

    re['card2'] = card2


    # Card3: Average Rating
    if category or subcategory or productid or city or rating or date:
        card3 = filtered_table['rating'].mean()
    else:
        card3 = db.review['rating'].mean()

    re['card3'] = card3


    # Card4: Number of Customers with applying related filter if exist:
    if category or subcategory or productid or city or rating or date:
        card4 = filtered_table['customer_id'].nunique()
    else:
        card4 = db.customer['customer_id'].nunique()
    
    re['card4'] = card4


    # Visual1:
    # Data preparing & Filter Reflicting:
    if category or subcategory or productid or city or rating or date:
        visual_2 = filtered_table.groupby('category')['quantity'].sum().reset_index()
    else:
        merged_df = db.sales.merge(db.products, on='product_id', how='inner')
        visual_2 = merged_df.groupby('category')['quantity'].sum().reset_index()
    visual_2.rename(columns={'category': 'Category', 'quantity':'Count of Sales'}, inplace=True)

    re['visual_2'] = visual_2


    # Visual2:
    # Data preparing & Filter Reflicting:
    if category or subcategory or productid or city or rating or date:
        visual_1 = filtered_table.groupby('city')['rating'].mean().reset_index()
    else:
        merged_df = db.review.merge(db.products, on='product_id', how='inner')
        merged_df = merged_df.merge(db.customer, on='customer_id', how='inner')
        visual_1 = merged_df.groupby('city')['rating'].mean().reset_index()
    
    result_df_top10 = visual_1.sort_values(by='rating', ascending=False).head(10)
    result_df_top10.rename(columns={'city': 'City', 'rating':'Avg Rating'}, inplace=True)

    re['result_df_top10'] = result_df_top10

    
    re['date'] = date
    re['category'] = category
    re['subcategory'] = subcategory
    re['productid'] = productid
    re['city'] = city
    re['rating'] = rating

    return re
    