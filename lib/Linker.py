# -*- coding: UTF-8 -*- 
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from GetPicture import GetPicture

class Linker(object):

	def __init__(self):
		# self.webbrowser = webdriver.Firefox()
		executable_path="/home/ec2-user/phantomjs-2.1.1-linux-i686/bin/phantomjs"
		self.webbrowser = webdriver.PhantomJS(executable_path)
		

	def quit(self):
		self.webbrowser.quit()

	def __del__(self):
		self.quit()
			
	def Get(self,url):
		#self.webbrowser.set_page_load_timeout(15)
		self.webbrowser.maximize_window()
		self.webbrowser.get(url)

class interface(Linker):
	def __init__(self):
		super(interface,self).__init__()

	def get_article_title(self):
		title = self.webbrowser.find_element_by_class_name("title").find_element_by_tag_name("h1").text
		return title

	def get_article_description(self):
		element_description = self.webbrowser.find_element_by_class_name("detailTxt").find_elements_by_tag_name("p")
		i = 0
		description = element_description[i].text
		while (u'\u58f0\u660e' in description):
			i=i+1
			description = element_description[i].text
		return description

	def get_article_image(self):
		element_title_image = self.webbrowser.find_element_by_class_name('detailTxt').find_elements_by_tag_name('img')
		image = element_title_image[1].get_attribute("src")
		return image

	def get_pages(self,article_id):
		pages = []
		data={}
		lists = self.webbrowser.find_element_by_id("pages").find_elements_by_tag_name("a")
		for p in lists:
			data['link'] = p.get_attribute("href")
			pages.append(data)
		return pages

	def get_detail(self,page_id):
		Details=[]
		lists=self.webbrowser.find_element_by_class_name('detailTxt').find_elements_by_tag_name('p')
		for D in lists:
			try:
				src = D.find_element_by_tag_name('img').get_attribute("src")
				Details.append({'Page_id':page_id,'type':'img','detail':src})
			except NoSuchElementException as msg:
				if(D.text==''):
					continue
				Details.append({'type':'txt','Page_id':page_id,'detail':D.text})
		return Details

	def execute(self,data):
		self.Get(data['link'])
		for detail in self.get_detail(data['page_id']):
			print ("title : ",detail['detail'])

		

# if __name__ == '__main__':
# 	interface = interface()
# 	link = Model('pages').field('link,page_id').where("id=2").select()
# 	interface.Get(link[0][0])
# 	for detail in interface.get_detail(link[0][1]):
# 		print ("title : ",detail['detail'])

