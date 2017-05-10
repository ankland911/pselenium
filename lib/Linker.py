# -*- coding: UTF-8 -*- 
from selenium import webdriver
import sys,os,time

class Linker(object):

	def __init__(self):
		iedriver = "C:\Python27\Scripts\IEDriverServer.exe"
		os.environ["webdriver.ie.driver"] = iedriver
		self.webbrowser = webdriver.Ie(iedriver)
		# self.webbrowser = webdriver.Firefox()
		#self.webbrowser = webdriver.PhantomJS(executable_path="/Users/leizhang/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs")
		time.sleep(1)

	def quit(self):
		self.webbrowser.quit()
		# print "Linker is release...Everything is done."
			
	def Get(self,url):
		try:
			self.webbrowser.implicitly_wait(5)
			self.webbrowser.set_page_load_timeout(5)
			# self.webbrowser.set_script_load_timeout(5)
			self.webbrowser.get(url)
		except Exception as e:
			# self.webbrowser.execute_script('window.stop()')
			print 'Get:'+str(e)

	def find_element(self, by=None, value=None):
		return self.webbrowser.find_element(by,value)
