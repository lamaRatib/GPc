import MySQLdb
import MySQLdb.cursors


class DB:
  conn = None

  def connect(self):
    self.conn = MySQLdb.connect(host='localhost', user='root', password='0000', database='amazonsales', cursorclass=MySQLdb.cursors.SSCursor)

  def query(self, sql):
    try:
     cursor = self.conn.cursor()
     cursor.execute(sql)
    except (AttributeError, MySQLdb.OperationalError):
     self.connect()
     cursor = self.conn.cursor()
     cursor.execute(sql)

    return cursor
  
