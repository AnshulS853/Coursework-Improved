# from PyQt5.uic import loadUi
# from PyQt5.QtWidgets import QDialog
#
# import sqlite3
# import datetime
# from datetime import datetime
#
# class viewListDetails(QDialog):
#     def __init__(self, app, lid, uid, admin):
#         super(viewListDetails, self).__init__()
#         loadUi("listdetails.ui", self)
#         self.app = app
#         self.admin = admin
#         self.userID = uid
#         self.listingID = lid
#         self.goback.clicked.connect(self.gobackpage)
#         self.continuepage.clicked.connect(self.confirmpurchase)
#
#         self.postcode = None
#
#         self.conn = sqlite3.connect("auc_database.db",isolation_level=None)
#         self.cur = self.conn.cursor()
#
#         self.fetchresult()
#         self.setbuttontext()
#         self.insertdetails()
#
#     def gobackpage(self):
#         self.close()
#         self.app.callViewListings(self.userID,self.admin)
#
#     def fetchresult(self):
#         self.cur.execute('SELECT * FROM listings WHERE listingID = ?',(self.listingID,))
#         self.result = self.cur.fetchall()
#         self.result = self.result[0]
#
#     def setbuttontext(self):
#         if self.result[5] == "Auction":
#             self.continuepage.setText("Place a Bid")
#             self.pricefield.setText("Starting Price:\n"+str(self.result[7]))
#         else:
#             self.continuepage.setText("Purchase Item")
#             self.pricefield.setText(self.result[7])
#
#
#     def calculatedatediff(self):
#         now = datetime.now().date()
#         date = datetime.strptime(self.result[6], '%Y-%m-%d').date()
#
#         difference = date - now
#
#         years = difference.days // 365
#         months = (difference.days - years * 365) // 30
#         days = (difference.days - years * 365 - months * 30)
#
#         remainingduration = (str(years)+" Years\n"+str(months)+" Months\n"+str(days)+" Days\n")
#         return remainingduration
#
#     def fetchdeliverylocation(self):
#         self.cur.execute('SELECT addressID from usad WHERE userID = ?',(self.result[10],))
#         addressID = self.cur.fetchall()
#         addressID = addressID[0][0]
#         self.cur.execute('SELECT postcode from address WHERE addressID = ?',(addressID,))
#         postcode = self.cur.fetchall()
#         postcode = postcode[0][0]
#         return postcode
#
#     def insertdetails(self):
#         self.titlefield.setText(self.result[1])
#         self.descfield.setText(self.result[2])
#         self.categoryfield.setText(self.result[3])
#         self.conditionfield.setText(self.result[4])
#         self.formatfield.setText(self.result[5])
#
#         remainingduration = self.calculatedatediff()
#         self.durationfield.setText(str(remainingduration))
#         self.deliveryfield.setText(self.result[8])
#
#         self.postcode = self.fetchdeliverylocation()
#         self.deliverylocation.setText("Item is located near\n" + str(self.postcode))
#
    # def confirmpurchase(self):
    #     if self.result[5] == "Auction":
    #         self.close()
    #         self.app.callAuctionBids(self.userID,self.listingID,self.admin,self.postcode)
    #     else:
    #         self.continuepage.setText("Confirm Purchase")
    #         self.continuepage.clicked.connect(self.purchase)
    #
    # def purchase(self):
    #     self.cur.execute('''
    #                     INSERT INTO invoice
    #                     (listingID,
    #                     buyerID,
    #                     total,
    #                     purchasedate)
    #                     VALUES (?,?,?,DATE('now'))
    #                     ''', (self.listingID, self.userID, self.result[7]))
    #     invoiceID = self.cur.lastrowid
    #
    #     self.cur.execute('''
    #                     UPDATE listings
    #                     SET active=0
    #                     WHERE listingID = (?)
    #                     ''', (self.listingID,))
    #
    #     self.close()
    #     self.app.callCreateInvoice(self.listingID,self.userID,invoiceID,self.admin)

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog

