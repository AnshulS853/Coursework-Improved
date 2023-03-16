from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QTableWidgetItem

import sqlite3
import locale

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
        self.updatesummary()

        self.viewitem.clicked.connect(self.gotoitem)
        self.remitem.clicked.connect(self.removeitem)
        self.clearbask.clicked.connect(self.clearbasket)
        self.goback.clicked.connect(self.gobackwindow)
        self.checkout.clicked.connect(self.gotocheckout)

    def gobackwindow(self):
        self.close()
        if self.admin:
            self.app.callAdminWindow(self.userID)
        else:
            self.app.callMainWindow(self.userID)

    def updatesummary(self):
        self.cur.execute('SELECT * FROM basket WHERE purchased = 0')
        basket = self.cur.fetchall()

        itemsno = 0
        btotal = 0

        self.cur.execute('SELECT addressID FROM usad WHERE userID = ?',(self.userID,))
        self.addressID = self.cur.fetchone()[0]
        self.cur.execute('SELECT postcode FROM address WHERE addressID = ?',(self.addressID,))
        postcode = self.cur.fetchone()[0]

        locale.setlocale(locale.LC_ALL, 'en_GB.UTF-8')

        for i in basket:
            itemsno += i[3]

            self.cur.execute('SELECT price FROM listings WHERE listingID = ?',(i[2],))
            fetchprice = self.cur.fetchone()[0]
            # btotal += (float(fetchprice[1:])) * i[3]
            btotal += (locale.atof(fetchprice[1:])) * i[3]

        self.summary.setText("Number of Items: " + str(itemsno)
                             + "\nBasket total: " + str(locale.currency(btotal, grouping=True))
                             + "\nNon VAT total: " + str(locale.currency((0.8 * btotal), grouping=True))
                             + "\nPostage to: " + str(postcode))

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

    # def gotocheckout(self):
    #     cbasket = []
    #     for i in self.bItems:
    #         listingID = i[0]
    #         quantity = i[5]
    #         cbasket.append((listingID, quantity))

    def gotocheckout(self):
        self.checkout.setText('Purchase')
        self.checkout.clicked.connect(self.purchase)

    def purchase(self):
        c_basket = [(i[0], i[5]) for i in self.bItems]

        for i in c_basket:
            self.cur.execute('''
                            UPDATE listings SET quantity = 
                            CASE 
                              WHEN (quantity - ?) > 0 THEN (quantity - ?)
                              ELSE 0
                            END,
                            active = 
                            CASE
                              WHEN (quantity - ?) > 0 THEN active
                              ELSE 0
                            END
                            WHERE listingID = ?;
                            ''',(i[1],i[1],i[1],i[0]))

        for i in self.bItems:
            self.cur.execute('''
                            UPDATE basket
                            SET purchased = 1
                            WHERE listingID = ?
                            ''',(i[0],))


        ##Fetch buyer's address
        self.cur.execute('SELECT * FROM address WHERE addressID = ?', (self.addressID,))
        buyerAddress = self.cur.fetchall()[0]

        # concatenate first two indexes with a space
        first_part = buyerAddress[1] + ' ' + buyerAddress[2]
        # concatenate the rest of the indexes with a new line
        second_part = '\n'.join(buyerAddress[3:])
        # concatenate the two parts and store in a new variable
        s_buyerAddress = f"{first_part}\n{second_part}"
        # print the concatenated address

        self.cur.execute('''
                        INSERT INTO invoice
                        (buyerID,
                        purchasedate,
                        buyeraddress)
                        VALUES (?,DATE('now'),?)
                        ''',(self.userID,str(s_buyerAddress)))
        invoiceID = self.cur.lastrowid

        for i in c_basket:
            self.cur.execute('''
                            INSERT INTO binv
                            (basketID,invoiceID)
                            VALUES (?,?)
                            ''',(i[0],invoiceID))