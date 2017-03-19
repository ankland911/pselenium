# -*- coding: UTF-8 -*-
from Linker import Linker
# from Queue import Queue
from selenium.webdriver.common.action_chains import ActionChains
from lib.core.MyDb import MyDb
import os
db_owner = {"host":"localhost","user":"root","pass":"","db":"ankland911"}
class IOdevice(Linker):
	#  use different mode:
	#  mode 0 is mysql database
	#  mode 1 is file 
	
	def __init__(self):
		Linker.__init__(self)
		self.mode = 0 
		if(self.mydb = MyDb(db_owner)==False):
			print "MySql Initiation make some errors!"
				
	def quit(self):
		super(IOdevice,self).quit()
		print "IOdevice is release now ..."

	def SQL(self,table,sql):
		return self.mydb.Model(table).SQL(sql)

	def write_dict(self,mydict,table):
		if self.mode == 0:
			self.mydb.Model(table).insert(mydict)
			print "insert id:",mydict.keys()[0],";",mydict[mydict.keys()[0]]	

	def write_dicts(self,mydicts,table):
		for mydict in mydicts:
			self.write_dict(mydict,table)
