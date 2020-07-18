import urllib.request as urllib2
from urllib.request import Request, urlopen
import urllib

from yelp_uri.encoding import recode_uri

import shutil
import time
import os

from Article import Article
from SearchResultParser import SearchResultParser
import Project

class SearchResultDownloader:
	RAW_RESULTS_DIR = Project.resource_path("data/raw_results/")

	def __init__(self):
		self.time_between_requests = 3.0
		self.page_url = 'https://scholar.google.de/scholar?'
		self.full_url = ''

	def already_exists(self, topic, page):
		file_name = self.RAW_RESULTS_DIR+topic+'.'+str(page)+'.html'
		exists = os.path.isfile(file_name)
		return exists

	def searchData(self, topic, page = 0, proxy_host = None):
		print("..................................................................")
		print("Search: <<< ",topic,">>> , Page ",page)
		if self.already_exists(topic, page):
			print("Already searched for it! File existing.")
			return
		print("Wait ",self.time_between_requests," seconds before request")
		time.sleep(self.time_between_requests)

		page = (page-1)*10
		data = None
		self.full_url = ''                                                  #re-init
		self.full_url = self.page_url+'start='+str(page)+'&hl=de&q='+topic  # specify the url
		self.full_url = recode_uri(self.full_url)                           # avoid Unicode Error

		req = Request(self.full_url, headers={'User-Agent': 'Mozilla/5.0'})

		response = urlopen(req)
		print("Got response!")
		return response

	def storeData(self, topic, page, response):
		file_name = self.RAW_RESULTS_DIR+topic+'.'+str(page)+'.html'
		with open(file_name, 'wb') as f:        #BYTE writing mode
			shutil.copyfileobj(response, f)
		print("Stored response in ",file_name)

	def download(self, topic, page, proxy_host = None):
		try:
		   response = self.searchData(topic, page, proxy_host)
		   if response == None: return
		   self.storeData(topic, page, response)
		except Exception as e:
			print(e)
			raise Exception("Download Error. Stop")

	def downloadMulti(self, topic, startpage, amount, proxy_host = None):
		start = startpage
		end   = startpage+amount-1
		print("__________________________________________________________________")
		print("Download multiple pages (",start,"-",end,") for: <<< ",topic," >>>")
		try:
			for i in range(start, end+1):
			    #print("Page ",i,":")
			    self.download(topic, i, proxy_host)
		except Exception as e:
			print(e)
			raise Exception("Download Error. Stop")
