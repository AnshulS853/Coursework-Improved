from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog
import sqlite3
from datetime import datetime

class mainmenu(QDialog):
    def __init__(self, app: object, uid: int):
        super().__init__()
        loadUi("menu.ui", self)
        self.app = app
        self.userID = uid
        self.welcometoast()

        self.gotocreate.clicked.connect(lambda: self.create_listing())
        self.gotoview.clicked.connect(lambda: self.view_listings())
        self.gotoupdateacc.clicked.connect(lambda: self.update_account())
        self.gotoinvoices.clicked.connect(lambda: self.find_invoices())

    def get_cursor(self):
        conn = sqlite3.connect("auc_database.db")
        cur = conn.cursor()
        return conn, cur

    def welcometoast(self):
        now = datetime.now().hour
        conn, cur = self.get_cursor()
        cur.execute('SELECT firstname FROM users WHERE userID=?', (self.userID,))
        firstname = cur.fetchone()[0]
        conn.close()

        if 5 <= now <= 11:
            self.greetuser.setText(f"Good Morning {firstname} :)")
        elif 12 <= now <= 17:
            self.greetuser.setText(f"Good Afternoon {firstname} :)")
        else:
            self.greetuser.setText(f"Good Evening {firstname} :)")

    def create_listing(self):
        self.close()
        self.app.callCreationWindow()

    def view_listings(self):
        self.close()
        self.app.callViewListings(self.userID)

    def update_account(self):
        self.close()
        self.app.callProfileScreen(self.userID, True)

    def find_invoices(self):
        self.close()
        self.app.callFindInvoices(self.userID)