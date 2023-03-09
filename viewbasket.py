from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QTableWidgetItem

import sqlite3

class viewBasket(QDialog):
    def __init__(self, app, uid, admin):
        super(viewBasket, self).__init__()
        loadUi("mybasket.ui", self)
        self.app = app
        self.admin = admin
        self.userID = uid

        self.conn = sqlite3.connect("auc_database.db", isolation_level=None)
        self.cur = self.conn.cursor()

        self.updatepreferences()

        self.viewitem.clicked.connect(self.gotoitem)
        self.remitem.clicked.connect(self.removeitem)
        self.clearbask.clicked.connect(self.clearbasket)
        self.goback.clicked.connect(self.gobackwindow)

    def gobackwindow(self):
        self.close()
        if self.admin:
            self.app.callAdminWindow(self.userID)
        else:
            self.app.callMainWindow(self.userID)

    def fetchlistingID(self):
        row = self.btable.currentRow()
        self.currentListingID = int(self.btable.item(row, 0).text())

    def gotoitem(self):
        self.fetchlistingID()
        self.close()
        self.app.callViewListingDetails(self.currentListingID,self.admin)

    def removeitem(self):
        self.fetchlistingID()
        self.cur.execute('DELETE FROM basket WHERE listingID = ? AND purchased = 0 ',(self.currentListingID,))
        self.updatepreferences()

    def clearbasket(self):
        self.cur.execute('DELETE FROM basket WHERE purchased = 0')
        self.updatepreferences()

    def updatepreferences(self):
        self.cur.execute('''
            SELECT l.listingID, l.title, l.price, l.format, l.delivery, b.quantity
            FROM basket b
            JOIN listings l ON b.listingID = l.listingID
            WHERE b.userID = ? AND b.purchased = 0
        ''', (self.userID,))
        fetchbasket = self.cur.fetchall()

        self.bItems = [tuple(row) for row in fetchbasket]

        self.loadTable()

    def loadTable(self):
        self.btable.setRowCount(0)
        self.btable.setRowCount(50)

        for row_number, row_data in enumerate(self.bItems):
            self.btable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.btable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        self.btable.setColumnHidden(0, True)

        header = self.btable.horizontalHeader()
        for i in range(6):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
