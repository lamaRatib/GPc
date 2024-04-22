import MySQLdb
import MySQLdb.cursors

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
  
  def cleaning(self,df):
    # Cleaning the resulting of query func
    pass

  
