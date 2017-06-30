# -*- coding: UTF-8 -*-
import MySQLdb,traceback
class db(object):
	"""docstring for db"""
	def __init__(self, db_owner):
		super(db, self).__init__()
		self.db_owner = db_owner
		try:	
			self.connect()
			self.Cursor = self.Db.cursor()
		except Exception, e:
			traceback.print_exc()

	def connect(self):
		try:
			self.Db = MySQLdb.connect(host=self.db_owner["host"],user=self.db_owner["user"],passwd=self.db_owner["pass"],db=self.db_owner["db"],charset="utf8")
		except Exception,e:
			traceback.print_exc()

	def query(self,sql):
		try:
			if not self.Db.ping():
				self.connect()
		 	if self.Cursor.execute(sql):
				return self.Cursor.fetchall()
		except Exception as e:
			traceback.print_exc()

	def commit(self,sql):
		try:
			if not self.Db.ping():
				self.connect()
		 	rs = self.Cursor.execute(sql)
		 	if rs:
				self.Db.commit()
			return rs
		except Exception as e:
			traceback.print_exc()

class Model(object):
	"""docstring for Model"""
	def __init__(self, tableName):
		super(Model, self).__init__()
		self.TABLE_NAME = tableName
		self.WHERE = ""
		self.FIELD = "*"
		self.option = {}
		self.LastSql = ''
		self.db = db({"host":"ankland911.gotoip3.com","user":"ankland911","pass":"kuailong88","db":"ankland911"})
		self._getFields()

	def _getFields(self):
		try:
			self.option['fields'] = []
			sql = "SHOW COLUMNS FROM %s" % self.TABLE_NAME
			Result = self.db.query(sql)
			for line in Result:
				self.option['fields'].append(line[0])
		except Exception,e:
			traceback.print_exc()

	def _cleanCondition(self):
		self.option['lastsql'] = sql
		self.WHERE = ""
		self.FIELD = "*"

	def field(self,fields):
		if(isinstance(fields,str)):
			self.FIELD = fields
		return self

	def where(self,condition):
		if(isinstance(condition,dict)):
			for key in condition:
				if(self.WHERE==""):
					self.WHERE += "%s='%s'" % (key,condition[key])
				else:
					self.WHERE += " and %s='%s'" % (key,condition[key])
		elif(isinstance(condition,str)):
			self.WHERE = condition
		return self

	def sql_query(self,sql):
		return self.db.query(sql)

	def sql_exec(self,sql):
		return self.db.commit(sql)

	def select(self):
		sql = "select %s from %s" % (self.FIELD,self.TABLE_NAME)
		if(self.WHERE != ""):
			sql += " where %s" % (self.WHERE)
		return self.db.query(sql)

	def update(self,values={}):
		if not (isinstance(values,dict)):
			return -1
		if (self.WHERE==""):
			return -2
		sql="update %s " % (self.TABLE_NAME)
		sql+="set "
		_data = []
		for key in values:
			_data.append("%s='%s'" % (key,values[key]))
		_set = ",".join(_data)
		sql += _set
		sql+=" where %s" % (self.WHERE)
		return self.db.commit(sql)

	def insert(self,values={}):
		if not (isinstance(values,dict)):
			return -1
		sql="insert into %s " % (self.TABLE_NAME)
		_key=[]
		_value=[]
		for key in values:
			_key.append(str(key))
			_value.append("'%s'" % (values[key]))
		sql+="(%s) values (%s)" % (",".join(_key),",".join(_value))
		return self.db.commit(sql)

	def count(self):
		sql = "select count(*) from %s" % (self.TABLE_NAME)
		if(self.WHERE != ""):
			sql+=" where %s" % (self.WHERE)
		Rs = self.db.query(sql)
		return Rs[0][0]

	def delete(self):
		sql = "delete from %s" % (self.TABLE_NAME)
		if(self.WHERE != ""):
			sql+=" where %s" % (self.WHERE)
		return self.db.commit(sql)

# if __name__ == '__main__':
# 	model = Model('article_links').where("1=1").select()
# 	print ("field0 : ",model[0][2])
		 	
