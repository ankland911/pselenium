# -*- coding: UTF-8 -*- 
from lib.IOdevice import IOdevice
from lib.Linker import Linker
from lib.MyDb import MyDb
import urllib2
from ftplib import FTP

class interface(Linker):
	
	def __init__(self):
		Linker.__init__(self)
		print "initial:     start a interface instance OK..."

	def get_article_title(self):
		element_title = self.webbrowser.find_element_by_class_name("title").find_element_by_tag_name("h1")
		title = element_title.text
		print "title:%s" % title
		return title

	def get_article_description(self):
		element_description = self.webbrowser.find_element_by_class_name("detailTxt").find_elements_by_tag_name("p")
		i = 0
		description = element_description[i].text
		while (u'\u58f0\u660e' in description):
			i=i+1
			description = element_description[i].text
		print "description:%s" % description
		return description

	def get_article_image(self):
		element_title_image = self.webbrowser.find_element_by_class_name("detailTxt").find_element_by_tag_name("img")
		return element_title_image.get_attribute("src")


	def GetDetail(self,pageid):
		Details=[]
		lists=self.webbrowser.find_element_by_class_name("detailTxt").find_elements_by_tag_name("p")
		for D in lists:
			try:
				Details.append({'page_id':pageid,'type':'img','detail':D.find_element_by_tag_name("img").get_attribute("src")})
			except Exception:
				if(D.text==''):
					continue
				Details.append({'type':'txt','Page_id':pageid,'detail':D.text})
		return Details




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
		#self.ftp.set_debuglevel(2)
		self.ftp.connect("ankland911.gotoip3.com","21")
		self.ftp.login("ankland911","kuailong88")
		# print self.ftp.getwelcome()
		self.ftp.cwd("/wwwroot/Public/jiongtu")
		self.bufsize=1024
		print "initial:     start a ftp client instance OK..."
		
	def ftp_upload(self,file_handle,filename):
		self.ftp.storbinary("STOR %s" % filename,file_handle,self.bufsize)

	def __del__(self):
		self.ftp.quit()

if __name__ == '__main__':
	# try:
	data = {}
	where = {}
	app = interface()
	ftp = ftp_client()
	db = MyDb({"host":"ankland911.gotoip3.com","user":"ankland911","pass":"kuailong88","db":"ankland911"})
	# step 1:
	article_links = db.Model("article_links").SQL("select copy_link,article_id from article_links limit 1")

	for article_link in article_links:
		print "   start:    article id=%s" % article_link[1]
		app.Get(article_link[0])
		data['detail']=app.get_article_description()
		data['title']=app.get_article_title()
		image_name = app.get_picture(app.get_article_image())
		file_handle = open("jiongtu/%s" % image_name,"r")
		ftp.ftp_upload(file_handle,image_name)
		data['imagepath'] = '/Public/jiongtu/%s' % image_name
		where['article_id'] = article_link[1]
		rs = db.Model('article_links').where(where).update(data)
		# step 2:
		pages = db.Model('pages').SQL(("select link,page_id from pages where article_id=\'%s\'" % article_link[1]))


		for page in pages:
			print "   start:    page_id=%s" % page[1]

			#step 3:
			detailtxts = db.Model('detailtxt').SQL(("select detail_id,type from detailtxt where page_id=\'%s\'" % page[1]))	


			if(detailtxts==()):
				detailtxts=[]
				details = app.GetDetail(page[1])
				for detail in details:
					rs = db.Model('detailtxt').field('max(detail_id)').select()
					max_detail_id = int(rs[0][0])
					detail['detail_id'] = str(max_detail_id+10).zfill(8)
					if(detail['type']=='txt'):
						rs = db.Model('detailtxt').insert(detail)
					elif(detail['type']=='img'):
						rs = db.Model('downimage').insert(detail)
						detail['detail']= ''
						rs = db.Model('detailtxt').insert(detail)
					print "do get detail result="+str(bool(rs))+"; detail_id="+detail['detail_id']+"; type="+detail['type']
					detailtxts.append([unicode(detail['detail_id']),unicode(detail['type'])])

			sort_id = 1
			for detailtxt in detailtxts:
				print "   start:    detail_id="+detailtxt[0]
				where={}
				where['detail_id'] = detailtxt[0]
				if(detailtxt[1]=='img'):
					#step 4:
					image = db.Model('downimage').where(where).field('detail').select()
					link_downimage = image[0][0]
					image_name_downimage = app.get_picture(link_downimage)
					file_handle = open("jiongtu/%s" % image_name_downimage,"r")
					ftp.ftp_upload(file_handle,image_name_downimage)
					data={}
					data['path'] = '/Public/jiongtu/%s' % image_name_downimage
					rs = db.Model('downimage').where(where).update(data)
					print 'change downimage path'+str(rs) + '  '+detailtxt[0]+'   '+data['path']
		#print "result : %s" % rs
		#print db.Model('article_links').option['lastsql']

	#print app.get_article_image()
	
	app.quit()
	del db
	del ftp
	raw_input()
	# except Exception, e:
	# 	print str(e)
	# 	raw_input()



	

