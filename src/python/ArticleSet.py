import os
import csv
from Article import Article


#DEFINE PARENT PATH
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) #   ./PaprScrapr/src/python
parentdir = os.path.dirname(currentdir)                                                #   ./PaprScrapr/src
rootdir = os.path.dirname(parentdir)  												   #   ./PaprScrapr
#sys.path.insert(0,parentdir)

class ArticleSet:
	CONV_RESULTS_DIR = rootdir+"/data/conv_results/"

	def __init__(self):
		self.list_of_article_lists = {}

	def addArticleList(self, article_list, topic):
		self.list_of_article_lists[topic] = article_list

	def getArticleList(self, topic):
		return self.list_of_article_lists.get(topic)

	def getAllArticleLists(self):
		return list(self.list_of_article_lists.values())

	def collectArticleFromROW(self, row):
		title     = row[0]
		authors   = row[1].replace("[","").replace("]","").replace("'","").split(",")
		year      = row[2]
		text      = row[3]
		hyperlink = row[4]
		pdflink   = row[5]
		cited     = row[6]
		typ       = row[7]
		searchkey = row[8]
		new_article = Article(title, authors, hyperlink, text, cited, year, typ, pdflink, searchkey)
		return new_article

	def collectArticlesFromCSV(self, topic):
		new_article_list = []
		os_file_path = self.CONV_RESULTS_DIR+topic+'.csv'
		with open(os_file_path,'r') as file:
			reader = csv.reader(file,delimiter=',')
			for row in reader:
				new_article = self.collectArticleFromROW(row)
				new_article_list.append(new_article)
		return new_article_list

	def collectArticlesFromDIR(self):
		for filename in os.listdir(self.CONV_RESULTS_DIR):
			if filename == "_tmp_.csv":
				continue
			if filename.endswith(".csv"):
				topic = filename.replace('.csv','')
				new_article_list = self.collectArticlesFromCSV(topic)
				self.addArticleList(new_article_list, topic)
