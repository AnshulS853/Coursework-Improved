from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog

import string
import sqlite3
import re

from datetime import date
from databasefunction import databaseClass

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


class FillProfileScreen(QDialog):
    def __init__(self, app, uid, cu, admin):
        super(FillProfileScreen, self).__init__()
        loadUi("fillprofile.ui", self)
        self.app = app
        self.checkupdate = cu
        self.userID = uid
        self.admin = admin

        self.updatetoast()
        self.showbuttons()

        self.skiptoadd.clicked.connect(self.skiptoaddress)
        self.signupcontinue.clicked.connect(self.saveprofile)
        self.goback.clicked.connect(self.gobackwindow)

    def showbuttons(self):
        if not self.checkupdate:
            self.goback.setText("")
            self.skiptoadd.setText("")

    def gobackwindow(self):
        if self.checkupdate:
            if self.admin:
                self.close()
                self.app.callAdminWindow(self.userID)
            else:
                self.close()
                self.app.callMainWindow(self.userID)
        else:
            self.filltoast.setText("You cannot go back until fields are filled!")

    def skiptoaddress(self):
        if self.checkupdate:
            self.close()
            self.app.callAddressScreen()

    def updatetoast(self):
        if self.checkupdate:
            self.filltoast.setText("Update your account details")

    def checknumeric(self, s):
        return any(i.isdigit() for i in s)

    def calculate_age(self, dateofb):
        today = date.today()
        try:
            birthday = dateofb.replace(year=today.year)
        except ValueError:  # raised when birth date is February 29 and the current year is not a leap year
            birthday = dateofb.replace(year=today.year, month=dateofb.month + 1, day=1)
        if birthday > today:
            return today.year - dateofb.year - 1
        else:
            return today.year - dateofb.year

    def validateuser(self):
        if len(self.firstname) > 12 or self.checknumeric(self.firstname) == True:
            self.firstnameerror.setText("Your firstname must be less than 12 characters and cannot be alphanumeric")
            return

        if len(self.firstname) == 0:
            self.firstnameerror.setText("This field cannot be empty")
            return

        if len(self.lastname) == 0:
            self.lastnameerror.setText("This field cannot be empty")
            return

        if len(self.lastname) > 12 or self.checknumeric(self.lastname) == True:
            self.firstnameerror.setText("Your lastname must be less than 12 characters and cannot be alphanumeric")
            return

    def validate_email(self,email):
        if (re.search(regex, email)):
            pass
        else:
            self.emailerror.setText("Invalid email format")
            return

    def checkemailexists(self,email):
        conn = sqlite3.connect("auc_database.db")
        cur = conn.cursor()
        cur.execute('SELECT COUNT(email) FROM users WHERE email=?', (email,))
        count = cur.fetchall()
        conn.close()
        if count[0][0] != 0:
            self.emailerror.setText("email already exists")
            return

    def checkuserage(self,dob):
        user_age = self.calculate_age(dob)
        if user_age <= 13:
            self.doberror.setText("You have to be over 13 to create an account")
            return
        else:
            return True

    def saveprofile(self):
        self.firstname = string.capwords(self.firstname.text())
        self.lastname = string.capwords(self.lastname.text())

        gender = str(self.gender.currentText())


        if gender == "Male":
            gender = 0
        else:
            gender = 1

        # user_info = {"firstname":self.firstname.text(),
        #              "lastname":self.lastname.text(),
        #              "email":self.email.text(),
        #              "dob":self.dob.date().toPyDate(),
        #              "gender":gender}
        self.validateuser()

        email = self.email.text()

        self.validate_email(email)

        # filladdress = FillAddress()
        # widget = QtWidgets.QStackedWidget()
        # widget.addWidget(filladdress)
        # widget.setCurrentIndex(widget.currentIndex() + 1)

        dob = self.dob.date().toPyDate()
        if self.checkuserage(dob) is True:
            user_info = (self.firstname,
                         self.lastname,
                         email,
                         dob,
                         int(gender))

            x = databaseClass(self.userID)
            x.insertuserinfo(user_info)

            self.close()
            self.app.callAddressScreen()
        else:
            return
