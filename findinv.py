from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog,QTableWidgetItem

import sqlite3

class findInvoices(QDialog):
    def __init__(self,app,uid,admin):
        super(findInvoices, self).__init__()
        loadUi("findinv.ui", self)
        self.confirmtoast.setText("")
        self.app = app
        self.userID = uid
        self.admin = admin

        self.currentBasketID = None

        self.conn = sqlite3.connect("auc_database.db", isolation_level=None)
        self.cur = self.conn.cursor()


        self.goback.clicked.connect(self.gotomenu)
        self.view.clicked.connect(self.gotoinvoice)
        self.loadTable()

    def gotomenu(self):
        self.close()
        if self.admin:
            self.app.callAdminWindow(self.userID)
        else:
            self.app.callMainWindow(self.userID)

    def fetchBasketID(self):
        try:
            row = self.ilistingstable.currentRow()
            self.currentBasketID = int(self.ilistingstable.item(row, 0).text())
            return True
        except:
            self.confirmtoast.setText("Select a\nRecord")
            return
    def gotoinvoice(self):
        if self.fetchBasketID() is True:
            self.close()
            self.app.callCreateInvoice(self.currentBasketID, self.admin)

    #     self.cur.execute('SELECT invoiceID FROM invoice WHERE listingID = ?',(self.currentListingID,))
    #     invoiceID = self.cur.fetchall()
    #     try:
    #         invoiceID = invoiceID[0][0]
    #         self.close()
    #         self.app.callCreateInvoice(self.currentListingID,self.userID,invoiceID,self.admin)
    #     except:
    #         self.confirmtoast.setText('Select one\nrecord')

    # def fetchlistingsbought(self):
    #     invdetails = []
    #
    #     self.cur.execute('SELECT basketID,listingID,quantity FROM basket WHERE purchased = 1')
    #     idquant = self.cur.fetchall()
    #
    #     for i in idquant:
    #         self.cur.execute('SELECT title,price FROM listings WHERE listingID = ?',(i[1],))
    #         tipri = self.cur.fetchall()[0]
    #
    #         self.cur.execute('SELECT invoiceID from binv WHERE basketID = ?',(i[0],))
    #         invoiceID = self.cur.fetchone()[0]
    #
    #         self.cur.execute('SELECT purchasedate FROM invoice WHERE invoiceID = ?',(invoiceID,))
    #         purchasedate = self.cur.fetchone()[0]
    #
    #         invdetails.append((i[0], tipri[0], i[2], tipri[1], purchasedate))
    #
    #     return invdetails

    def fetchlistingsbought(self):
        invdetails = []

        self.cur.execute('''
            SELECT b.listingID, l.title, b.quantity, l.price, i.purchasedate 
            FROM basket b 
            INNER JOIN listings l ON b.listingID = l.listingID 
            INNER JOIN binv bi ON b.basketID = bi.basketID 
            INNER JOIN invoice i ON bi.invoiceID = i.invoiceID 
            WHERE b.purchased = 1 AND b.userID = ?
            ''',(self.userID,))

        rows = self.cur.fetchall()

        for row in rows:
            invdetails.append(row)

        return invdetails

    def loadTable(self):
        results = self.fetchlistingsbought()
        self.ilistingstable.setRowCount(0)

        self.ilistingstable.setRowCount(50)

        for row_number, row_data in enumerate(results):
            self.ilistingstable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.ilistingstable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        self.ilistingstable.setColumnHidden(0, True)
        header = self.ilistingstable.horizontalHeader()
        for i in range(5):
            header.setSectionResizeMode(i,QtWidgets.QHeaderView.Stretch)
