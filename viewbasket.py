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

        # self.coupon = None
        # self.couponquantity = 0

        self.updatepreferences()
        self.updatesummary()

        self.applydiscount.clicked.connect(self.itemdiscount)
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


    def updatesummary(self,discountedprice=None,savings=None):
        dprice = discountedprice
        saved = savings

        self.cur.execute('SELECT * FROM basket WHERE purchased = 0')
        self.basket = self.cur.fetchall()

        itemsno = 0
        btotal = 0

        self.cur.execute('SELECT addressID FROM usad WHERE userID = ?',(self.userID,))
        self.addressID = self.cur.fetchone()[0]
        self.cur.execute('SELECT postcode FROM address WHERE addressID = ?',(self.addressID,))
        postcode = self.cur.fetchone()[0]

        locale.setlocale(locale.LC_ALL, 'en_GB.UTF-8')

        for i in self.basket:
            itemsno += i[3]

            self.cur.execute('SELECT price FROM listings WHERE listingID = ?',(i[2],))
            fetchprice = self.cur.fetchone()[0]
            # btotal += (float(fetchprice[1:])) * i[3]
            btotal += (locale.atof(fetchprice[1:])) * i[3]

        summary = ("Number of Items: " + str(itemsno)
                   + "\nPostage to: " + str(postcode)
                   + "\nNon VAT total: " + str(locale.currency((0.8 * btotal), grouping=True))
                   + "\nBasket total: " + str(locale.currency(btotal, grouping=True))
                   )

        if saved and dprice:
            summary = (str(summary) + "\n"
                       + "\nSavings: -" + str(saved)
                       + "\nFinal Total: " + str(locale.currency(dprice, grouping=True)))

        self.summary.setText(summary)

    # def itemdiscount(self):
    #     discount_code = self.discountfield.text()
    #
    #     self.cur.execute('SELECT listingID FROM basket WHERE purchased = 0 AND USERID = ?', (self.userID,))
    #     listingIDs = [row[0] for row in self.cur.fetchall()]
    #
    #     # make the discount code case and space insensitive by converting it to uppercase with no spaces
    #     discount_code = discount_code.upper().replace(' ', '')
    #
    #     self.cur.execute("SELECT * FROM coupons WHERE upper(trim(coupontag)) = ?", (discount_code,))
    #     coupon = self.cur.fetchone()
    #
    #     locale.setlocale(locale.LC_ALL, 'en_GB.UTF-8')
    #
    #     if coupon is None:
    #         self.error.setText("This discount code does not exist")
    #     else:
    #         usability = coupon[3]
    #         if usability == 'User':
    #             coupon_userID = coupon[5]
    #             self.cur.execute('SELECT listingID FROM listings WHERE sellerID = ?',(coupon_userID,))
    #             coupon_listingIDs = [row[0] for row in self.cur.fetchall()]
    #
    #             coupon_basket_listingIDs = (set(listingIDs).intersection(set(coupon_listingIDs)))
    #
    #             totalprice = 0
    #
    #             for i in coupon_basket_listingIDs:
    #                 self.cur.execute('SELECT price FROM listings WHERE listingID = ?', (i,))
    #                 price = self.cur.fetchone()[0]
    #                 self.cur.execute('SELECT quantity FROM basket WHERE listingID = ? AND purchased = 0 AND userID = ?',(i,self.userID))
    #                 quantity = self.cur.fetchone()[0]
    #
    #                 price = (locale.atof(price[1:])) * quantity
    #
    #                 totalprice += price
    #
    #             discount = coupon[4]
    #             discountedprice = (discount / 100) * (totalprice)
    #             savings = locale.currency(totalprice - discountedprice)
    #
    #             self.updatesummary(discountedprice, savings)
    #         else:
    #             usability = int(usability)
    #             if usability in listingIDs:
    #                 discount = coupon[4]
    #                 self.cur.execute('SELECT price FROM listings WHERE listingID = ?', (usability,))
    #                 price = self.cur.fetchone()[0]
    #                 self.cur.execute('SELECT quantity FROM basket WHERE listingID = ? AND purchased = 0 AND userID = ?',(usability,self.userID))
    #                 quantity = self.cur.fetchone()[0]
    #
    #                 price = (locale.atof(price[1:]))*quantity
    #                 discountedprice = (discount/100)*(price)
    #                 savings = locale.currency(price - discountedprice)
    #
    #                 self.updatesummary(discountedprice, savings)
    #             else:
    #                 self.error.setText("This discount code is invalid for your items")

    def itemdiscount(self):
        locale.setlocale(locale.LC_ALL, 'en_GB.UTF-8')
        discount_code = self.discountfield.text().upper().replace(' ', '')

        if not hasattr(self, 'coupon') or self.coupon[0] != discount_code:
            self.cur.execute("SELECT * FROM coupons WHERE upper(trim(coupontag)) = ?", (discount_code,))
            self.coupon = self.cur.fetchone()

        if self.coupon is None:
            self.error.setText("This discount code does not exist")
            self.updatesummary()
        else:
            usability = self.coupon[3]
            if usability == 'User':
                coupon_userID = self.coupon[5]
                self.cur.execute('SELECT listingID, price FROM listings WHERE sellerID = ?', (coupon_userID,))
                listing_prices = dict(self.cur.fetchall())

                coupon_basket_listingIDs = set()
                totalprice = 0

                self.cur.execute('''
                                SELECT basket.listingID, basket.quantity 
                                FROM basket JOIN listings 
                                ON basket.listingID = listings.listingID 
                                WHERE basket.purchased = 0 AND basket.userID = ?
                                ''',(self.userID,))

                for row in self.cur.fetchall():
                    listingID, quantity = row
                    if listingID in listing_prices:
                        # self.couponquantity += quantity
                        price = listing_prices[listingID]
                        price = (locale.atof(price[1:]))
                        totalprice += price * quantity
                        coupon_basket_listingIDs.add(listingID)

                discount = self.coupon[4]
                discounted_prices = [(locale.atof((listing_prices[listingID])[1:])) * (1 - discount / 100) for listingID in
                                     coupon_basket_listingIDs]
                discountedprice = sum(discounted_prices)
                savings = locale.currency(totalprice - discountedprice)

                self.updatesummary(discountedprice, savings)
            else:
                usability = int(usability)
                self.cur.execute(
                    '''SELECT listings.price, basket.quantity 
                    FROM listings JOIN basket USING (listingID) 
                    WHERE listings.listingID = ? AND basket.purchased = 0 AND basket.userID = ?''',
                    (usability, self.userID))
                row = self.cur.fetchone()
                if row is None:
                    self.error.setText("This discount code is invalid for your items")
                    self.updatesummary()
                else:
                    price, quantity = row
                    price = (locale.atof(price[1:]))
                    discountedprice = float(price) * int(quantity) * (1 - self.coupon[4] / 100)
                    savings = locale.currency(price * quantity - discountedprice)
                    self.updatesummary(discountedprice, savings)

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

        if hasattr(self, 'coupon'):
            self.cur.execute('''
                            INSERT INTO invoice
                            (buyerID,
                            couponID,
                            purchasedate,
                            buyeraddress)
                            VALUES (?,?,DATE('now'),?)
                            ''',(self.coupon[1],self.userID,str(s_buyerAddress)))

            # self.cur.execute('''
            #                 UPDATE coupons
            #                 SET quantity = quantity - ?
            #                 WHERE couponID = ?
            #                 ''',(int(self.couponquantity),self.coupon[0]))
        else:
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

        self.close()
        if self.admin:
            self.app.callAdminWindow(self.userID)
        else:
            self.app.callMainWindow(self.userID)
