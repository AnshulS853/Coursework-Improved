from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QTableWidgetItem

import sqlite3

class viewListings(QDialog):
    def __init__(self, app, uid, admin):
        super(viewListings, self).__init__()
        loadUi("viewlists.ui", self)
        self.confirmtoast.setText("")
        self.app = app
        self.userID = uid
        self.admin = admin
        self.currentListingID = None
        self.highlightedname = None
        self.query = None
        # self.check = False

        # self.isselected = None

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
        if self.admin:
            self.close()
            self.app.callAdminWindow(self.userID)
        else:
            self.close()
            self.app.callMainWindow(self.userID)

    def fetchlistingID(self):
        row = self.vlistingstable.currentRow()
        self.currentListingID = int(self.vlistingstable.item(row, 0).text())
        # self.confirmtoast.setText("Please select one Listing")

    def gotoviewlisting(self):
        self.fetchlistingID()
        self.close()
        self.app.callViewListingDetails(self.currentListingID,self.admin)

    def updatepreferences(self):
        # self.isselected = False
        self.query = 'SELECT listingID,title,price,condition,dateofend,format,delivery FROM listings WHERE active=1'
        self.setpreferences()
        # self.number = 0
        # self.check = True
        self.loadTable()

    def setpreferences(self):
        if self.category.currentText() != "Select a Category":
            self.pcategory = self.category.currentText()
            self.query = (self.query + " AND category = '" + self.pcategory + "'")
            # self.isselected = True

            # self.number += 1
            # if self.number > 1:
            #     self.query = (self.query + 'AND category = ? ')
            # else:
            #     self.query = (self.query + ' category = ? ')

        if self.condition.currentText() != "Select an Option":
            self.pcondition = self.condition.currentText()
            self.query = (self.query + " AND condition = '" + self.pcondition + "'")

            # if self.isselected:
            #     self.query = (self.query + " AND condition = '" + self.pcondition + "'")
            # else:
            #     self.query = (self.query + "condition = '" + self.pcondition + "'")
            #     self.isselected = True

        if self.deliveryoption.currentText() != "Select an Option":
            self.pdelivery = self.deliveryoption.currentText()
            self.query = (self.query + " AND delivery = '" + self.pdelivery + "'")

            # if self.isselected:
            #     self.query = (self.query + " AND delivery = '" + self.pdelivery + "'")
            # else:
            #     self.query = (self.query + "delivery = '" + self.pdelivery + "'")
            #     self.isselected = True

        if self.format.currentText() != "Select an Option":
            self.pformat = self.format.currentText()
            self.query = (self.query + " AND format = '" + self.pformat + "'")

            # if self.isselected:
            #     self.query = (self.query + " AND format = '" + self.pformat + "'")
            # else:
            #     self.query = (self.query + "format = '" + self.pformat + "'")
            #     self.isselected = True

    def loadTable(self):
        self.vlistingstable.setRowCount(0)
        # if self.number == 0:
        #     self.check = False

        # if self.check:
        #     # self.cur.execute('SELECT title,price,condition,dateofend,format,delivery FROM listings WHERE condition=? AND category=? AND delivery=? AND format=? LIMIT 50',
        #     #                  (self.pcondition,self.pcategory,self.pdelivery,self.pformat))
        #     print(self.query)
        #     self.cur.execute(str(self.query))
        # else:
        #     self.cur.execute('SELECT title,price,condition,dateofend,format,delivery FROM listings WHERE active=1 LIMIT 50')

        self.cur.execute(str(self.query))
        results = self.cur.fetchall()
        self.vlistingstable.setRowCount(50)

        for row_number, row_data in enumerate(results):
            self.vlistingstable.insertRow(row_number)
            # for column_number, data in enumerate(row_data[0:len(row_data)-1]):
            for column_number, data in enumerate(row_data):
                self.vlistingstable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        self.vlistingstable.setColumnHidden(0, True)

        header = self.vlistingstable.horizontalHeader()
        for i in range(6):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
