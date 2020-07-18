import urllib.request as urllib2
from urllib.request import Request, urlopen
from Article import Article
import Project

import time
import os

class PDFDownloader:
	PDFS_DIR = Project.resource_path("data/pdfs/")

	def __init__(self):
		self.time_between_requests = 3.0
		self.article = None

	def already_exists(self, article_name):
		file_name = self.PDFS_DIR+article_name+'.pdf'
		exists = os.path.isfile(file_name)
		return exists

	def addMetadata(self, file_path):
		#Add Source
		attr = 'com.apple.metadata:kMDItemWhereFroms'
		data = self.article.pdflink
		os.system('xattr -w '+attr+' \''+data+'\' \''+file_path+'\'')

		#Add Tag
		attr = 'com.apple.metadata:_kMDItemUserTags'
		tags = '<string>'+self.article.searchkey+'</string>'#+'<string>'+tag2+'</string>'
		data = '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd"><plist version="1.0"><array>'+tags+'</array></plist>'
		os.system('xattr -w '+attr+' \''+data+'\' \''+file_path+'\'')

		print("Metadata was added to PDF!")

		#xattr -w com.apple.metadata:kMDItemFinderComment "Comment here" file_path

	def downloadArticle(self, article, print_suffix=""):
		self.article = article
		article_name = self.article.name

		#print("_________________________________")
		print()
		print(print_suffix,"Download PDF for article: ")
		print("\t<<< ",article_name," >>>")

		#Check if already downloaded
		if self.already_exists(article_name):
			print("File already existing.")
			#os_file_path = '/Users/sebastianprusak/Desktop/GoogleScholar/pdfs/'+article.name+'.pdf'
			#self.addMetadata(os_file_path)
			return 2

		#Check if PDFlink exists
		download_url = self.article.pdflink
		if not download_url:
			print("Article has no PDF download link!")
			return 3

		#Check if PDFlink has correct format (.pdf)
		if not download_url.endswith(".pdf"):
			print("PDF download link is in wrong format! (no .pdf)")
			return 4

		#(Wait a little)
		print("Wait ",self.time_between_requests," seconds before request")
		time.sleep(self.time_between_requests)

		#Download
		file_name = self.PDFS_DIR+article_name+'.pdf'
		try:
			req = Request(download_url, headers={'User-Agent': 'Mozilla/5.0'})
			#response = urlopen(req)
			response = urllib2.urlopen(req).read()
			#response = urllib2.urlopen(download_url).read()
			with open(file_name, 'wb') as f:
				f.write(response)
			print("Download of PDF completed!")

			#Add Metadata
			os_file_path = self.PDFS_DIR+article_name+'.pdf'
			#os_file_path = '/Users/sebastianprusak/Desktop/GoogleScholar/pdfs/'+article_name+'.pdf'
			self.addMetadata(os_file_path)
			return 1
		except urllib2.HTTPError as err:
			if err.code == 404:
				print("HTTP Error 404: Not Found --> Continue with next PDF")
				return 0
			else:
				#raise
				print("Other Error")
				return 0
		except urllib2.URLError as err:
			print("URL Error --> Continue with next PDF")
			return 0
		except:
			return 0
		return 0

	def downloadArticleList(self, article_list):
		print("__________________________________________________________________")
		print("Download Article List:")
		for idx,article in enumerate(article_list):
			print("(",str(idx),"): ",article.name)
		print("..................................................................")
		for idx,article in enumerate(article_list):
			self.downloadArticle(article, "("+str(idx)+"): ")
			#print()

	def downloadFromLink(self, href, pdf_name, print_suffix=""):
		title     = "";
		authors   = [""];
		hyperlink = "";
		text      = "";
		cited     = "";
		year	  = "";
		typ       = "";
		pdflink   = "";
		searchkey = "";
		pdflink   = href;
		tmp_article = Article(title, authors, hyperlink, text, cited, year, typ, pdflink, searchkey)
		tmp_article.name = pdf_name;
		status = self.downloadArticle(tmp_article);
		return status
