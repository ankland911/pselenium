# -*- coding: UTF-8 -*- 
# from lib.IOdevice import IOdevice
from Linker import Linker
from MyDb import MyDb
import urllib2
from ftplib import FTP
import socket
import time
from Queue import Queue

class mTime():
	@staticmethod
	def mtime():
		return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

class STATE_NOTICE():
	@staticmethod
	def print_notice(etype,einfo,ftype='notice'):
		if ftype=='error':
			pass
		contral = 120
		length = len(einfo)
		if(length<contral):
			print("%12s:  %s" % (etype,einfo))
		else:
			print("%12s:  %s" % (etype,einfo[:self.contral]))
			self.print_notice('',einfo[self.contral:])
	@staticmethod
	def print_error(etype,einfo,ftype='error'):
		STATE_NOTICE.print_notice(etype,einfo,ftype)



class interface(Linker):	
	def __init__(self):
		Linker.__init__(self)
		STATE_NOTICE.print_notice('initial','start a interface instance OK...')

	def get_article_title(self):
		element_title = self.webbrowser.find_element_by_class_name("title").find_element_by_tag_name("h1")
		title = element_title.text
		STATE_NOTICE.print_notice('article','get_article_title')
		return title

	def get_article_description(self):
		element_description = self.webbrowser.find_element_by_class_name("detailTxt").find_elements_by_tag_name("p")
		i = 0
		description = element_description[i].text
		while (u'\u58f0\u660e' in description):
			i=i+1
			description = element_description[i].text
		STATE_NOTICE.print_notice('article','get_article_description')
		return description

	def get_article_image(self):
		element_title_image = self.webbrowser.find_element_by_class_name('detailTxt').find_element_by_tag_name('img')
		STATE_NOTICE.print_notice('article','get_article_image')
		return element_title_image.get_attribute("src")


	def GetDetail(self,pageid):
		Details=[]
		lists=self.webbrowser.find_element_by_class_name('detailTxt').find_elements_by_tag_name('p')
		for D in lists:
			try:
				Details.append({'Page_id':pageid,'type':'img','detail':D.find_element_by_tag_name('img').get_attribute("src")})
			except Exception,e:
				STATE_NOTICE.print_notice('GetDetailErr',str(e).replace('\n',''))
				if("img" in str(e)):
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
		return pages


	def get_picture(self,link):
		header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'}
		request = urllib2.Request(link, None, header)  
		response = urllib2.urlopen(request)
		name = link.split("/")
		name = name[len(name)-1]
		with open("jiongtu/%s" % name, "wb") as f:
			f.write(response.read())
		STATE_NOTICE.print_notice('get_picture',link+'->'+name)
		return name

class ftp_client(object):
	def __init__(self):
		HOST = 'ankland911.gotoip3.com'
		PORT = '21' 
		USER = 'ankland911'
		PASS = 'kuailong88'
		DIRN = '/wwwroot/Public/jiongtu'
		FILE = 'bugzilla-3.6.7.tar.gz'
		try:
			self.ftp = FTP()
			self.ftp.connect(HOST,PORT)
		except(socket.error,socket.gaierror):
			STATE_NOTICE.print_error('ERROR','ERROR:cannotreach"%s"' % HOST)
			return
		self.ftp.login(USER,PASS)
		self.ftp.cwd(DIRN)
		self.bufsize=1024
		STATE_NOTICE.print_notice('initial','start a ftp client instance OK...')
		
	def ftp_upload(self,file_handle,filename):
		try:
			self.ftp.storbinary("STOR %s" % filename,file_handle,self.bufsize)
		except Exception,e:
			print str(e)
			raw_input()
			self.__init__()

	def __del__(self):
		self.ftp.quit()

def check_detail(detailtxts,tid):
	if(len(detailtxts)==0):
		return 0
	count_img = 0
	count_txt = 0
	for detailtxt in detailtxts:
		if(detailtxt[tid]=='img'):
			count_img = count_img +1
		elif(detailtxt[tid]=='txt'):
			count_txt = count_txt +1
	if(count_txt==count_img):
		return 1
	else:
		return -1


def db_get_data_list():
	db = MyDb({"host":"ankland911.gotoip3.com","user":"ankland911","pass":"kuailong88","db":"ankland911"})
	article_links = db.Model("article_links").SQL("select copy_link,article_id,imagepath from article_links")
	articles = Queue()
	for article_link in article_links:
		article = {}
		article['copy_link'] = article_link[0]
		article['article_id'] = article_link[1]
		article['imagepath'] = article_link[2]
		if(article['imagepath']!=None):
				STATE_NOTICE.print_notice('articleLinks',("article_id %s is not Null" % article['article_id']))
				continue
		articles.put(article)

	return articles

