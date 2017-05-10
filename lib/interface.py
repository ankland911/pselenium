# -*- coding: UTF-8 -*- 
# from lib.IOdevice import IOdevice
from Linker import Linker
from MyDb import MyDb
import urllib2
from ftplib import FTP
import socket
import time
from Queue import Queue
import threading

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
			print("%16s:  %s" % (etype,einfo))
		else:
			print("%16s:  %s" % (etype,einfo[:contral]))
			STATE_NOTICE.print_notice('',einfo[contral:])
	@staticmethod
	def print_error(etype,einfo,ftype='error'):
		STATE_NOTICE.print_notice(etype,einfo,ftype)



class interface(Linker):
	def __init__(self,no):
		Linker.__init__(self)
		self.no =no
		STATE_NOTICE.print_notice('initial','start a interface instance OK...')

	def get_article_title(self):
		title = self.webbrowser.find_element_by_class_name("title").find_element_by_tag_name("h1").text
		STATE_NOTICE.print_notice('get_article_title',title) 
		return title

	def get_article_description(self):
		element_description = self.webbrowser.find_element_by_class_name("detailTxt").find_elements_by_tag_name("p")
		i = 0
		description = element_description[i].text
		while (u'\u58f0\u660e' in description):
			i=i+1
			description = element_description[i].text
		STATE_NOTICE.print_notice('get_article_description',description)
		return description

	def get_article_image(self):
		element_title_image = self.webbrowser.find_element_by_class_name('detailTxt').find_elements_by_tag_name('img')
		image = element_title_image[1].get_attribute("src")
		STATE_NOTICE.print_notice('get_article_image',image)
		return image


	def GetDetail(self,pageid):
		Details=[]
		lists=self.webbrowser.find_element_by_class_name('detailTxt').find_elements_by_tag_name('p')
		for D in lists:
			try:
				src = D.find_element_by_tag_name('img').get_attribute("src")
				Details.append({'Page_id':pageid,'type':'img','detail':src})
				STATE_NOTICE.print_notice(str(self.no)+'GetDetailImg',str(pageid)+';'+src)
			except Exception,e:
				if("img" in str(e)):
					if(D.text==''):
						continue
					Details.append({'type':'txt','Page_id':pageid,'detail':D.text})
					STATE_NOTICE.print_notice(str(self.no)+'GetDetailTxt',str(pageid)+';'+D.text)
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
		try:
			header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'}
			request = urllib2.Request(link, None, header)  
			response = urllib2.urlopen(request)
			name = link.split("/")
			name = name[len(name)-1]
			with open("jiongtu/%s" % name, "wb") as f:
				f.write(response.read())
			STATE_NOTICE.print_notice('get_picture',link+'->'+name)
			return name
		except Exception,e:
			STATE_NOTICE.print_error('system error',str(e))



# def check_detail(detailtxts,tid):
# 	if(len(detailtxts)==0):
# 		return 0
# 	count_img = 0
# 	count_txt = 0
# 	for detailtxt in detailtxts:
# 		if(detailtxt[tid]=='img'):
# 			count_img = count_img +1
# 		elif(detailtxt[tid]=='txt'):
# 			count_txt = count_txt +1
# 	if(count_txt==count_img):
# 		return 1
# 	else:
# 		return -1


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
				# STATE_NOTICE.print_notice('articleLinks',("article_id %s is not Null" % article['article_id']))
				continue
		articles.put(article)

	return articles


# def get_detail_main(page_tasks,no):
# 	app  = interface(no)
# 	# ftp  = ftp_client()
# 	db = MyDb({"host":"ankland911.gotoip3.com","user":"ankland911","pass":"kuailong88","db":"ankland911"})
# 	while not page_tasks.empty():
# 		try:
# 			if mutex.acquire():	
# 				task = page_tasks.get()
# 				mutex.release()
# 			app.Get(task['link'])
# 			page_id = task['page_id']
# 			detailtxts = db.Model('detailtxt').SQL(("select detail_id,type from detailtxt where page_id=\'%s\'" % page_id))	
# 			check_d = check_detail(detailtxts,1)
			
