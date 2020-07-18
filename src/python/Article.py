# coding=utf8

class Article:
    def __init__(self, title, authors, hyperlink, text, cited, year, typ, pdflink, searchkey):
        self.title     = title
        self.authors   = authors
        self.hyperlink = hyperlink
        self.text      = text
        self.cited     = cited
        self.year      = year
        self.typ       = typ
        self.pdflink   = pdflink
        self.searchkey = searchkey

        self.name = None
        self.makeName()

    def makeName(self):
        #self.name = unicode(''+self.title+' ° '+self.authors[0]+' ° '+self.year, "utf-8")
        self.name = ''+self.title+' ° '+self.authors[0]+' ° '+self.year
        self.name.encode('utf8', 'ignore')

    def addTitle(self, title):
        self.title = title

    def addAuthors(self, authors):
        self.authors = authors

    def addHyperlink(self, hyperlink):
        self.hyperlink = hyperlink

    def addText(self, text):
        self.text = text

    def addCited(self, cited):
        self.cited = cited

    def addYear(self, year):
        self.year = year

    def addTyp(self, typ):
        self.typ = typ

    def addDownload(self, download):
        self.download = download

    def show(self):
        print("_________________________________")
        if self.title:     print(self.title)
        if self.hyperlink: print(self.hyperlink)
        if self.pdflink:   print(self.pdflink)
        if self.text:      print(self.text)
        if self.authors:   print(self.authors)
