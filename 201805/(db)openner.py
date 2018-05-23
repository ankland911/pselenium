import mysql.connector
from mysql.connector import errorcode
db_host = 'ankland911.gotoip3.com'
db_user = 'ankland911'
db_pass = 'kuailong88'
db_database = 'ankland911'

def create_opener():
	try:
		opener = mysql.connector.connect(user=db_user,password=db_pass,host=db_host,database=db_database)
		return opener
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Something is wrong with your user name or password")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("Database does not exist")
		else:
			print(err)
	else:
		opener.close()


class executer:
	def __init__(self,opener,tableName):
		self.OPENER = opener
		self.TABLE = tableName
		self.WHERE = ''
		self.FIELD = '*'
		self.CURSOR = opener.cursor()

	def field(self,fields):
		if(isinstance(fields,str)):
			self.FIELD = fields

	def where(self,conditions):
		where = []
		if(isinstance(conditions,dict)):
			for key in conditions:
				where.append("%s='%s'" % (key,conditions[key]))
			self.WHERE = ' and '.join(where)
		if(isinstance(conditions,str)):
			self.WHERE = conditions

	def select(self):
		sql = "select %s from %s" % (self.FIELD,self.TABLE)
		if(self.WHERE !=""):
			sql += " where %s" % (self.WHERE)
		return self.query(sql)

	def update(self,values={}):
		_data=[]
		if(isinstance(values,dict)):
			for key in values:
				_data.append("%s='%s'" % (key,values[key]))
		sql = "update %s set %s where %s" % (self.TABLE,' and '.join(_data),self.WHERE)
		self.commit(sql)

	def insert(self,values={}):
		_key,_value=[]
		if(isinstance(values,dict)):
			for key in values:
				_key.append(str(key))
				_value.append("'%s'" % (values[key]))
		sql = "insert into %s (%s) values (%s)" % (self.TABLE,','.join(key),','.join(_value))
		self.commit(sql)

	def count(self):
		sql = "select count(*) from %s" % (self.TABLE)
		if(self.WHERE != ''):
			sql += " where %s" % (self.WHERE)
		return self.query(sql)

	def query(self,sql):
		if not (self.OPENER.is_connected()):
			self.OPENER.reconnect()
		self.CURSOR.execute(sql)
		self.WHERE = ''
		self.FIELD = ''
		result = []
		for line in self.CURSOR.fetchall():
			result.append(line)
		return result

	def commit(self,sql):
		if not (self.OPENER.is_connected()):
			self.OPENER.reconnect()
		self.CURSOR.execute(sql)
		self.WHERE = ''
		self.FIELD = ''
		self.OPENER.commit()
