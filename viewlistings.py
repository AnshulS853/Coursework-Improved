from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QTableWidgetItem

import sqlite3

class viewListings(QDialog):
    def __init__(self, app, uid, admin):
        super(viewListings, self).__init__()
        loadUi("viewlists.ui", self)
        self.app = app
        self.userID = uid
        self.admin = admin

        self.currentListingID = None
        self.highlightedname = None
        self.query = None
        self.pcategory = None
        self.pcondition = None
        self.pdelivery = None
        self.pformat = None

        self.conn = sqlite3.connect("auc_database.db", isolation_level=None)
        self.cur = self.conn.cursor()

        self.updatepreferences()
        self.updatepref.clicked.connect(self.updatepreferences)
        self.goback.clicked.connect(self.gobackwindow)
        self.gotoview.clicked.connect(self.gotoviewlisting)

    def gobackwindow(self):
        self.close()
        if self.admin:
            self.app.callAdminWindow(self.userID)
        else:
            self.app.callMainWindow(self.userID)

    def fetchlistingID(self):
        row = self.vlistingstable.currentRow()
        self.currentListingID = int(self.vlistingstable.item(row, 0).text())

    def gotoviewlisting(self):
        self.fetchlistingID()
        self.close()
        self.app.callViewListingDetails(self.currentListingID,self.admin)

    def updatepreferences(self):
        self.query = 'SELECT listingID,title,price,condition,dateofend,format,delivery,quantity FROM listings WHERE active=1'
        self.setpreferences()
        self.loadTable()

    def setpreferences(self):
        if self.category.currentText() != "Select a Category":
            self.pcategory = self.category.currentText()
            self.query = (self.query + " AND category = '" + self.pcategory + "'")

        if self.condition.currentText() != "Select an Option":
            self.pcondition = self.condition.currentText()
            self.query = (self.query + " AND condition = '" + self.pcondition + "'")

        if self.deliveryoption.currentText() != "Select an Option":
            self.pdelivery = self.deliveryoption.currentText()
            self.query = (self.query + " AND delivery = '" + self.pdelivery + "'")

        if self.format.currentText() != "Select an Option":
            self.pformat = self.format.currentText()
            self.query = (self.query + " AND format = '" + self.pformat + "'")

    def loadTable(self):
        self.vlistingstable.setRowCount(0)

        self.cur.execute(str(self.query))
        results = self.cur.fetchall()
        self.vlistingstable.setRowCount(50)

        for row_number, row_data in enumerate(results):
            self.vlistingstable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.vlistingstable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        self.vlistingstable.setColumnHidden(0, True)

        header = self.vlistingstable.horizontalHeader()
        for i in range(7):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
