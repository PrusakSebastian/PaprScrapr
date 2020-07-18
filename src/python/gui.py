from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QPushButton, QTableWidget, QTableWidgetItem, QListWidget, QListWidgetItem, QLineEdit, QCheckBox, QProgressBar, QLabel, QMessageBox
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtCore import Qt, QFile

#import threading
import time
import webbrowser
import pandas as pd

from PaperScraperAPI import PaperScraperAPI
import Project

#Form, Window = uic.loadUiType("/Users/sebastianprusak/Desktop/PaprScrapr/src/python/dialog.ui")

class Gui:
    def __init__(self):
        self.app = QApplication([])

        # Load the UI
        filepath = Project.resource_path("data/ui/dialog.ui")
        fileh = QFile(filepath)
        fileh.open(QFile.ReadOnly)
        Form, Window = uic.loadUiType(fileh)
        fileh.close()

        self.window = Window()
        self.form = Form()
        self.form.setupUi(self.window)

        self.df   = None
        self.papi = PaperScraperAPI()
        self.active_topic     = None
        self.articles         = self.window.findChild(QTableWidget, 'articles'); # Find the button
        self.search_field     = self.window.findChild(QLineEdit, 'search_field');
        self.topics_list      = self.window.findChild(QListWidget, 'topics_list');
        self.download_all_btn = self.window.findChild(QPushButton, 'download_all');
        self.download_all_btn.setAutoDefault(False) # Don't Trigger Button with Enter Key
        self.only_pdfs        = self.window.findChild(QCheckBox, 'only_pdfs');
        self.progress         = self.window.findChild(QProgressBar, 'search_progress');
        self.progress.hide();
        self.empty_label      = self.window.findChild(QLabel, 'empty_label');
        self.only_pdfs.hide()
        self.only_pdfs_isactive = False

        self.search_field.returnPressed.connect(self.search)
        self.download_all_btn.clicked.connect(self.show_dialog)
        self.only_pdfs.stateChanged.connect(self.only_pdfs_changed)

        self.initTopics()
        self.initArticles()
        self.initStyle()

        self.window.setWindowTitle("Papr Scrapr")
        self.window.show()
        self.app.exec_()

    def cell_click(self, row, column):
        print("cell clicked: "+str(row)+" "+str(column))
        # PDF Download
        if(column == 5):
            if(self.articles.item(row, 4).text()=="PDF"):
                title        = self.articles.item(row, 0).text()
                author       = self.articles.item(row, 1).text().split(",")[0]
                year         = self.articles.item(row, 2).text()
                href         = self.articles.item(row, 3).text()
                pdf_name     = ''+title+' ° '+author+' ° '+year
                pdflink      = self.articles.item(row, 6).text()
                webbrowser.open(pdflink)
            # PDF Search
            else:
                title        = self.articles.item(row, 0).text()
                title        = title.replace(" ","+")
                author       = self.articles.item(row, 1).text().split(",")[0]
                author       = author.replace(" ","+")
                webbrowser.open("https://www.google.com/search?q="+title+"+"+author+"+pdf")
        # Open Link
        if(column == 3):
            href         = self.articles.item(row, 3).text()
            webbrowser.open(href)
            time.sleep(0.2)
        # Search for Title
        if(column == 0):
            title             = self.articles.item(row, 0).text()
            self.search_field.setText(title)

    def initArticles(self, topic = None):
        self.active_topic = topic

        # clear table
        self.articles.setRowCount(0);

        if(topic==None):
            self.df = pd.DataFrame()
        else:
            self.df = self.papi.get_csv_for_topic(topic)
        self.articles.show()
        self.download_all_btn.show()
        self.only_pdfs.show()
        self.empty_label.hide()

        (rows, cols) = self.df.shape
        # set row count
        self.articles.setRowCount(rows)
        # set column count
        self.articles.setColumnCount(7)
        self.articles.setColumnHidden(6, True);
        self.articles.setHorizontalHeaderItem(0,QTableWidgetItem("Title"))
        self.articles.setHorizontalHeaderItem(1,QTableWidgetItem("Authors"))
        self.articles.setHorizontalHeaderItem(2,QTableWidgetItem("Date"))
        self.articles.setHorizontalHeaderItem(3,QTableWidgetItem("Source"))
        self.articles.setHorizontalHeaderItem(4,QTableWidgetItem("Type"))
        self.articles.setHorizontalHeaderItem(5,QTableWidgetItem("Download"))
        self.articles.setHorizontalHeaderItem(6,QTableWidgetItem("PDF Link"))

        self.articles.setColumnWidth(0, 400);
        self.articles.setColumnWidth(1, 300);
        self.articles.setColumnWidth(2, 50);
        self.articles.setColumnWidth(3, 270);
        self.articles.setColumnWidth(4, 70);

        if(self.df.empty):
            self.download_all_btn.hide()
            self.only_pdfs.hide()
            self.empty_label.show()
            return

        r = 0
        for i in range(0,rows):
            title      = str(self.df[self.df.columns[0]].iloc[i])
            authors    = str(self.df[self.df.columns[1]].iloc[i]).replace("[","").replace("]","").replace("'","")
            year       = str(self.df[self.df.columns[2]].iloc[i])
            source     = str(self.df[self.df.columns[4]].iloc[i])
            type       = str(self.df[self.df.columns[7]].iloc[i])
            pdflink    = str(self.df[self.df.columns[5]].iloc[i])
            if(self.only_pdfs_isactive):
                if(type != "PDF"): continue

            author = authors.split(",")[0]
            pdf_name = ''+title+' ° '+author+' ° '+year
            item = QTableWidgetItem(title)
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            item.setForeground(QBrush(QColor(255, 255, 255)))
            self.articles.setItem(r,0, item)

            item = QTableWidgetItem(authors)
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            self.articles.setItem(r,1, item)

            item = QTableWidgetItem(year)
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            self.articles.setItem(r,2, item)

            item = QTableWidgetItem(source)
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            item.setForeground(QBrush(QColor(70, 100, 255)))
            self.articles.setItem(r,3, item)

            item = QTableWidgetItem(type)
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            self.articles.setItem(r,4, item)

            self.articles.setItem(r,6, QTableWidgetItem(pdflink))
            if(type == "PDF"):
                # create an cell widget
                btn = QPushButton()
                btn.setText('Download')
                self.articles.setCellWidget(r, 5, btn)
            else:
                btn = QPushButton()
                btn.setText('Search PDF')
                self.articles.setCellWidget(r, 5, btn)
            r = r+1
        self.articles.setRowCount(r)
        self.articles.cellClicked.connect(self.cell_click)

    # def update_progress(self):
    #     self.progress.show()
    #     while(self.papi.status() < 100):
    #         time.sleep(0.5)
    #         self.progress.setValue(self.papi.status())
    #         time.sleep(0.2)
    #     time.sleep(1.0)
    #     self.progress.hide()

    def search(self):
        topic = str(self.search_field.text())
        if(topic == ""): return
        try:
            self.papi.search(topic)
            self.initTopics()
        except Exception as e:
        	self.show_error_dialog()

    def topic_click(self, item):
        topic = str(item.text())
        self.initArticles(topic)

    def initTopics(self, new_topic = None):
        topics = self.papi.getTopics()
        self.topics_list.clear()
        for topic in topics:
            item = QListWidgetItem(topic)
            self.topics_list.addItem(item)
        self.topics_list.itemClicked.connect(self.topic_click)

    def only_pdfs_changed(self):
        self.only_pdfs_isactive = self.only_pdfs.isChecked()
        self.initArticles(self.active_topic)

    def download_all(self):
        for row in range (self.articles.rowCount()):
            print(row)
            if(self.articles.item(row, 4).text()=="PDF"):
                self.cell_click(row,5)
                time.sleep(0.5)

    def show_error_dialog(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Error")
        msg.setInformativeText("Too many Downloads. Try Later")
        msg.setWindowTitle("Error. Too many Downloads")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.buttonClicked.connect(self.msgbtn)
        retval = msg.exec_()

    def show_dialog(self):
        print("Test")
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Download All")
        msg.setInformativeText("This will open many Tabs in your Browser and take some time to download all pdfs. Continue?")
        msg.setWindowTitle("Download All Warning")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.buttonClicked.connect(self.msgbtn)
        retval = msg.exec_()

    def msgbtn(self,i):
        if (i.text() == "OK"):
            self.download_all()

    def initStyle(self):
        self.articles.setStyleSheet(
        """QTableWidget {
        background-color: rgb(50, 50, 50);
        border:1px solid rgb(100, 100, 100);
        color:rgb(200,200,200);
        gridline-color: rgb(255,255,230);
        font-size: 12pt;
        border-style: none;
        border-bottom: 1px solid rgb(100, 100, 100);
        border-right: 1px solid rgb(100, 100, 100); }

        QHeaderView {
        background-color: #777777;
        font-size: 10pt;
        border-style: none;
        border-bottom: 1px solid rgb(100, 100, 100);
        border-right: 1px solid rgb(100, 100, 100);
        }

        QPushButton {
        background-color: rgb(150,150,160);
        border-style: outset;
        border-width: 1px;
        border-radius: 4px;
        border-color: beige;
        font: bold 7px;
        min-width: 10em;
        padding: 2px;
        }

        QPushButton:hover {
        background-color: rgb(110,110,130);
        }
        """)

        self.download_all_btn.setStyleSheet("""
        QPushButton {
        background-color: rgb(130,130,140);
        border-style: outset;
        border-width: 1px;
        border-radius: 2px;
        border-color: beige;
        font: bold 7px;
        min-width: 10em;
        padding: 2px;
        }

        QPushButton:hover {
        background-color: rgb(110,110,130);
        }
        """)

        self.topics_list.setStyleSheet("""
        QListWidget {
        background-color: rgb(50, 50, 50);
        border:1px solid rgb(100, 100, 100);
        color:rgb(200,200,200) }
        """)

        self.search_field.setStyleSheet("""
        QLineEdit {
        background-color: rgb(50, 50, 50);
        border:1px solid rgb(100, 100, 100);
        color:rgb(200,200,200) }
        """)

        self.window.setStyleSheet("""
        background-color: rgb(45,45,50);
        color:rgb(250,250,250);
        """);

if __name__ == "__main__":
	app = Gui()
