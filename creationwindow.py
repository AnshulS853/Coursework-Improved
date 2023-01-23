from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog

from datetime import datetime, timedelta

from databasefunction import databaseClass
import locale


class creationScreen(QDialog):
    def __init__(self, app, uid, admin):
        super(creationScreen, self).__init__()
        loadUi("createlisting.ui", self)
        # connecting buttons to functions when clicked
        self.app = app
        self.userID = uid
        self.admin = admin
        self.goback.clicked.connect(self.gobacktomenu)
        self.continuepage.clicked.connect(self.createwindow)

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

    def calcend_date(self,duration,durationunits):
        if durationunits == "Days":
            self.end_date = datetime.now().date() + timedelta(days=duration)
        elif durationunits == "Months":
            self.end_date = datetime.now().date() + timedelta(months=duration)
        elif durationunits == "Years":
            self.end_date = datetime.now().date() + timedelta(years=duration)

    def checkduration(self, duration):
        self.duration = duration
        try:
            self.duration = int(self.duration)
            if self.duration < 1:
                return
            else:
                self.calcend_date(self.duration, self.durationunits.currentText())
                # print(self.end_date.date())
                return True
        except:
            self.error.setText("Duration must be a positive integer")
            return

    def checkprice(self,price):
        self.price = price
        try:
            self.price = float(self.price)
            locale.setlocale(locale.LC_ALL, 'en_GB')
            self.price = locale.currency(self.price, grouping=True)
            # print(price)
            return True
        except:
            self.error.setText("Price must in a valid format")
            return

    def overperiod(self, format, period):
        self.error.setText("You cannot " + format + " for more than a " + period)
        return

    def acceptconditions(self):
        if self.acceptcondition.isChecked():
            return True
        else:
            self.error.setText("You must accept to the terms to use this service")
            return

    def durationlimit(self,durationunits,duration):
        if self.format.currentText() == "Auction":
            if (durationunits == "Days" and duration > 7) or (durationunits == "Months") or (durationunits == "Years"):
                self.overperiod("auction", "week")
                return
            else:
                return True

        elif self.format.currentText() == "Buy Now":
            if durationunits == "Days" and duration > 365:
                self.overperiod("list this item", "year")
                return
            elif durationunits == "Months" and duration > 12:
                self.overperiod("list this item", "year")
                return
            elif durationunits == "Years" and duration > 1:
                self.overperiod("list this item", "year")
                return
            else:
                return True

    def characterlimit(self,fieldname,limit):
        self.error.setText("The "+fieldname+" cannot exceed "+limit+" characters") 
        return

    def createwindow(self):
        selectoptions = [self.category.currentText(),self.category.currentText(),self.condition.currentText(),
                         self.format.currentText(),self.durationunits.currentText(),self.deliveryoption.currentText()]
        selectfields = [self.durationfield.text(),self.title.text(),self.itemdesc.text()]

        # self.selectoption(self.category.currentText())
        # self.selectoption(self.condition.currentText())
        # self.selectoption(self.format.currentText())
        # self.selectoption(self.durationunits.currentText())
        # self.selectoption(self.deliveryoption.currentText())

        # self.emptyfield(self.durationfield.text())
        # self.emptyfield(self.title.text())
        # self.emptyfield(self.itemdesc.text())

        if len(self.itemdesc.text()) >= 400:
            self.characterlimit("description","400")

        if len(self.title.text()) >= 30:
            self.characterlimit("title","30")

        if (self.acceptconditions() is True) and (self.checkprice(self.pricefield.text()) is True) and (
                self.checkduration(self.durationfield.text()) is True) and (self.selectoption(selectoptions) is True) and (
                self.emptyfield(selectfields) is True) and (self.durationlimit(self.durationunits.currentText(),self.duration) is True):

            listing_info = (self.title.text(),
                            self.itemdesc.text(),
                            self.category.currentText(),
                            self.condition.currentText(),
                            self.format.currentText(),
                            self.end_date,
                            self.price,
                            self.deliveryoption.currentText(),
                            True,
                            self.userID)
            #in order of title,description,category,condition,format,end date,price,delivery,Listing Active,sellerID

            print(listing_info)
            x = databaseClass(self.userID)
            x.insertlisting(listing_info)
            if self.admin:
                self.close()
                self.app.callAdminWindow(self.userID)
            else:
                self.close()
                self.app.callMainWindow(self.userID)

        # if duration < 0:
        #     self.error.setText("Duration cannot be negative")
        #     self.continuepage.clicked.connect(self.createwindow)
        # else:
        #     durationunits = self.durationunits.currentText()
        #     price = self.price.text()
        #
        #     if self.title.text() == "" or self.itemdesc.text() == "" or duration == "" or price == "":
        #         self.error.setText("Please fill in all fields")
        #         self.continuepage.clicked.connect(self.createwindow)
        #
        #     if self.format.currentText() == "Auction":
        #         if (durationunits == "Days" and duration > 7) or (durationunits == "Months") or (
        #                 durationunits == "Years"):
        #             self.overperiod("auction", "week")
        #
        #     elif self.format.currentText() == "Buy Now":
        #         if durationunits == "Days" and duration > 365:
        #             self.overperiod("list this item", "year")
        #         elif durationunits == "Months" and duration > 12:
        #             self.overperiod("list this item", "year")
        #         elif durationunits == "Years" and duration > 1:
        #             self.overperiod("list this item", "year")
        #
        #     if len(description) >= 1000:
        #         self.error.setText("Your description exceeds 1000 character limit")
        #         self.continuepage.clicked.connect(self.createwindow)
        #
        #     if durationunits == "Days":
        #         self.end_date = datetime.now() + timedelta(days=duration)
        #     elif durationunits == "Months":
        #         self.end_date = datetime.now() + timedelta(months=duration)
        #     elif durationunits == "Years":
        #         self.end_date = datetime.now() + timedelta(years=duration)
        #
        #     listing_info = (self.title.text(),
        #                     description,
        #                     self.category.currentText(),
        #                     self.condition.currentText(),
        #                     self.format.currentText(),
        #                     self.end_date,
        #                     price,
        #                     self.deliveryoption.currentText(),)
        #
        #     print(listing_info)
        #     # In order of (title,desc,category,format,dateofend,delivery)
        #
        #     x = databaseClass(self.userID)
        #     x.insertlisting(listing_info)
