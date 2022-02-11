import sys
from tkinter import Menu
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5 import uic
from datetime import datetime
import sqlite3
import os
import webbrowser

from pandas import Series

class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("saveTvSeriesGui.ui", self)

        self.startDB()
        self.populateList(self.populateDict())

        self.display()

        self.viewButton.clicked.connect(self.viewFunction)
        self.deleteButton.clicked.connect(self.deleteFunction)
        self.updateButton.clicked.connect(self.updateFuntcion)

        self.addButton.clicked.connect(self.addFunction)
        self.searchButton.clicked.connect(self.searchFunction)
        self.googleButton.clicked.connect(self.googleFunction)

    def display(self):
        #set to first item
        self.listWidget.setCurrentRow(0)

        #display in view
        self.viewFunction()

    def viewFunction(self):
        currentItem = menu[self.listWidget.currentRow()]
        currentSeries = tvList[currentItem]
        print(currentItem, currentSeries)

        self.rankTextEdit.setPlainText(currentSeries["RANK"])
        self.lastWatchedTextEdit.setPlainText(currentSeries["LAST"])
        self.titleTextEdit.setPlainText(currentItem)
        self.timeLabel.setText(currentSeries["DATE"])

    # get ratingLabel and lastestLabel info
    def getInfo(self):
        pass

    def deleteFunction(self):
        currentItem = menu[self.listWidget.currentRow()]

        ret = QMessageBox.question(self, 'MessageBox', 'Confirm delete ' + currentItem, QMessageBox.Yes , QMessageBox.Cancel)

        if ret == QMessageBox.Yes:
            cur.execute("delete from tvseriesapp where title = ?",(currentItem,))
            conn.commit()
            self.populateList(self.populateDict())

    def updateFuntcion(self):
        rank = self.rankTextEdit.toPlainText()
        lastWatch = self.lastWatchedTextEdit.toPlainText()
        title = self.titleTextEdit.toPlainText()

        if title != "" and title in menu:
            ret = QMessageBox.question(self, 'MessageBox', 'Update ' + title, QMessageBox.Yes , QMessageBox.Cancel)

            if ret == QMessageBox.Yes:
                cur.execute("update tvseriesapp set lastwatch=?,rank=?,lastupdate=? where title = ?",(lastWatch, rank, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), title))
                conn.commit()
                self.display()


    def addFunction(self):
        rank = self.rankTextEdit.toPlainText()
        lastWatch = self.lastWatchedTextEdit.toPlainText()
        title = self.titleTextEdit.toPlainText()

        if rank =="\n" or rank == "" or lastWatch == "\n" or lastWatch == "" or title == "\n" or title == "":
            QMessageBox.about(self, "Required", "Title, last watched and ranking required!")
        elif title in menu:
            QMessageBox.about(self, "Error", "Title exist!")
        else:
            cur.execute("INSERT INTO tvseriesapp(title,lastwatch,rank,lastupdate) VALUES(?,?,?,?)", (title, lastWatch, rank, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            conn.commit()
            self.populateList(self.populateDict())

    def searchFunction(self):
        textToFind = self.titleTextEdit.toPlainText()

        cur.execute("select * from tvseriesapp where title like ? order by rank, title", ("%"+textToFind+"%",))
        series = cur.fetchall()

        self.populateList(series)


    def googleFunction(self):
        pass

    def populateList(self, series):
        global tvList
        global menu

        menu = list()
        tvList = {}

        self.listWidget.clear()
        
        #populate dictionary and populate list
        for item in series:
            tvList[item[0]] = {"LAST":item[1], "RANK":item[2], "DATE":item[3]}
            menu.append(item[0])
            self.listWidget.addItem(item[0])
            self.display()
        
        


    def populateDict(self):
        #get items from dictionary
        cur.execute("select * from tvseriesapp order by rank, title")
        series = cur.fetchall()
        return series


    def startDB(self):
        global conn, cur

        dblocation = r"D:\python\saveTVSeries2.0\tvseriesapp.db"

        conn = sqlite3.connect(dblocation)
        cur = conn.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS tvseriesapp(title,lastwatch,rank,lastupdate)")

if __name__ == '__main__':
    app = QApplication(sys.argv)

    demo = AppDemo()
    demo.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print("Closing Window...")
