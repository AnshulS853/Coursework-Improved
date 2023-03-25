from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog

from datetime import datetime, timedelta
import sqlite3
import locale

class creationScreen(QDialog):
    def __init__(self, app, uid, admin):
        super(creationScreen, self).__init__()
        loadUi("createlisting.ui", self)
        self.app = app
        self.userID = uid
        self.admin = admin

        self.goback.clicked.connect(self.gobacktomenu)
        self.continuepage.clicked.connect(self.createwindow)
        self.format.currentIndexChanged.connect(self.checkFormat)

    def checkFormat(self):
        if self.format.currentText() == "Auction":
            self.quantityfield.setEnabled(False)
            self.quantityfield.setText("1")
            self.itemquantity = 1

            self.couponfield.setEnabled(False)
            self.couponfield.setText("N/A (Auction)")
        else:
            self.quantityfield.setEnabled(True)
            self.itemquantity = self.quantityfield.text()

            self.couponfield.setEnabled(True)
            self.couponfield.setText("No Coupon (Current)")
            try:
                self.itemquantity = int(self.itemquantity)
                if self.itemquantity < 0:
                    return
                else:
                    return True
            except:
                self.error.setText("Enter quantity as a positive integer")
                return

    def gobacktomenu(self):
        if self.admin:
            self.close()
            self.app.callAdminWindow(self.userID)
        else:
            self.close()
            self.app.callMainWindow(self.userID)

    def selectoption(self, selectx):
        for i in range(len(selectx)):
            var = selectx[i]
            if (var == "Select a Category") or (var == "Select an Option"):
                self.error.setText("Please make sure all boxes are selected")
                return
            else:
                i += 1
        return True

    def emptyfield(self, field):
        for i in range(len(field)):
            if len(field[i]) == 0:
                self.error.setText("Fields cannot be empty")
                return
            else:
                i += 1
        return True

    def calcend_date(self, duration, durationunits):
        if durationunits == "Days":
            self.end_date = datetime.now().date() + timedelta(days=duration)
        elif durationunits == "Months":
            month = datetime.now().month - 1 + duration
            year = datetime.now().year + month // 12
            month = month % 12 + 1
            self.end_date = datetime(year, month, 1) - timedelta(days=1)
        elif durationunits == "Years":
            self.end_date = datetime(datetime.now().year + duration, 12, 31).date()

    def checkduration(self, duration):
        self.duration = duration
        try:
            self.duration = int(self.duration)
            if self.duration < 1:
                return
            else:
                self.calcend_date(self.duration, self.durationunits.currentText())
                return self.duration
        except:
            self.error.setText("Please enter a valid duration")
            return

    def checkprice(self, price):
        self.price = price
        try:
            self.price = float(self.price)
            if self.price <= 0:
                raise ValueError
            return True
        except:
            self.error.setText("Price must be a positive number")
            return

    def acceptconditions(self):
        if self.acceptcondition.isChecked():
            return True
        else:
            self.error.setText("You must accept to the terms to use this service")
            return

    def durationlimit(self, durationunits, duration):
        if self.format.currentText() == "Auction":
            if durationunits == "Days" and duration > 7:
                self.error.setText("You cannot auction this item for greater than a week")
                return False
        elif self.format.currentText() == "Buy Now":
            if durationunits == "Years" or (durationunits == "Months" and duration > 12):
                self.error.setText("You cannot list this item for greater than a year")
                return False
            elif durationunits == "Days" and duration > 365:
                self.error.setText("You cannot list this item for greater than a year")
                return False
        return True

    def characterlimit(self,fieldname,limit):
        self.error.setText("The "+fieldname+" cannot exceed "+limit+" characters") 
        return

    def createwindow(self):
        selectoptions = [self.category.currentText()] * 6
        selectoptions[2] = self.condition.currentText()
        selectoptions[3] = self.format.currentText()
        selectoptions[4] = self.durationunits.currentText()
        selectoptions[5] = self.deliveryoption.currentText()

        selectfields = [self.durationfield.text(), self.title.text(), self.itemdesc.text(), self.quantityfield.text()]

        if len(self.itemdesc.text()) >= 400:
            self.characterlimit("description", "400")

        if len(self.title.text()) >= 30:
            self.characterlimit("title", "30")

        if (self.acceptconditions() and self.checkprice(self.pricefield.text()) and
                self.checkduration(self.durationfield.text()) and self.selectoption(selectoptions) and
                self.emptyfield(selectfields) and self.durationlimit(self.durationunits.currentText(), self.duration)):

            conn = sqlite3.connect("auc_database.db", isolation_level=None)
            cur = conn.cursor()

            locale.setlocale(locale.LC_ALL, 'en_GB.UTF-8')
            price_formatted = locale.currency(self.price, grouping=True)

            data = (self.title.text(), self.itemdesc.text(), self.category.currentText(),
                    self.condition.currentText(), self.format.currentText(), self.end_date, price_formatted,
                    self.deliveryoption.currentText(), self.itemquantity, True, self.userID)

            cur.execute('''
                INSERT INTO listings
                (title, description, category, condition, format, dateofend, price, delivery, quantity, active, sellerID)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', data)
            listingID = cur.lastrowid

            # if (self.couponfield.text() != "No Coupon (Current)") or (self.couponfield.text() != ""):
            #     coupon = str(self.couponfield.text())
            #     cur.execute('''
            #                 INSERT INTO coupons
            #                 (coupontag,quantity,usability,active)
            #                 VALUES (?,?,?,1)
            #                 ''',(coupon,self.itemquantity,listingID))

            coupon_text = self.couponfield.text()
            if coupon_text not in {"No Coupon (Current)", ""}:
                coupon = str(coupon_text)
                data = [(coupon, self.itemquantity, listingID)]
                cur.executemany('''
                    INSERT INTO coupons 
                    (coupontag,quantity,usability,active)
                    VALUES (?,?,?,1)
                    ''', data)

            conn.close()

            if self.admin:
                self.close()
                self.app.callAdminWindow(self.userID)
            else:
                self.close()
                self.app.callMainWindow(self.userID)
