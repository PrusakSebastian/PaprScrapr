#DEFINE PARENT PATH TO IMPORT MODULES
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from SearchResultDownloader import SearchResultDownloader
from SearchResultConverter import SearchResultConverter
from PDFDownloader import PDFDownloader
from ArticleSet import ArticleSet

from PaperScraperAPI import PaperScraperAPI

#Online Work
#srd = SearchResultDownloader()
#srd.downloadMulti("signal processing", 1, 8)

#Offline Work
#src = SearchResultConverter()
#src.convertAll("signal processing")
#article = src.searchresults[7]

#Online Work
#pdfd = PDFDownloader()
#pdfd.download(article)


#srd = SearchResultDownloader()
#srd.downloadMulti("mechanical", 1, 2)
#srd.downloadMulti("neural network", 1, 3)
#srd.downloadMulti("deep learning", 1, 3)

#src = SearchResultConverter()
#src.convertAll("math")
#src.convertAll("neural network")
#src.convertAll("deep learning")

#aset = ArticleSet()
#aset.collectArticlesFromDIR()
#al = aset.getArticleList("neural network")
#al = aset.getAllArticleLists()

#articles = src.searchresults[0]
#pdfd = PDFDownloader()
#pdfd.downloadArticle(article)
#pdfd.downloadArticleList(al[0])

#Online Work
#srd = SearchResultDownloader()
#srd.download("neural", 1)
#srd.download("neural", 2)
#srd.download("neural", 3)

#Offline Work
#src = SearchResultConverter()
#src.load_file("neural", 1)
#src.convert()
#src.store()
#src.load_file("neural", 2)
#src.convert()
#src.store()
#src.load_file("neural", 3)
#src.convert()
#src.store()

ps_api = PaperScraperAPI()
ps_api.download("Quant",2)
