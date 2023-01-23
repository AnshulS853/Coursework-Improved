from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog

from datetime import datetime

from databasefunction import databaseClass
import sqlite3
import locale
import time

class auctionBids(QDialog):
    def __init__(self, app, bID, lID, admin, postcode):
        super(auctionBids, self).__init__()
        loadUi("placebid.ui", self)
        # connecting buttons to functions when clicked
        self.app = app
        self.buyerID = bID
        self.admin = admin
        self.listingID = lID
        self.postcode = postcode

        self.result = None
        self.buyerBid = None
        self.bidDetails = None
        self.new = False

        self.goback.clicked.connect(self.gobackpage)
        self.continuepage.clicked.connect(self.confirmbid)

        self.conn = sqlite3.connect("auc_database.db",isolation_level=None)
        self.cur = self.conn.cursor()

        self.fillFields()

    def gobackpage(self):
        self.close()
        self.app.callViewListings(self.buyerID,self.admin)

    def checkprice(self, price):
        try:
            price = float(price)
            locale.setlocale(locale.LC_ALL, 'en_GB')
            price = locale.currency(price, grouping=True)
            return price
        except:
            self.confirmtoast.setText("Price must in a valid format")
            return

    def pricetoint(self,raw_price):
        locale.setlocale(locale.LC_ALL, 'en_GB')
        conv = locale.localeconv()
        raw_numbers = raw_price.strip(conv['currency_symbol'])
        amount = locale.atof(raw_numbers)
        return amount

    def validatebid(self):
        try:
            buyerBid = float(self.biddingfield.text())
        except:
            self.confirmtoast.setText("Enter a valid Bid")
            return
        self.buyerBid = self.checkprice(buyerBid)
        if self.bidDetails is None:
            bidPrice = float(self.pricetoint(self.result[7]))
        else:
            bidPrice = float(self.pricetoint(self.bidDetails[0]))

        if buyerBid > bidPrice:
            return True
        else:
            self.confirmtoast.setText("Invalid Bid.\nMust be greater\nthan highest bid")
            return

    def acceptconditions(self):
        if self.acceptcondition.isChecked():
            return True
        else:
            self.confirmtoast.setText("You must accept\nto the terms")
            return

    def confirmbid(self):
        if self.acceptconditions() is True:
            if self.validatebid() is True:
                self.continuepage.setText("Confirm")
                self.confirmtoast.setText("Confirm your bid\nplacement of\n"+str(self.buyerBid))
                self.continuepage.clicked.connect(self.saveBid)
        else:
            self.confirmtoast.setText("You must accept\nto the terms")

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

    def fillFields(self):
        self.confirmtoast.setText("")
        self.cur.execute('SELECT * FROM listings WHERE listingID = ?',(self.listingID,))
        self.result = self.cur.fetchall()
        self.result = self.result[0]

        self.titlefield.setText(self.result[1])

        remainingduration = self.calculatedatediff()
        self.durationfield.setText(str(remainingduration))
        self.deliveryfield.setText(self.result[8])
        self.deliverylocation.setText("Item is located near\n" + str(self.postcode))

        self.cur.execute('SELECT highestBid, bidDate FROM auctions WHERE listingID = ?', (self.listingID,))
        bidDetails = self.cur.fetchall()
        if not bidDetails:
            self.new = True
            self.highestbidfield.setText(str(self.result[7]))
        else:
            self.bidDetails = bidDetails[0]
            self.highestbidfield.setText(str(self.bidDetails[0]))
            self.bidtimefield.setText(str(self.bidDetails[1]))

    def saveBid(self):
        self.confirmtoast.setText("Bid Placed \nSuccessfully")
        today = datetime.now().date()
        xtime = datetime.today().strftime("%H:%M %p")
        bidTime = (str(today)+"\n"+str(xtime))

        bid = (self.listingID, self.buyerBid, bidTime)

        if self.new is True:
            x = databaseClass(self.buyerID)
            x.insertbid(bid)
        else:
            x = databaseClass(self.buyerID)
            x.updatebid(bid)
        time.sleep(8)
        #Created illusion to the user that their bid has been saved successfully
        #stops the user doubting

        if self.admin is True:
            self.close()
            self.app.callAdminWindow(self.buyerID)
        else:
            self.close()
            self.app.callMainWindow(self.buyerID)
