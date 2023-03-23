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

        self.currentListingID = None

        self.conn = sqlite3.connect("auc_database.db",isolation_level=None)
        self.cur = self.conn.cursor()



        self.goback.clicked.connect(self.gotomenu)
    #     self.view.clicked.connect(self.gotoinvoice)
        self.loadTable()
    #
    def gotomenu(self):
        if self.admin:
            self.close()
            self.app.callAdminWindow(self.userID)
        else:
            self.close()
            self.app.callMainWindow(self.userID)
    #
    # def fetchlistingID(self):
    #     try:
    #         row = self.ilistingstable.currentRow()
    #         self.currentListingID = int(self.ilistingstable.item(row, 0).text())
    #     except:
    #         self.confirmtoast.setText("Select a\nRecord")
    #
    # def gotoinvoice(self):
    #     self.fetchlistingID()
    #     self.cur.execute('SELECT invoiceID FROM invoice WHERE listingID = ?',(self.currentListingID,))
    #     invoiceID = self.cur.fetchall()
    #     try:
    #         invoiceID = invoiceID[0][0]
    #         self.close()
    #         self.app.callCreateInvoice(self.currentListingID,self.userID,invoiceID,self.admin)
    #     except:
    #         self.confirmtoast.setText('Select one\nrecord')

    def fetchlistingsbought(self):
        # self.cur.execute('SELECT listingID FROM invoice WHERE buyerID = ?',(self.userID,))
        # buyerIDs = self.cur.fetchall()
        # # print("buyerIDs = ",buyerIDs)
        #
        #
        # self.cur.execute('SELECT listingID FROM listings WHERE sellerID = ? AND active=0',(self.userID,))
        # listingIDs = self.cur.fetchall()
        # # print("listingIDs",listingIDs)
        #
        # self.insertlist = []
        #
        # if buyerIDs:
        #     for i in buyerIDs:
        #         i = i[0]
        #         self.insertlist.append(i)
        #
        # if listingIDs:
        #     for i in listingIDs:
        #         i = i[0]
        #         self.cur.execute('SELECT COUNT(listingID) FROM invoice WHERE listingID=?',(i,))
        #         result = self.cur.fetchall()
        #         result = result[0][0]
        #         if result == 0:
        #             pass
        #         else:
        #             self.insertlist.append(i)

        invdetails = []

        self.cur.execute('SELECT basketID,listingID,quantity FROM basket WHERE purchased = 1')
        idquant = self.cur.fetchall()


        for i in idquant:
            self.cur.execute('SELECT title,price FROM listings WHERE listingID = ?',(i[1],))
            tipri = self.cur.fetchall()[0]

            self.cur.execute('SELECT invoiceID from binv WHERE basketID = ?',(i[0],))
            invoiceID = self.cur.fetchone()[0]

            self.cur.execute('SELECT purchasedate FROM invoice WHERE invoiceID = ?',(invoiceID,))
            purchasedate = self.cur.fetchone()[0]

            invdetails.append((i[1], tipri[0], i[2], tipri[1], purchasedate))

        return invdetails



    def loadTable(self):
        results = self.fetchlistingsbought()
        self.ilistingstable.setRowCount(0)

        # print(results)
        self.ilistingstable.setRowCount(50)

        for row_number, row_data in enumerate(results):
            self.ilistingstable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.ilistingstable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        self.ilistingstable.setColumnHidden(0, True)
        header = self.ilistingstable.horizontalHeader()
        for i in range(5):
            header.setSectionResizeMode(i,QtWidgets.QHeaderView.Stretch)
