import sys
from tkinter import Menu
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import uic
from datetime import datetime
import sqlite3
import os
import webbrowser

class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("saveTvSeriesGui.ui", self)

        self.startDB()
        self.populateList()

        self.viewButton.clicked.connect(self.viewFunction)
        self.deleteButton.clicked.connect(self.deleteFunction)
        self.updateButton.clicked.connect(self.updateFuntcion)

        self.addButton.clicked.connect(self.addFunction)
        self.searchButton.clicked.connect(self.searchFunction)
        self.googleButton.clicked.connect(self.googleFunction)

    def viewFunction(self):
        currentItem = menu[self.listWidget.currentRow()]
        currentSeries = tvList[currentItem]
        print(currentItem, currentSeries)
        self.rankTextEdit.setPlainText(currentSeries["RANK"])
        self.lastWatchedTextEdit.setPlainText(currentSeries["LAST"])
        self.titleTextEdit.setPlainText(currentItem)
        self.timeLabel.setText(currentSeries["DATE"])

    def deleteFunction(self):
        pass

    def updateFuntcion(self):
        pass

    def addFunction(self):
        print(self.rankTextEdit.toPlainText())
        print(self.lastWatchedTextEdit.toPlainText())
        print(self.titleTextEdit.toPlainText())

    def searchFunction(self):
        pass

    def googleFunction(self):
        pass

    def populateList(self):
        global tvList
        global menu

        menu = list()
        tvList = {}

        series = self.populateDict()
        
        #populate dictionary and populate list
        for item in series:
            tvList[item[0]] = {"LAST":item[1], "RANK":item[2], "DATE":item[3]}
            menu.append(item[0])
            self.listWidget.addItem(item[0])

        #set to first item
        self.listWidget.setCurrentRow(0)
        
        #display in view
        self.viewFunction()


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
