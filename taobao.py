# -*- coding: UTF-8 -*- 
from lib.IOdevice import IOdevice
import copy
from selenium.common.exceptions import NoSuchElementException
import urllib2,os

class taobao(IOdevice):

	def __init__(self):
		IOdevice.__init__(self)

	def get_title(self):
		title_element = self.find_element_by_class("tb-main-title")
		title = title_element.text
		return title

	def get_price(self):
		price_element = self.find_element_by_id("J_promoPriceNum")
		price = price_element.text
		return price

	def get_comment(self):
		comment_element = self.find_element_by_id("J_RateCounter")
		comment = comment_element.text
		return comment

	def get_volume(self):
		volume_element = self.find_element_by_id("J_SellCounter")
		volume = volume_element.text
		return volume

	def get_point(self):
		rate_element = self.find_elements_by_class("tb-rate-higher")
		describes = rate_element[0].find_element_by_tag_name("a").text
		service = rate_element[1].find_element_by_tag_name("a").text
		logistics = rate_element[2].find_element_by_tag_name("a").text
		point = {}
		point['describes'] = describes
		point['service'] = service
		point['logistics'] = logistics
		return point

	def get_stock(self):
		stock_element = self.find_element_by_id("J_SpanStock")
		stock = stock_element.text
		return stock

	def get_images(self):
		images = []
		images_element = self.find_element_by_id("J_UlThumb").find_elements_by_tag_name("li")
		for image in images_element:
			images.append(image.find_element_by_tag_name("a").find_element_by_tag_name("img").get_attribute("src").replace("60x60","400x400"))
		for img in images:
			print img
		return images

	def get_description(self):
		descriptions = []
		description_element = self.find_element_by_id("description").find_elements_by_tag_name("img")
		for desc in description_element:
			descriptions.append(desc.get_attribute("src"))
		return descriptions

	def get_Information(self,url):
		Information = {}
		Information["title"] = self.get_title()
		Information["price"] = self.get_price()
		Information["comment"] = self.get_comment()
		Information["volume"] = self.get_volume()
		Information["stock"] = self.get_stock()
		Information["images"] = self.get_images()
		self.update_dict({'link':'url'},Information,tbkitem)


app = taobao()
test = app.read_dict({},'tbkitem')
print test

	



	
