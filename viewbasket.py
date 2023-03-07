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

        self.goback.clicked.connect(self.gobackwindow)

    def gobackwindow(self):
        if self.admin:
            self.close()
            self.app.callAdminWindow(self.userID)
        else:
            self.close()
            self.app.callMainWindow(self.userID)

    def updatepreferences(self):
        self.cur.execute('SELECT listingID,quantity FROM basket WHERE userID = ? AND purchased = 0',(self.userID,))
        fetchbasket = self.cur.fetchall()

        self.bItems = []

        for i in fetchbasket:
            self.cur.execute('SELECT title,price,format,delivery FROM listings WHERE listingID = ?',(i[0],))
            query = self.cur.fetchall()[0]
            query = list(query)
            query.append(i[1])
            print(self.bItems)
            query = tuple(query)
            print(query)
            self.bItems.append(query)
            print(self.bItems)

        self.loadTable()

    def loadTable(self):
        self.btable.setRowCount(0)
        self.btable.setRowCount(50)

        for row_number, row_data in enumerate(self.bItems):
            self.btable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.btable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        header = self.btable.horizontalHeader()
        for i in range(4):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
