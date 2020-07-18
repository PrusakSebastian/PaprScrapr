import unicodedata
import re

class SearchResultParser:

    #Title
    #Hyperlink
    #PDFLink
    #Text
    #Authors
    #Cited
    #Year
    #Format

    def __init__(self):
        self.raw = None

    def init_raw(self, raw):
        self.raw = raw

    def parse_title(self):
        title = self.raw.find('h3', attrs={'class':'gs_rt'}).find('a')
        if title: title = title.get_text()
        else: title = self.raw.find('h3', attrs={'class':'gs_rt'}).get_text().split(']')[-1]
        return title

    def parse_hyperlink(self):
        hyperlink = self.raw.find('h3', attrs={'class':'gs_rt'}).find('a')
        if hyperlink: hyperlink = hyperlink.get('href')
        return hyperlink

    def parse_pdflink(self):
        pdflink = self.raw.find('div', attrs={'class':'gs_or_ggsm'})
        if pdflink: pdflink = pdflink.find('a').get('href')
        return pdflink

    def parse_text(self):
        text = self.raw.find('div', attrs={'class':'gs_rs'})
        if text: text = text.get_text()
        return text

    def parse_authors(self):
        raw_authors = self.raw.find('div', attrs={'class':'gs_a'})
        authors = []
        a_tmp = raw_authors.get_text().split('-')[0]
        authors = a_tmp.split(',')
        authors = [unicodedata.normalize("NFKD",a) for a in authors]
        return authors

    def parse_cited(self):
        cited = self.raw.find('div', attrs={'class':'gs_fl'})
        if cited: cited = cited.find('a', attrs={'class':'gs_or_cit gs_nph'})
        if cited: cited = cited.find_next_sibling('a')
        if cited: cited = cited.get_text().split()[-1]
        return cited

    def parse_typ(self):
        #typ = self.raw.find('h3', attrs={'class':'gs_rt'}).find('span', attrs={'class':'gs_ct1'})
        typ = self.raw.find('div', attrs={'class':'gs_or_ggsm'})
        if not typ: return "PAPER"
        typ = typ.find('span')
        if typ: typ = typ.get_text().replace("[", "").replace("]", "")
        else: typ = "PAPER"
        return typ

    def parse_year(self):
        year = self.raw.find('div', attrs={'class':'gs_a'}).get_text()
        year = re.search(r"(\d{4})", year).group(1)
        return year
