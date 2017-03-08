# -*- coding: UTF-8 -*- 
from selenium import webdriver
import sys,os,time,threading
# from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException

class Linker(object):

	def __init__(self):
		iedriver = "C:\Python27\Scripts\IEDriverServer.exe"
		os.environ["webdriver.ie.driver"] = iedriver
		self.webbrowser = webdriver.Ie(iedriver)

	def quit(self):
		self.webbrowser.quit()
		print "Linker is release...Everything is done."
			
	def Get(self,url):
		try:
			self.webbrowser.get(url)
			self.webbrowser.implicitly_wait(5)
		except TimeoutException as e:
			print str(e)
		except Exception as e:
			print str(e)

	def find_element(self, by=None, value=None):
		return self.webbrowser.find_element(by,value)