import sqlite3
import datetime
from datetime import datetime

class viewListDetails(QDialog):
    def __init__(self, app, lid, uid, admin):
        super(viewListDetails, self).__init__()
        loadUi("listdetails.ui", self)
        self.app = app
        self.admin = admin
        self.userID = uid
        self.listingID = lid
        self.goback.clicked.connect(self.gobackpage)
        self.continuebasket.clicked.connect(self.confirmpurchase)

        self.postcode = None
        self.quantity = 1

        self.conn = sqlite3.connect("auc_database.db",isolation_level=None)
        self.cur = self.conn.cursor()

        self.fetchresult()
        self.setbuttontext()
        self.insertdetails()

    def gobackpage(self):
        self.close()
        self.app.callViewListings(self.userID,self.admin)

    def fetchresult(self):
        self.cur.execute('SELECT * FROM listings WHERE listingID = ?',(self.listingID,))
        self.result = self.cur.fetchall()[0]

    def setbuttontext(self):
        if self.result[5] == "Auction":
            self.continuebasket.setText("Place a Bid")
            self.quantityfield.setReadOnly(True)
            self.quantityfield.setText("1")
            self.pricefield.setText("Starting Price:\n"+str(self.result[7]))
        else:
            self.cur.execute('SELECT quantity FROM listings WHERE listingID = ?',(self.listingID,))
            self.maxquantity = self.cur.fetchall()[0][0]
            self.quantityfield.setText("MAX: "+ str(self.maxquantity))
            self.pricefield.setText(self.result[7])


    def calculatedatediff(self):
        now = datetime.now().date()
        date = datetime.strptime(self.result[6], '%Y-%m-%d').date()

        difference = date - now

        years = difference.days // 365
        months = (difference.days - years * 365) // 30
        days = (difference.days - years * 365 - months * 30)

        remainingduration = (str(years)+" Years\n"+str(months)+" Months\n"+str(days)+" Days\n")
        return remainingduration

    def fetchdeliverylocation(self):
        self.cur.execute('SELECT addressID from usad WHERE userID = ?',(self.result[10],))
        addressID = self.cur.fetchall()
        addressID = addressID[0][0]
        self.cur.execute('SELECT postcode from address WHERE addressID = ?',(addressID,))
        postcode = self.cur.fetchall()
        postcode = postcode[0][0]
        return postcode

    def insertdetails(self):
        self.titlefield.setText(self.result[1])
        self.descfield.setText(self.result[2])
        self.categoryfield.setText(self.result[3])
        self.conditionfield.setText(self.result[4])
        self.formatfield.setText(self.result[5])

        remainingduration = self.calculatedatediff()
        self.durationfield.setText(str(remainingduration))
        self.deliveryfield.setText(self.result[8])

        self.postcode = self.fetchdeliverylocation()
        self.deliverylocation.setText("Item is located near\n" + str(self.postcode))


    def validatequantity(self):
        quantity_text = self.quantityfield.text()
        if not quantity_text.isdigit():
            self.error.setText("Enter a valid quantity")
            return
        self.quantity = int(quantity_text)
        if self.quantity > self.maxquantity:
            self.error.setText("Quantity must be lower than max")
            return
        else:
            return True

    def confirmpurchase(self):
        if self.result[5] == "Auction":
            self.close()
            self.app.callAuctionBids(self.userID,self.listingID,self.admin,self.postcode)
        else:
            if self.validatequantity():
                self.cur.execute('''
                                INSERT INTO basket
                                (userID,
                                listingID,
                                quantity,
                                purchased,
                                creationdate)
                                VALUES (?,?,?,0,DATE('now'))
                                ''', (self.userID, self.listingID, self.quantity))
                self.basketID = self.cur.lastrowid

                self.close()
                if self.admin:
                    self.app.callAdminWindow(self.userID)
                else:
                    self.app.callMainWindow(self.userID)

