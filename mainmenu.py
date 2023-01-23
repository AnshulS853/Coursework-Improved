from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog

from datetime import datetime
import sqlite3

class mainmenu(QDialog):
    def __init__(self,app,uid: object):
        super(mainmenu, self).__init__()
        loadUi("menu.ui",self)
        self.app = app
        self.userID = uid
        self.now = datetime.now().hour
        self.welcometoast()

        self.gotocreate.clicked.connect(self.createlisting)
        self.gotoview.clicked.connect(self.viewlistings)
        self.gotoupdateacc.clicked.connect(self.updateaccount)
        self.gotoinvoices.clicked.connect(self.myinvoices)

    def welcometoast(self):
        conn = sqlite3.connect("auc_database.db")
        cur = conn.cursor()
        cur.execute('SELECT firstname FROM users WHERE userID=?', (self.userID,))
        firstname = cur.fetchall()

        if 5 <= self.now <= 11:
            self.greetuser.setText("Good Morning "+str((firstname)[0][0])+" :)")
        elif 12 <= self.now <= 17:
            self.greetuser.setText("Good Afternoon "+str((firstname)[0][0])+" :)")
        else:
            self.greetuser.setText("Good Evening "+str((firstname)[0][0])+" :)")

    def createlisting(self):
        self.close()
        self.app.callCreationWindow()

    def viewlistings(self):
        self.close()
        self.app.callViewListings(self.userID)

    def updateaccount(self):
        self.close()
        check = True
        self.app.callProfileScreen(self.userID,check)

    def myinvoices(self):
        self.close()
        self.app.callFindInvoices(self.userID)


