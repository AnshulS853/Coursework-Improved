from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog

import sqlite3
import re

from databasefunction import databaseClass

class FillAddress(QDialog):
    def __init__(self,app,uid,check,admin):
        super(FillAddress, self).__init__()
        loadUi("address.ui",self)
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
            self.app.callProfileScreen(self.userID,self.checkupdate,self.checkadmin)

    def goskip(self):
        if self.checkupdate and self.checkadmin:
            self.close()
            self.app.callAdminWindow(self.userID,self.checkadmin)
        elif self.checkupdate:
            self.close()
            self.app.callMainWindow(self.userID,self.checkadmin)

    def validate_postcode(self,pc):
        if pc.isspace() == True:
            self.postcodeerror.setText("Please remove the space from the postcode")
            return
        else:
            pattern = 'not matched'
            # e.g. W27XX
            if len(pc.replace(" ", "")) == 5:
                pattern = re.compile("^[a-zA-Z]{1}[0-9]{2}[a-zA-Z]{2}")
            # e.g. TW27XX
            elif len(pc.replace(" ", "")) == 6:
                pattern = re.compile("^[a-zA-Z]{2}[0-9]{2}[a-zA-Z]{2}")
            # e.g. TW218FF
            elif len(pc.replace(" ", "")) == 7:
                pattern = re.compile("^[a-zA-Z]{2}[0-9]{3}[a-zA-Z]{2}")

            if pattern == 'not matched':
                self.postcodeerror.setText("This is an invalid UK postcode")
                return
            else:
                if pattern.match(pc):
                    return True

    def saveaddress(self):
        if self.validate_postcode(str(self.postcode.text())) is not True:
            return
        else:
            user_address = (self.houseno.text(),
                            self.addressfield1.text(),
                            self.addressfield2.text(),
                            self.postcode.text(),
                            self.county.text())

            # user_address = {"afieldone": self.addressfield1.text(),
            #              "afieldtwo": self.addressfield2.text(),
            #              "postcode": int(self.postcode.text()),
            #              "county": self.county.text()}

            conn = sqlite3.connect("auc_database.db",isolation_level=None)
            # connecting to the database
            cur = conn.cursor()

            # cur.execute('SELECT COUNT(postcode) FROM address WHERE postode=?',(user_address[3]))
            # count = cur.fetchall()
            # if count[0][0] != 0:
            #     cur.execute('SELECT COUNT(addressfield1) FROM address WHERE addressfield1=?',(user_address[1]))
            #     count = cur.fetchall()
            #     if count[0][0] != 0:
            #         pass

            cur.execute('SELECT COUNT(postcode) FROM address WHERE postcode=?',(user_address[3],))
            countpostcode = cur.fetchall()
            cur.execute('SELECT COUNT(houseno) FROM address WHERE houseno=?',(user_address[0],))
            counthouseno = cur.fetchall()

            if countpostcode[0][0] != 0 and counthouseno[0][0] != 0:
                cur.execute('SELECT addressID FROM address where houseno=? AND postcode=?',(user_address[0],user_address[3]))
                self.addressID = cur.fetchall()
                self.addressID = self.addressID[0][0]
                # print(self.addressID)
            else:
                x = databaseClass(self.userID)
                self.addressID = x.insertaddress(user_address)
                # print(self.addressID)

            # cur.execute('UPDATE users SET addressID=? WHERE userID=?', (self.addressID, self.userID))
            if not self.checkupdate:
                cur.execute('INSERT INTO usad (userID,addressID) VALUES (?,?)',(self.userID,self.addressID))
            else:
                cur.execute('UPDATE usad SET addressID = ? WHERE userID = ?',(self.addressID,self.userID))

            cur.execute('SELECT admin FROM users WHERE userID=?', (self.userID,))
            admin = cur.fetchone()

            if admin[0] == True:
                self.close()
                self.app.callAdminWindow(self.userID,admin)
            else:
                 self.close()
                 self.app.callMainWindow(self.userID,admin)



