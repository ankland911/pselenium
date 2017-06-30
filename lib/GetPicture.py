# -*- coding: UTF-8 -*- 
import urllib2
from ftplib import FTP
class GetPicture(object):
	"""docstring for GetPicture"""
	def __init__(self):
		super(GetPicture, self).__init__()
		self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'}

	def get_pic_from_link(self,link,path):
		response = urllib2.urlopen(urllib2.Request(link, None, self.header))
		name = link.split("/")
		name = name[len(name)-1]
		file_name = '{0}/{1}'.format(patn,name)
		with open(file_name,"wb") as file:
			file.write(response.read())
			ftp = FtpCli(file,file_name)
		return file_name

class FtpCli(object):
	"""docstring for FtpCli"""
	def __init__(self, file_handle , filename):
		super(FtpCli, self).__init__()
		self.file_handle = file_handle
		self.filename = filename

	def up_load(self):
		HOST = 'ankland911.gotoip3.com'
		PORT = '21' 
		USER = 'username'
		PASS = 'password'
		DIRN = '/wwwroot/Public/jiongtu'
		self.ftp = FTP()
		self.ftp.connect(HOST,PORT)
		self.ftp.login(USER,PASS)
		self.ftp.cwd(DIRN)
		bufsize=1024
		self.ftp.storbinary("STOR %s" % self.filename,self.file_handle,bufsize)

	def __del__(self):
		self.ftp.quit()
		
