import os
import csv
from bs4 import BeautifulSoup

from Article import Article
from SearchResultParser import SearchResultParser
import Project

class SearchResultConverter:
	def __init__(self):
		self.topic         = None
		self.page          = None
		self.response      = None
		self.searchresults = []   #contains list of articles
		self.sr_parser     = SearchResultParser()
		self.RAW_RESULTS_DIR = Project.resource_path("data/raw_results/")
		self.CONV_RESULTS_DIR = Project.resource_path("data/conv_results/")

	####################################################################
	# LOAD server response (which has been offline-saved)
	####################################################################
	def RAWexists(self, topic, page):
		file_name = self.RAW_RESULTS_DIR+topic+'.'+str(page)+'.html'
		exists = os.path.isfile(file_name)
		return exists

	def load_file(self, topic, page):
		print("..................................................................")
		print("Load from file: ",topic," , Page ",page)
		file_name = self.RAW_RESULTS_DIR+topic+'.'+str(page)+'.html'
		if not os.path.isfile(file_name):
			print("File doesn't exist!")
			return
		self.topic = topic
		self.page  = page
		response = None
		with open(file_name, 'r') as f:
			response = f.read()
		self.response = response
		print("Loaded response from ",file_name)
		print()
		return response

	####################################################################
	# PARSE server response INTO local searchresult format
	####################################################################
	def extract_list(self, response):
		soup = BeautifulSoup(response, 'html.parser')
		raw_list  = soup.find_all('div', attrs={'class': 'gs_r gs_or gs_scl'})
		return raw_list

	def parse_searchresult(self, raw_searchresult):
		self.sr_parser.init_raw(raw_searchresult)
		title     = self.sr_parser.parse_title()
		authors   = self.sr_parser.parse_authors()
		hyperlink = self.sr_parser.parse_hyperlink()
		text      = self.sr_parser.parse_text()
		cited     = self.sr_parser.parse_cited()
		year      = self.sr_parser.parse_year()
		typ       = self.sr_parser.parse_typ()
		pdflink   = self.sr_parser.parse_pdflink()
		searchkey = self.topic
		article = Article(title, authors, hyperlink, text, cited, year, typ, pdflink, searchkey)
		return article

	def parse_list_of_searchresults(self):
		#Extract HTML-searchresults from HTML-response
		raw_list = self.extract_list(self.response)
		parsed_list = []
		#Parse each HTML-searchresult and store in new LOCAL format
		for raw_searchresult in raw_list:
			article = self.parse_searchresult(raw_searchresult)
			parsed_list.append(article)
		self.searchresults = parsed_list
		return self.searchresults


	####################################################################
	# CSV Export of searchresults
	####################################################################
	def CSVexists(self, topic):
		file_name = self.CONV_RESULTS_DIR+topic+'.csv'
		exists = os.path.isfile(file_name)
		return exists

	def resetCSV(self, topic):
		file_name = self.CONV_RESULTS_DIR+topic+'.csv'
		with open(file_name, 'w+') as f:
			f.close()

	def extendCSV(self, topic):
		#TMP CSV
		file_name_tmp = self.CONV_RESULTS_DIR+'_tmp_.csv'
		self.resetCSV('_tmp_')
		self.writeCSV(topic, True)

		#OLD CSV
		file_name  = self.CONV_RESULTS_DIR+topic+'.csv'
		with open(file_name,'r') as file1:
			existingLines = [line for line in csv.reader(file1, delimiter=',')]

		#DIFF: Compare TMP CSV with OLD CSV to find new rows
		new = []
		with open(file_name_tmp,'r') as file2:
			reader2 = csv.reader(file2,delimiter=',')
			for row in reader2:
				if row not in new and row not in existingLines:
					new.append(row)

		#EXTEND: Add new rows to OLD CSV    (via append mode = 'a')
		with open(file_name, 'a') as f:
			csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			for row in new:
				csv_writer.writerow(row)

		self.resetCSV('_tmp_')

	def writeCSV(self, topic, is_tmp = False):
		file_name = self.CONV_RESULTS_DIR+topic+'.csv'
		if is_tmp:
			file_name = self.CONV_RESULTS_DIR+'_tmp_.csv'
		with open(file_name, 'w') as f:
			csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			for sr in self.searchresults:
				csv_writer.writerow([sr.title, sr.authors, sr.year, sr.text, sr.hyperlink, sr.pdflink, sr.cited, sr.typ, topic])

	def store(self):
		file_name = self.CONV_RESULTS_DIR+self.topic+'.csv'
		if self.CSVexists(self.topic):
			self.extendCSV(self.topic)
			print("Stored searchresults in ",file_name," (Extended)")
		else:
			self.writeCSV(self.topic)
			print("Stored searchresults in ",file_name," (New File)")
		#'.'+str(self.page)+

	####################################################################
	# AUTO CONVERT
	####################################################################
	def convert(self, topic, page):
		self.load_file(topic, page)
		self.parse_list_of_searchresults()
		self.store()

	def convertAll(self, topic):
		print("__________________________________________________________________")
		print("Convert Searchresults for <<< ",topic," >>> to CSV:")
		page = 1
		while self.RAWexists(topic, page):
			self.convert(topic, page)
			page = page+1
