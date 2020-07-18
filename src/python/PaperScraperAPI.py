from os import walk
import os.path
import os
import pandas as pd
import time

from SearchResultDownloader import SearchResultDownloader
from SearchResultConverter import SearchResultConverter
from PDFDownloader import PDFDownloader
from ArticleSet import ArticleSet
import Project

class PaperScraperAPI(object):
	def __init__(self):
		self.srd = SearchResultDownloader();
		self.src = SearchResultConverter();
		self.pdfd = PDFDownloader();
		self.d_progress = 0;
		self.CONV_RESULTS_DIR = Project.resource_path("data/conv_results")
		self.PDFS_DIR = Project.resource_path("data/pdfs/")

	def downloadPdfLink(self, href, pdf_name):
		print("__________________________________________________________________")
		print("Download PDF from Link:")
		status = self.pdfd.downloadFromLink(href, pdf_name);
		if status == 0:
			return "error";
		if status == 1:
			return "success";
		if status == 2:
			return "exists";
		if status == 3:
			return "nolink";
		if status == 4:
			return "format";
		return "none"


	def downloadArticleList(self, article_list):
		#------------------------------------------------------ 25%
		print("__________________________________________________________________")
		print("Download Article List:")
		for idx,article in enumerate(article_list):
			print("(",str(idx),"): ",article.name)
		#------------------------------------------------------
		self.d_progress = 30;
		time.sleep(0.1)
		#------------------------------------------------------ 30%
		print("..................................................................")
		al_len = len(article_list)
		for idx,article in enumerate(article_list):
			self.pdfd.downloadArticle(article, "("+str(idx)+"): ")
			#------------------------------------------------------
			self.d_progress = 30 + (idx/al_len)*70;
			time.sleep(0.1)
			#------------------------------------------------------ 30%-100%
		#------------------------------------------------------ 100%

	# def downloadMulti(self, topic, startpage, amount, proxy_host = None):
	# 	# start = startpage
	# 	# end   = startpage+amount-1
	# 	# print("__________________________________________________________________")
	# 	# print("Download multiple pages (",start,"-",end,") for: <<< ",topic," >>>")
	# 	# p_len = amount;
	# 	# for i in range(start, end+1):
	# 	# 	self.srd.download(topic, i, proxy_host)
	# 	# 	#------------------------------------------------------
	# 	# 	self.d_progress = 0 + (i/p_len)*90;
	# 	# 	time.sleep(0.1)
	# 	# 	#------------------------------------------------------ 0%-20%
	# 	# #------------------------------------------------------ 20%
	# 	self.srd.downloadMulti(topic, startpage, amount)

	def download(self, topic, amount):
		startpage = 1;
		amount = int(amount);
		#------------------------------------------------------
		self.d_progress = 0;
		time.sleep(0.1)
		#------------------------------------------------------ 0%
		self.downloadMulti(topic, startpage, amount);
		#------------------------------------------------------
		self.d_progress = 20;
		time.sleep(0.1)
		#------------------------------------------------------ 20%
		self.src.convertAll(topic)
		#------------------------------------------------------
		self.d_progress = 25;
		time.sleep(0.1)
		#------------------------------------------------------ 25%
		aset = ArticleSet()
		alist = aset.collectArticlesFromCSV(topic)
		chunk = alist[0:0 + amount*10]
		self.downloadArticleList(chunk)
		#------------------------------------------------------
		self.d_progress = 100;
		time.sleep(2)
		print("__________________________________________________________________")
		print()
		print("--- Finished Download ---")
		#------------------------------------------------------ 100%
		self.d_progress = 0;
		return

	def search(self, topic, amount=4):
		#startpage = 1
		amount = int(amount)
		startpage = 1
		self.srd.downloadMulti(topic, startpage, amount)
		self.src.convertAll(topic)
		#self.d_progress = 100;
		#self.download(topic, amount)
		print("__________________________________________________________________")
		print()
		print("--- Finished Search ---")
		return

	def getTopics(self):
		topics = []
		filedir_i = self.CONV_RESULTS_DIR
		for filename in os.listdir(filedir_i):
			if not filename.endswith(".csv"):
				continue
			if filename == "_tmp_.csv":
				continue
			topics.append(filename[:-4])
		return topics

	def getDownloads(self):
		downloads = []
		filedir_i = self.PDFS_DIR
		for filename in os.listdir(filedir_i):
			if not filename.endswith(".pdf"):
				continue
			downloads.append(filename)#[:-4])
		return downloads

	def get_csv_for_topic(self, topic):
		df = pd.DataFrame()
		if self.src.CSVexists(topic):
		   csv_filename = self.CONV_RESULTS_DIR+"/"+topic+".csv"
		   try:
			   df = pd.read_csv(csv_filename)
		   except Exception:
			   pass
		return df

	#def resolve_pdf_search(self, title, author):

	def status(self):
		return int(self.d_progress)
