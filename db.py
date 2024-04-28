import MySQLdb
import MySQLdb.cursors
import pandas as pd
# Connection to MySQL class:

class DB:
  conn = None

  def connect(self):
    # Connetion func to connet to DB
    self.conn = MySQLdb.connect(host='localhost', user='root', password='0000', database='amazonsales', cursorclass=MySQLdb.cursors.SSCursor)

  def query(self, sql):
    # This for execute the sql statement in db and return the results
    try:
     cursor = self.conn.cursor()
     cursor.execute(sql)
    except (AttributeError, MySQLdb.OperationalError):
     self.connect()
     cursor = self.conn.cursor()
     cursor.execute(sql)

    return cursor

  def get_sales(self):
    sql="SELECT * FROM sales;"
    query=self.query(sql)
    sales=pd.DataFrame(query,columns=['sale_id','product_id','discounted_price','actual_price','discounted_percentage','customer_id','date','quantity'])
    return sales
  
  def get_product(self):
    sql="SELECT * FROM products;"
    query=self.query(sql)
    product=pd.DataFrame(query,columns=['product_id','product_name','category','sub_category'])
    return product
  
  def get_customer(self):
    sql="SELECT * FROM customer;"
    query=self.query(sql)
    customer=pd.DataFrame(query,columns=['customer_id','customer_name','city'])
    return customer
  
  def get_review(self):
    sql="SELECT * FROM review;"
    query=self.query(sql)
    review=pd.DataFrame(query,columns=['review_id','product_id','customer_id','review_title','review_content','rating'])
    return review
    
  def cleaning(self,df):
    # Cleaning the resulting of query func
    pass

datab=DB()
sales=datab.get_sales()
products=datab.get_product()
customer=datab.get_customer()
review=datab.get_review()

# Joins:
sales_product = pd.merge(sales, products, on='product_id', how='inner')
sales_product_customer = pd.merge(sales_product, customer, on='customer_id', how='inner')
sales_product_customer_review = pd.merge(sales_product_customer, review, on=['product_id', 'customer_id'], how='inner')
review_product=pd.merge(review, products, on='product_id', how='inner')
review_product_customer= pd.merge(review_product, customer, on='customer_id', how='inner')
