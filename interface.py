# -*- coding: UTF-8 -*- 
from lib.IOdevice import IOdevice
from lib.Linker import Linker
from lib.MyDb import MyDb
import urllib2
from ftplib import FTP

class STATE_NOTICE():
	def __init__(self):
		self.type=""
		self.info=""
	def print_notice(self,etype,einfo):
		self.type = etype
		self.info = einfo
		print("%12s:    %s" % (self.type,self.info))



class interface(Linker):
	
	def __init__(self,notice_instance):
		Linker.__init__(self)
		self.notice_ins = notice_instance
		self.notice_ins.print_notice('initial','start a interface instance OK...')
		# print "initial:     start a interface instance OK..."

	def get_article_title(self):
		element_title = self.webbrowser.find_element_by_class_name("title").find_element_by_tag_name("h1")
		title = element_title.text
		# print "title:%s" % title
		self.notice_ins.print_notice('article','get_article_title')
		return title

	def get_article_description(self):
		element_description = self.webbrowser.find_element_by_class_name("detailTxt").find_elements_by_tag_name("p")
		i = 0
		description = element_description[i].text
		while (u'\u58f0\u660e' in description):
			i=i+1
			description = element_description[i].text
		self.notice_ins.print_notice('article','get_article_description')
		# print "description:%s" % description
		return description

	def get_article_image(self):
		element_title_image = self.webbrowser.find_element_by_class_name("detailTxt").find_element_by_tag_name("img")
		self.notice_ins.print_notice('article','get_article_image')
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

	def GetPages(self,article_id):
		pages = []
		data={}
		lists = self.webbrowser.find_element_by_id("pages").find_elements_by_tag_name("a")
		for p in lists:
			data['link'] = p.get_attribute("href")
			data['category'] = '0' 
			max_page_id = M('pages').field('max(page_id)').select()
			data['page_id'] = str(int(max_page_id[0][0])+10).zfill(8)
			data['article_id'] = article_id
			pages.append(data)
			# rs = M('pages').insert(data)
		return pages




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
	def __init__(self,notice_instance):
		self.ftp = FTP()
		#self.ftp.set_debuglevel(2)
		self.ftp.connect("ankland911.gotoip3.com","21")
		self.ftp.login("ankland911","kuailong88")
		# print self.ftp.getwelcome()
		self.ftp.cwd("/wwwroot/Public/jiongtu")
		self.bufsize=1024
		self.notice_ins = notice_instance
		self.notice_ins.print_notice('initial','start a ftp client instance OK...')
		# print "initial:     start a ftp client instance OK..."
		
	def ftp_upload(self,file_handle,filename):
		try:
			self.ftp.storbinary("STOR %s" % filename,file_handle,self.bufsize)
		except Exception,e:
			print str(e)
			raw_input()
			self.__init__()

	def __del__(self):
		self.ftp.quit()

if __name__ == '__main__':
	# try:
	data = {}
	where = {}
	error_notice = STATE_NOTICE()
	app = interface(error_notice)
	ftp = ftp_client(error_notice)
	db = MyDb({"host":"ankland911.gotoip3.com","user":"ankland911","pass":"kuailong88","db":"ankland911"},error_notice)
	# step 1:
	article_links = db.Model("article_links").SQL("select copy_link,article_id from article_links limit 1")

	for article_link in article_links:
		article_id = article_link[1]
		error_notice.print_notice('start',("article id=%s" % article_id))
		# print "   start:    article id=%s" % article_id
		app.Get(article_link[0])
		data['detail']=app.get_article_description()
		data['title']=app.get_article_title()
		image_name = app.get_picture(app.get_article_image())
		file_handle = open("jiongtu/%s" % image_name,"r")
		ftp.ftp_upload(file_handle,image_name)
		data['imagepath'] = '/Public/jiongtu/%s' % image_name
		where['article_id'] = article_id
		rs = db.Model('article_links').where(where).update(data)

		# step 2:
		pages = db.Model('pages').SQL(("select link,page_id from pages where article_id=\'%s\'" % article_id))
		if(pages==()):
			rs = app.GetPages(article_id)
			for r in rs:
				rs = db.Model('pages').insert(r)
				error_notice.print_notice('insertPages',r['page_id'])
			pages = db.Model('pages').SQL(("select link,page_id from pages where article_id=\'%s\'" % article_id))


		for page in pages:
			error_notice.print_notice('start',("page_id=%s" % page[1]))
			# print "   start:    page_id=%s" % page[1]
			# self.notice_ins.print_notice('start',('page_id=%s' % page[1]))

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
					error_notice.print_notice('result',"do get detail result="+str(bool(rs))+"; detail_id="+detail['detail_id']+"; type="+detail['type'])
					detailtxts.append([unicode(detail['detail_id']),unicode(detail['type'])])

			sort_id = 1
			for detailtxt in detailtxts:
				error_notice.print_notice('start',("detail_id=%s" % detailtxt[0]))
				# print "   start:    detail_id="+detailtxt[0]
				where={}
				where['detail_id'] = detailtxt[0]
				if(detailtxt[1]=='img'):
					#step 4:
					image = db.Model('downimage').where(where).field('detail').select()
					if(image==()):
						pass
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



	