# 			if(check_d<1):
# 				if(check_d==-1):
# 					db.Model('detailtxt').SQL("delete from detailtxt where page_id=\'%s\'" % page_id)
# 				detail_txts=[]
# 				details = app.GetDetail(page_id)
# 				for detail in details:
# 					rs = db.Model('detailtxt').field('max(detail_id)').select()
# 					max_detail_id = int(rs[0][0])
# 					detail['detail_id'] = str(max_detail_id+10).zfill(8)
# 					if(detail['type']=='txt'):
# 						# STATE_NOTICE.print_notice('detail_r',str(detail))
# 						rs = db.Model('detailtxt').insert(detail)
# 					elif(detail['type']=='img'):
# 						downimage={}
# 						downimage['detail_id']=detail['detail_id']
# 						downimage['detail']=detail['detail']
# 						# STATE_NOTICE.print_notice('detail_r',str(downimage))
# 						rs = db.Model('downimage').insert(downimage)
# 						# STATE_NOTICE.print_notice('downimage',"do get downimage result="+str(bool(rs))+"; detail_id="+detail['detail_id']+"; type="+detail['type'])
# 						# STATE_NOTICE.print_notice('lastsql',db.Model('downimage').option['lastsql'])
# 						# del detail['detail']
# 						# STATE_NOTICE.print_notice('detail_r',str(downimage))
# 						rs = db.Model('detailtxt').insert(detail)
# 					STATE_NOTICE.print_notice(str(no)+'result',"do get detail result="+str(bool(rs))+"; detail_id="+detail['detail_id']+"; type="+detail['type'])
# 					# STATE_NOTICE.print_notice('lastsql',db.Model('detailtxt').option['lastsql'])
# 					# detail_txts.append([unicode(detail['detail_id']),unicode(detail['type'])])
# 					# sort_id = 1
# 					# for detailtxt in detail_txts:
# 					# 	detailId = detailtxt[0]
# 					# 	STATE_NOTICE.print_notice('start',("detail_id=%s" % detailId))
# 					# 	where={}
# 					# 	where['detail_id'] = detailId
# 					# 	if(detailtxt[1]=='img'):
# 					# 		#step 4:
# 					# 		# image = db.Model('downimage').where(where).field('detail').select()
# 					# 		# if(image==()):
# 					# 			# pass
# 					# 		# link_downimage = image[0][0]
# 					# 		# image_name_downimage = app.get_picture(link_downimage)
# 					# 		# file_handle = open("jiongtu/%s" % image_name_downimage,"r")
# 					# 		# ftp.ftp_upload(file_handle,image_name_downimage)
# 					# 		data={}
# 					# 		data['detail_id'] = detailId
# 					# 		data['detail'] = link_downimage
# 					# 		# data['path'] = '/Public/jiongtu/%s' % image_name_downimage
# 					# 		rs = db.Model('downimage').where(where).update(data)
# 					# 		STATE_NOTICE.print_notice('change','downimage path:'+str(detailId) + '  '+detailtxt[0]+'   '+data['detail'])
# 					where={}
# 					where['page_id'] = page_id
# 					db.Model('pages').where(where).update({'date':mTime.mtime()})
# 			else:
# 				STATE_NOTICE.print_notice("Nothing","Nothing to do")
# 		except:
# 			continue
# 	del db
# 	del app


