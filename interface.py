# -*- coding: UTF-8 -*- 
from lib.IOdevice import IOdevice
from lib.Linker import Linker
from lib.MyDb import MyDb
import urllib2
from ftplib import FTP

class interface(Linker):
	
	def __init__(self):
		Linker.__init__(self)

	def get_article_title(self):
		element_title = self.webbrowser.find_element_by_class_name("title").find_element_by_tag_name("h1")
		return element_title.text

	def get_article_description(self):
		element_description = self.webbrowser.find_element_by_class_name("detailTxt").find_element_by_tag_name("p")
		return element_description.text

	def get_article_image(self):
		element_title_image = self.webbrowser.find_element_by_class_name("detailTxt").find_element_by_tag_name("img")
		return element_title_image.get_attribute("src")

	def get_picture(self,link):
		header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'}
		request = urllib2.Request(link, None, header)  
		response = urllib2.urlopen(request)
		name = link.split("/")
		name = name[len(name)-1]
		with open("jiongtu/%s" % name, "wb") as f:
			f.write(response.read())
		print("link:"+link+" file:"+name)
		return name

class ftp_client(object):
	def __init__(self):
		self.ftp = FTP()
		self.ftp.set_debuglevel(2)
		self.ftp.connect("ankland911.gotoip3.com","21")
		self.ftp.login("ankland911","kuailong88")
		print self.ftp.getwelcome()
		self.ftp.cwd("/wwwroot/Public/jiongtu")
		self.bufsize=1024
		
	def ftp_upload(self,file_handle,filename):
		self.ftp.storbinary("STOR %s" % filename,file_handle,self.bufsize)

	def __del__(self):
		self.ftp.quit()

if __name__ == '__main__':
	data = {}
	app = interface()
	ftp = ftp_client()
	db = MyDb({"host":"localhost","user":"root","pass":"toor","db":"ankland911"})
	article_links = db.Model("article_links").SQL("select copy_link,article_id from article_links limit 5")
	for article_link in article_links:
		app.Get(article_link[0])
		data['detail']=app.get_article_description()
		data['title']=app.get_article_title()
		image_name = app.get_picture(app.get_article_image())
		file_handle = open("jiongtu/%s" % image_name,"r")
		ftp.ftp_upload(file_handle,image_name)
		data['imagepath'] = '/Public/jiongtu/%s' % image_name
		
		db.Model('article_links').where('article_id=\'%s\'' % article_link[1]).update(data)

	#print app.get_article_image()
	
	app.quit()
	del db
	del ftp
	raw_input()


	

