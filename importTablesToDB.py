import pandas as pd
from sqlalchemy import create_engine

# File path of your Excel file
excel_file = 'C:/Users/Admin/Desktop/GP/finaldividedtables.xlsx'

# Read Excel data into a pandas DataFrame
df = pd.read_excel(excel_file)

# MySQL connection parameters
db_username = 'root'
db_password = '0000'
db_host = 'localhost'  # or your host
db_name = 'amazonsales'


# Create SQLAlchemy engine to connect to MySQL database
engine = create_engine(f'mysql+mysqlconnector://{db_username}:{db_password}@{db_host}/{db_name}')


tables_to_import = ['Products', 'Sales', 'Customer', 'Review']  # Replace with the names of your tables
for table_name in tables_to_import:
    # Read data from Excel
    df = pd.read_excel(excel_file, sheet_name=table_name)
    # Insert data into MySQL database
    df.columns = df.columns.str.strip()
    df.to_sql(table_name.lower(), con=engine, if_exists='replace', index=False)


# Close the database connection
engine.dispose()

print("Data has been imported successfully into MySQL database.")
