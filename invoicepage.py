from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog,QTableWidgetItem

import sqlite3
import locale

class createInvoice(QDialog):
    def __init__(self, app, bid, uid ,admin):
        super(createInvoice, self).__init__()
        loadUi("invoice.ui", self)
        # connecting buttons to functions when clicked
        self.app = app
        self.currentBasketID = bid
        self.userID = uid
        self.admin = admin

        self.goback.clicked.connect(self.gobackpage)

        self.conn = sqlite3.connect("auc_database.db",isolation_level=None)
        self.cur = self.conn.cursor()

        self.fetchbaskinv()
        self.loadTable()
        self.populatefields()

        # self.fetchresult()
        # self.setfields()

    def gobackpage(self):
        if self.admin:
            self.close()
            self.app.callAdminWindow(self.userID)
        else:
            self.close()
            self.app.callMainWindow(self.userID)

    def fetchbaskinv(self):
        self.cur.execute('SELECT invoiceID FROM binv WHERE basketID = ?',(self.currentBasketID,))
        self.invoiceID = self.cur.fetchone()[0]

        self.cur.execute('SELECT basketID FROM binv WHERE invoiceID = ?',(self.invoiceID,))
        self.basketIDs = self.cur.fetchall()

    def fetchtable(self):
        tablecontents = []
        for i in self.basketIDs:
            self.cur.execute('SELECT basketID,listingID,quantity,creationdate FROM basket WHERE basketID = ? AND purchased = 1',(i[0],))
            self.basket = self.cur.fetchall()

            for j in self.basket:
                self.cur.execute('SELECT title,price FROM listings WHERE listingID = ?',(j[1],))
                tipri = self.cur.fetchone()
                tablecontents.append((tipri[0],j[2],tipri[1]))

        return tablecontents

    def loadTable(self):
        results = self.fetchtable()
        self.ilistingstable.setRowCount(0)

        self.ilistingstable.setRowCount(50)

        for row_number, row_data in enumerate(results):
            self.ilistingstable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.ilistingstable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        header = self.ilistingstable.horizontalHeader()
        for i in range(3):
            header.setSectionResizeMode(i,QtWidgets.QHeaderView.Stretch)

    def populatefields(self):
        self.cur.execute('SELECT purchasedate,buyeraddress FROM invoice WHERE invoiceID = ?',(self.invoiceID,))
        invoicedet = self.cur.fetchone()

        self.deliveredtofield.setText(invoicedet[1])

        self.invIDfield.setText(str(self.invoiceID))
        self.invdatefield.setText(invoicedet[0])


    # def fetchinvoicedet(self):
    #     self.cur.execute('SELECT invoiceID FROM binv WHERE basketID = ?',(self.basketID,))
    #     invoiceID = self.cur.fetchone()
    #
    #     self.cur.execute('SELECT purchasedate,buyeraddress FROM invoice WHERE invoiceID = ?',(self.invoiceID,))

    # def fetchresult(self):
    #     self.cur.execute('SELECT * FROM listings WHERE listingID = ?',(self.listingID,))
    #     self.result = self.cur.fetchall()
    #     self.result = self.result[0]
    #
    # def fetchinvoicedetails(self):
    #     self.cur.execute('SELECT buyerID,purchasedate,total FROM invoice WHERE invoiceID = ?',(self.invoiceID,))
    #     self.invoicedetails = self.cur.fetchall()
    #     self.invoicedetails = self.invoicedetails[0]
    #
    #     self.buyerID = self.invoicedetails[0]
    #     print(self.buyerID)
    #
    #     self.fetchdeliveredto()
    #     self.fetchdeliveredfrom()
    #
    # def pricetoint(self,raw_price):
    #     locale.setlocale(locale.LC_ALL, 'en_GB')
    #     conv = locale.localeconv()
    #     raw_numbers = raw_price.strip(conv['currency_symbol'])
    #     amount = locale.atof(raw_numbers)
    #     return amount
    #
    # def checkprice(self, price):
    #     price = float(price)
    #     locale.setlocale(locale.LC_ALL, 'en_GB')
    #     price = locale.currency(price, grouping=True)
    #     return price
    #
    # def fetchdeliveredto(self):
    #     self.cur.execute('SELECT addressID from usad WHERE userID = ?',(self.buyerID,))
    #     addressID = self.cur.fetchall()
    #     addressID = addressID[0][0]
    #
    #     self.cur.execute('SELECT houseno,addfield1,addfield2,postcode,county FROM address WHERE addressID = ?', (addressID,))
    #     buyeraddress = self.cur.fetchall()
    #     buyeraddress = buyeraddress[0]
    #
    #     for i in buyeraddress:
    #         if i is not None:
    #             self.buyeraddress = (str(self.buyeraddress) + str(i) + "\n")
    #         else:
    #             pass
    #
    # def fetchdeliveredfrom(self):
    #     self.cur.execute('SELECT sellerID FROM listings WHERE listingID = ?', (self.listingID,))
    #     self.sellerID = self.cur.fetchall()
    #     self.sellerID = self.sellerID[0][0]
    #
    #     self.cur.execute('SELECT addressID from usad WHERE userID = ?',(self.sellerID,))
    #     addressID = self.cur.fetchall()
    #     addressID = addressID[0][0]
    #
    #     self.cur.execute('SELECT houseno,addfield1,addfield2,postcode,county FROM address WHERE addressID = ?', (addressID,))
    #     selleraddress = self.cur.fetchall()
    #     selleraddress = selleraddress[0]
    #
    #     for i in selleraddress:
    #         if i is not None:
    #             self.selleraddress = (str(self.selleraddress) + str(i) + "\n")
    #         else:
    #             pass
    #
    #
    # def setfields(self):
    #     self.fetchinvoicedetails()
    #
    #     #Product Details
    #     self.titlefield.setText(self.result[1])
    #     self.categoryfield.setText(self.result[3])
    #     self.conditionfield.setText(self.result[4])
    #     self.sellerIDfield.setText(str(self.sellerID))
    #     self.categoryfield.setText(self.result[3])
    #     self.deliveryfield.setText(self.result[8])
    #     self.formatfield.setText(self.result[5])
    #
    #     #Delivery Fields
    #     self.deliveredfromfield.setText(self.selleraddress)
    #     self.deliveredtofield.setText(self.buyeraddress)
    #
    #     #Invoice Details
    #     self.invoiceIDfield.setText(str(self.invoiceID))
    #     self.invoicedatefield.setText(str(self.invoicedetails[1]))
    #     self.agreedpricefield.setText(str(self.invoicedetails[2]))
    #
    #     #Price Subtotal
    #     self.listedpricefield.setText(str(self.result[7]))
    #     self.finalpricefield.setText(str(self.invoicedetails[2]))
    #     self.businesscomfield.setText(str(self.checkprice(int(self.pricetoint(self.invoicedetails[2]))*0.15)))
    #     self.amountduefield.setText(str(self.invoicedetails[2]))







