# -*- coding: UTF-8 -*-
import MySQLdb

class MyDb:
	model = {}
	def __init__(self,db_owner):
		try:			
			self.Db = MySQLdb.connect(host=db_owner["host"],user=db_owner["user"],passwd=db_owner["pass"],db=db_owner["db"],charset="utf8")
			self.Cursor = self.Db.cursor()
		except Exception, e:
			print e
	def Model(self,model_name):
		if not (self.model.has_key(model_name)):
			self.model[model_name] = Model(model_name,self)
		return self.model[model_name]

class Model:
	def __init__(self,table_name,mydb):
		self.TABLE_NAME = table_name
		self.WHERE = ""
		self.FIELD = "*"
		self.option = {}
		self.mydb = mydb
		self._getFields()

	def _getFields(self):
			self.option['fields'] = []
			rs = self.mydb.Cursor.execute("SHOW COLUMNS FROM %s" % self.TABLE_NAME) 
			if(rs):
				Result = self.mydb.Cursor.fetchall()
			for line in Result:
				self.option['fields'].append(line[0])

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

	def SQL(self,sql):
		self.query(sql)
		return self.mydb.Cursor.fetchall()

	def select(self):
		sql = "select %s from %s" % (self.FIELD,self.TABLE_NAME)
		if(self.WHERE != ""):
			sql += " where %s" % (self.WHERE)
		#print sql
		self.query(sql)
		return self.mydb.Cursor.fetchall()

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
		rs = self.query(sql)
		self.mydb.Db.commit()
		return rs

	# def Exist(self,values={}):
	# 	if not (isinstance(values,dict)):
	# 		return False

	def insert(self,values={}):
		if not (isinstance(values,dict)):
			return False
		sql="insert into %s " % (self.TABLE_NAME)
		_key=[]
		_value=[]
		for key in values:
			_key.append(str(key))
			_value.append("'%s'" % (values[key]))
		sql+="(%s) values (%s)" % (",".join(_key),",".join(_value))
		#print sql
		rs = self.query(sql)
		self.mydb.Db.commit()
		return rs

	def count(self):
		sql = "select count(*) from %s" % (self.TABLE_NAME)
		if(self.WHERE != ""):
			sql+=" where %s" % (self.WHERE)
		self.query(sql)
		Rs = self.mydb.Cursor.fetchall()
		return Rs[0][0]

	def delete(self):
		sql = "delete from %s" % (self.TABLE_NAME)
		if(self.WHERE != ""):
			sql+=" where %s" % (self.WHERE)
		rs = self.query(sql)
		self.mydb.Db.commit()
		return rs

	def query(self,sql):
		try:
		 	rs = self.mydb.Cursor.execute(sql)
			self.WHERE = ""
			self.FIELD = ""
			return rs
		except MySQLdb.Error as e:
			if 'MySQL server has gone away' in str(e):
				self.mydb(db_owner)
				print "Mysql gone away but I had reconnect..."
				self.query(sql)
		except Exception as e:
			print str(e)


app = MyDb({"host":"localhost","user":"root","pass":"","db":"ankland911"})
rs = app.Model('categorys').where('id=0').update({'title':'test1','detail':'test1'})