class PageThread(threading.Thread):
	def __init__(self,page_tasks,no):
		self.app = interface(no)
		self.page_tasks = page_tasks
		threading.Thread.__init__(self)

	def check_detail(self,detailtxts,tid):
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

	def run(self):
		db = MyDb({"host":"ankland911.gotoip3.com","user":"ankland911","pass":"kuailong88","db":"ankland911"})
		global mutex
		while not page_tasks.empty():
			try:
				if mutex.acquire():	
					task = page_tasks.get()
					mutex.release()
				STATE_NOTICE.print_notice("Starting PageThread",str(task['link']))
				self.app.Get(task['link'])
				page_id = task['page_id']
				detailtxts = db.Model('detailtxt').SQL(("select detail_id,type from detailtxt where page_id=\'%s\'" % page_id))	
				check_d = self.check_detail(detailtxts,1)
				
				if(check_d<1):
					if(check_d==-1):
						db.Model('detailtxt').SQL("delete from detailtxt where page_id=\'%s\'" % page_id)
					detail_txts=[]
					details = self.app.GetDetail(page_id)
					for detail in details:
						rs = db.Model('detailtxt').field('max(detail_id)').select()
						max_detail_id = int(rs[0][0])
						detail['detail_id'] = str(max_detail_id+10).zfill(8)
						if(detail['type']=='txt'):
							rs = db.Model('detailtxt').insert(detail)
						elif(detail['type']=='img'):
							downimage={}
							downimage['detail_id']=detail['detail_id']
							downimage['detail']=detail['detail']
							rs = db.Model('downimage').insert(downimage)
							rs = db.Model('detailtxt').insert(detail)
						STATE_NOTICE.print_notice(str(no)+'result',"do get detail result="+str(bool(rs))+"; detail_id="+detail['detail_id']+"; type="+detail['type'])
						where={}
						where['page_id'] = page_id
						db.Model('pages').where(where).update({'date':mTime.mtime()})
				else:
					STATE_NOTICE.print_notice("Nothing","Nothing to do")
			except KeyboardInterrupt:
			 	exit()
			except Exception,e:
				print str(e)
				# continue
		del db
		del app
class MyThread(threading.Thread):
	def __init__(self,articles,no):
		self.app = interface(no)
		self.articles = articles
		threading.Thread.__init__(self)
	def run(self):
		# ftp  = ftp_client()
		db = MyDb({"host":"ankland911.gotoip3.com","user":"ankland911","pass":"kuailong88","db":"ankland911"})
		global mutex
		while not self.articles.empty():
			if mutex.acquire():
				data={}
				article = self.articles.get()
				mutex.release()
				self.app.Get(article['copy_link'])
				data['detail']=self.app.get_article_description()
				data['title']=self.app.get_article_title()
				image_name = self.app.get_picture(self.app.get_article_image())
				if image_name == None:
					continue
				file_handle = open("jiongtu/%s" % image_name,"r")
				ftp.ftp_upload(file_handle,image_name)
				data['imagepath'] = '/Public/jiongtu/%s' % image_name
				where['article_id'] = article['article_id']
				data['date'] = mTime.mtime()
				rs = db.Model('article_links').where(where).update(data)

				pages=db.Model('pages').SQL('select link,page_id from pages where article_id=\'%s\'' % article['article_id'])

				if(pages==()):
					prs = app.GetPages(article_id)
					for r in prs:
						rs = db.Model('pages').insert(r)
						STATE_NOTICE.print_notice('getPages',r['page_id'])
		self.app.quit()
		del self.app
		del db
		# del ftp




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
			self.__init__()
			self.ftp_upload(file_handle,filename)

	def __del__(self):
		try:
			self.ftp.quit()
		except:
			pass

if __name__ == '__main__':
	global mutex
	mutex = threading.Lock()
	try:
		data = {}
		where = {}
		db = MyDb({"host":"ankland911.gotoip3.com","user":"ankland911","pass":"kuailong88","db":"ankland911"})
		# step 1:
		articles = db_get_data_list()
		if not articles.empty():
			my_thread = []
			for i in range(2):
				my_thread.append(MyThread(articles,i))
			for t in my_thread:
				t.start()
			for t in my_thread:
				t.join()

		pages = db.Model('pages').SQL('select link,page_id from pages')
		page_tasks = Queue()
		for p in pages:
			page={}
			page['link'] = p[0]
			page['page_id'] = p[1]
			page_tasks.put(page)

			#step 3:
			threads=[]
		for t in range(2):
			threads.append(PageThread(page_tasks,t))
		for thread in threads:
			thread.start()
		for thread in threads:
			thread.join()

		# app.quit()
		del db
	except KeyboardInterrupt:
	 	del db
	except Exception,e:
		print str(e)








	

