from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog

import sqlite3
import re

from databasefunction import databaseClass


class FillAddress(QDialog):
    def __init__(self, app, uid, check, admin):
        super(FillAddress, self).__init__()
        loadUi("address.ui", self)
        self.app = app
        self.userID = uid
        self.checkupdate = check
        self.checkadmin = admin
        self.showbuttons()

        self.addsignup.clicked.connect(self.saveaddress)
        self.goback.clicked.connect(self.gobackwindow)
        self.skiptomenu.clicked.connect(self.goskip)

    def showbuttons(self):
        if not self.checkupdate:
            self.goback.setText("")
            self.skiptomenu.setText("")

    def gobackwindow(self):
        if self.checkupdate:
            self.close()
            self.app.callProfileScreen(self.userID, self.checkupdate, self.checkadmin)

    def goskip(self):
        if self.checkupdate:
            if self.checkadmin:
                self.close()
                self.app.callAdminWindow(self.userID, self.checkadmin)
            else:
                self.close()
                self.app.callMainWindow(self.userID, self.checkadmin)

    def validate_postcode(self, pc):
        pc = pc.replace(" ", "")  # remove spaces
        if len(pc) == 0:
            self.postcodeerror.setText("Please enter a postcode")
            return False

        pattern = re.compile(r"^[A-Z]{1,2}\d{1,2}[A-Z]{0,2}\d[A-Z]{2}$")
        if not pattern.match(pc):
            self.postcodeerror.setText("This is an invalid UK postcode")
            return False

        return True

    def saveaddress(self):
        postcode = self.postcode.text()
        if not self.validate_postcode(postcode):
            return

        user_address = (
            self.houseno.text(),
            self.addressfield1.text(),
            self.addressfield2.text(),
            postcode,
            self.county.text()
        )

        with sqlite3.connect("auc_database.db", isolation_level=None) as conn:
            cur = conn.cursor()

            cur.execute(
                'SELECT addressID FROM address WHERE houseno=? AND postcode=?',
                (user_address[0], user_address[3])
            )
            result = cur.fetchone()
            if result:
                self.addressID = result[0]
            else:
                x = databaseClass(self.userID)
                self.addressID = x.insertaddress(user_address)

            if not self.checkupdate:
                cur.execute(
                    'INSERT INTO usad (userID,addressID) VALUES (?,?)',
                    (self.userID, self.addressID)
                )
            else:
                cur.execute(
                    'UPDATE usad SET addressID = ? WHERE userID = ?',
                    (self.addressID, self.userID)
                )

            try:
                cur.execute('SELECT admin FROM users WHERE userID=?', (self.userID,))
                admin = cur.fetchone()[0]
                if admin:
                    self.close()
                    self.app.callAdminWindow(self.userID, admin)
                else:
                    self.close()
                    self.app.callMainWindow(self.userID, admin)
            except Exception as e:
                print(f"Error: {e}")
            finally:
                cur.close()