if __name__ == '__main__':
	try:
		data = {}
		where = {}
		app = interface()
		ftp = ftp_client()
		db = MyDb({"host":"ankland911.gotoip3.com","user":"ankland911","pass":"kuailong88","db":"ankland911"})
		# step 1:
		articles = db_get_data_list()
		# article_links = db.Model("article_links").SQL("select copy_link,article_id,imagepath from article_links")
		# for article_link in article_links:
		# 	article_id = article_link[1]
		# 	error_notice.print_notice('start',("article id=%s" % article_id))
		# 	if(article_link[2]!=None):
		# 		error_notice.print_notice('articleLinks',("article id %s is not Null" % article_id))
		# 	else:
		while not (articles.empty()):
			article = articles.get()
			app.Get(article['copy_link'])
			data['detail']=app.get_article_description()
			data['title']=app.get_article_title()
			image_name = app.get_picture(app.get_article_image())
			file_handle = open("jiongtu/%s" % image_name,"r")
			ftp.ftp_upload(file_handle,image_name)
			data['imagepath'] = '/Public/jiongtu/%s' % image_name
			where['article_id'] = article_id
			data['date'] = mTime.mtime()
			rs = db.Model('article_links').where(where).update(data)

			# step 2:
		pages = db.Model('pages').SQL(("select link,page_id from pages where article_id=\'%s\' and UNIX_TIMESTAMP(\'%s\')-UNIX_TIMESTAMP(date)>864000" % (article_id,mTime.mtime())))
		if(pages==()):
			rs = app.GetPages(article_id)
			for r in rs:
				rs = db.Model('pages').insert(r)
				error_notice.print_notice('insertPages',r['page_id'])
			pages = db.Model('pages').SQL(("select link,page_id from pages where article_id=\'%s\'" % article_id))


		for page in pages:
			pageId = page[1]
			error_notice.print_notice('start',("page_id=%s" % pageId))
			app.Get(page[0])

			#step 3:
			detailtxts = db.Model('detailtxt').SQL(("select detail_id,type from detailtxt where page_id=\'%s\'" % pageId))	
			check_d = check_detail(detailtxts,1)
			
			if(check_d<1):
				if(check_d==-1):
					db.Model('detailtxt').SQL("delete from detailtxt where page_id=\'%s\'" % pageId)
				detailtxts=[]
				details = app.GetDetail(pageId)
				for detail in details:
					rs = db.Model('detailtxt').field('max(detail_id)').select()
					max_detail_id = int(rs[0][0])
					detail['detail_id'] = str(max_detail_id+10).zfill(8)
					if(detail['type']=='txt'):
						error_notice.print_notice('detail_r',str(detail))
						rs = db.Model('detailtxt').insert(detail)
					elif(detail['type']=='img'):
						downimage={}
						downimage['detail_id']=detail['detail_id']
						downimage['detail']=detail['detail']
						error_notice.print_notice('detail_r',str(downimage))
						rs = db.Model('downimage').insert(downimage)
						error_notice.print_notice('result',"do get downimage result="+str(bool(rs))+"; detail_id="+detail['detail_id']+"; type="+detail['type'])
						error_notice.print_notice('lastsql',db.Model('downimage').option['lastsql'])
						del detail['detail']
						error_notice.print_notice('detail_r',str(detail))
						rs = db.Model('detailtxt').insert(detail)
					error_notice.print_notice('result',"do get detail result="+str(bool(rs))+"; detail_id="+detail['detail_id']+"; type="+detail['type'])
					error_notice.print_notice('lastsql',db.Model('detailtxt').option['lastsql'])
					detailtxts.append([unicode(detail['detail_id']),unicode(detail['type'])])

			sort_id = 1
			for detailtxt in detailtxts:
				detailId = detailtxt[0]
				error_notice.print_notice('start',("detail_id=%s" % detailId))
				where={}
				where['detail_id'] = detailId
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
					error_notice.print_notice('change','downimage path:'+str(rs) + '  '+detailtxt[0]+'   '+data['path'])
			where={}
			where['page_id'] = pageId
			db.Model('pages').where(where).update({'date':mTime.mtime()})
		app.quit()
		del db
		del ftp
		raw_input()
	except KeyboardInterrupt:
	 	raw_input()
	 	del db
	 	del ftp




	

