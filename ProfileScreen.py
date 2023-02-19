# from PyQt5.uic import loadUi
# from PyQt5.QtWidgets import QDialog
#
# import string
# import sqlite3
# import re
#
# from datetime import date
#
# regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
#
# class FillProfileScreen(QDialog):
#     def __init__(self, app, uid, cu, admin):
#         super(FillProfileScreen, self).__init__()
#         loadUi("fillprofile.ui", self)
#         self.app = app
#         self.checkupdate = cu
#         self.userID = uid
#         self.admin = admin
#
#         self.updatetoast()
#         self.showbuttons()
#
#         self.skiptoadd.clicked.connect(self.skiptoaddress)
#         self.signupcontinue.clicked.connect(self.saveprofile)
#         self.goback.clicked.connect(self.gobackwindow)
#
#     def showbuttons(self):
#         if not self.checkupdate:
#             self.goback.setText("")
#             self.skiptoadd.setText("")
#
#     def gobackwindow(self):
#         if self.checkupdate:
#             if self.admin:
#                 self.close()
#                 self.app.callAdminWindow(self.userID)
#             else:
#                 self.close()
#                 self.app.callMainWindow(self.userID)
#         else:
#             self.filltoast.setText("You cannot go back until fields are filled!")
#
#     def skiptoaddress(self):
#         if self.checkupdate:
#             self.close()
#             self.app.callAddressScreen()
#
#     def updatetoast(self):
#         if self.checkupdate:
#             self.filltoast.setText("Update your account details")
#
#     def checknumeric(self, s):
#         return any(i.isdigit() for i in s)
#
#     def calculate_age(self, dateofb):
#         today = date.today()
#         try:
#             birthday = dateofb.replace(year=today.year)
#         except ValueError:  # raised when birth date is February 29 and the current year is not a leap year
#             birthday = dateofb.replace(year=today.year, month=dateofb.month + 1, day=1)
#         if birthday > today:
#             return today.year - dateofb.year - 1
#         else:
#             return today.year - dateofb.year
#
#     def validateuser(self):
#         if len(self.firstname) > 12 or self.checknumeric(self.firstname) == True:
#             self.firstnameerror.setText("Your firstname must be less than 12 characters and cannot be alphanumeric")
#             return
#
#         if len(self.firstname) == 0:
#             self.firstnameerror.setText("This field cannot be empty")
#             return
#
#         if len(self.lastname) == 0:
#             self.lastnameerror.setText("This field cannot be empty")
#             return
#
#         if len(self.lastname) > 12 or self.checknumeric(self.lastname) == True:
#             self.lastnameerror.setText("Your lastname must be less than 12 characters and cannot be alphanumeric")
#             return
#
#     def validate_email(self,email):
#         if (re.search(regex, email)):
#             pass
#         else:
#             self.emailerror.setText("Invalid email format")
#             return
#
#     def checkemailexists(self,email):
#         conn = sqlite3.connect("auc_database.db")
#         cur = conn.cursor()
#         cur.execute('SELECT COUNT(email) FROM users WHERE email=?', (email,))
#         count = cur.fetchall()
#         conn.close()
#         if count[0][0] != 0:
#             self.emailerror.setText("email already exists")
#             return
#
#     def checkuserage(self,dob):
#         user_age = self.calculate_age(dob)
#         if user_age <= 13:
#             self.doberror.setText("You have to be over 13 to create an account")
#             return
#         else:
#             return True
#
#     def saveprofile(self):
#         self.firstname = string.capwords(self.firstname.text())
#         self.lastname = string.capwords(self.lastname.text())
#
#         gender = str(self.gender.currentText())
#
#
#         if gender == "Male":
#             gender = 0
#         else:
#             gender = 1
#
#         # user_info = {"firstname":self.firstname.text(),
#         #              "lastname":self.lastname.text(),
#         #              "email":self.email.text(),
#         #              "dob":self.dob.date().toPyDate(),
#         #              "gender":gender}
#         self.validateuser()
#
#         email = self.email.text()
#
#         self.validate_email(email)
#
#         # filladdress = FillAddress()
#         # widget = QtWidgets.QStackedWidget()
#         # widget.addWidget(filladdress)
#         # widget.setCurrentIndex(widget.currentIndex() + 1)
#
#         dob = self.dob.date().toPyDate()
#
#         if self.checkuserage(dob):
#
#             conn = sqlite3.connect("auc_database.db", isolation_level=None)
#             cur = conn.cursor()
#             cur.execute('''
#                 UPDATE users
#                 SET firstname=?,
#                 lastname=?,
#                 email=?,
#                 dob=?,
#                 gender=?
#                 WHERE userID = (?)
#             ''',(self.firstname,
#                 self.lastname,
#                 email,
#                 dob,
#                 int(gender),
#                 self.userID
#                 ))
#             conn.close()
#
#             self.close()
#             self.app.callAddressScreen()
#         else:
#             return

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog

import string
import sqlite3
import re

from datetime import date

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
        if not self.checkupdate:
            self.filltoast.setText("You cannot go back until fields are filled!")
            return

        if self.admin:
            self.close()
            self.app.callAdminWindow(self.userID)
        else:
            self.close()
            self.app.callMainWindow(self.userID)

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
        name_pattern = r'^[a-zA-Z\s]{1,12}$'
        if not re.match(name_pattern, self.firstname):
            self.firstnameerror.setText(
                "Your firstname must be less than 12 characters and cannot contain special characters")
            return

        if not re.match(name_pattern, self.lastname):
            self.lastnameerror.setText(
                "Your lastname must be less than 12 characters and cannot contain special characters")
            return

    def validate_email(self, email):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            self.emailerror.setText("Invalid email format")

    def checkemailexists(self, email):
        with sqlite3.connect("auc_database.db") as conn:
            cur = conn.cursor()
            cur.execute('SELECT COUNT(email) FROM users WHERE email=?', (email,))
            count = cur.fetchone()[0]
            if count != 0:
                self.emailerror.setText("Email already exists")
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
        self.validateuser()

        email = self.email.text()

        self.validate_email(email)

        dob = self.dob.date().toPyDate()

        if self.checkuserage(dob):
            with sqlite3.connect("auc_database.db") as conn:
                cur = conn.cursor()

                query = '''
                    UPDATE users
                    SET firstname=?,
                    lastname=?,
                    email=?,
                    dob=?,
                    gender=?
                    WHERE userID=?
                '''
                params = (self.firstname, self.lastname, email, dob, int(gender), self.userID)

                cur.execute(query, params)

                conn.commit()

            self.close()
            self.app.callAddressScreen()
        else:
            return
