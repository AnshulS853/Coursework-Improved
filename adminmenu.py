# from PyQt5.uic import loadUi
# from PyQt5.QtWidgets import QDialog
#
# from datetime import datetime
# import sqlite3
#
# # class adminmenu(QDialog):
# #     def __init__(self,app,uid: object):
# #         super(adminmenu, self).__init__()
# #         loadUi("adminmenu.ui",self)
# #         self.app = app
# #         self.userID = uid
# #         self.now = datetime.now().hour
# #         self.admin = True
# #         self.welcometoast()
# #
# #         self.gotocreate.clicked.connect(self.createlisting)
# #         self.gotoview.clicked.connect(self.viewlistings)
# #         self.gotoupdateacc.clicked.connect(self.updateaccount)
# #         self.gotoinvoices.clicked.connect(self.myinvoices)
# #         self.manageaccounts.clicked.connect(self.manageaccs)
# #         self.managelistings.clicked.connect(self.managelists)
# #
# #     def welcometoast(self):
# #         conn = sqlite3.connect("auc_database.db")
# #         cur = conn.cursor()
# #         cur.execute('SELECT firstname FROM users WHERE userID=?', (self.userID,))
# #         firstname = cur.fetchall()
# #
# #         if 5 <= self.now <= 11:
# #             self.greetuser.setText("Good Morning "+str((firstname)[0][0])+" :)")
# #         elif 12 <= self.now <= 17:
# #             self.greetuser.setText("Good Afternoon "+str((firstname)[0][0])+" :)")
# #         else:
# #             self.greetuser.setText("Good Evening "+str((firstname)[0][0])+" :)")
#
# class adminmenu(QDialog):
#     def __init__(self, app, uid):
#         super(adminmenu, self).__init__()
#         loadUi("adminmenu.ui", self)
#         self.app = app
#         self.userID = uid
#         self.now = datetime.now().hour
#         self.admin = True
#         self.conn = sqlite3.connect("auc_database.db")
#         self.current_time = datetime.now()
#
#         self.welcometoast()
#
#         self.gotocreate.clicked.connect(self.createlisting)
#         self.gotoview.clicked.connect(self.viewlistings)
#         self.gotoupdateacc.clicked.connect(self.updateaccount)
#         self.gotoinvoices.clicked.connect(self.myinvoices)
#         self.manageaccounts.clicked.connect(self.manageaccs)
#         self.managelistings.clicked.connect(self.managelists)
#
#     def welcometoast(self):
#         cur = self.conn.cursor()
#         cur.execute('SELECT firstname FROM users WHERE userID=?', (self.userID,))
#         firstname = cur.fetchone()[0]
#
#         if 5 <= self.current_time.hour <= 11:
#             self.greetuser.setText("Good Morning " + firstname + " :)")
#         elif 12 <= self.current_time.hour <= 17:
#             self.greetuser.setText("Good Afternoon " + firstname + " :)")
#         else:
#             self.greetuser.setText("Good Evening " + firstname + " :)")
#
#     def createlisting(self):
#         self.close()
#         self.app.callCreationWindow(self.admin)
#
#     def updateaccount(self):
#         self.close()
#         check = True
#         self.app.callProfileScreen(self.userID,check,self.admin)
#
#     def viewlistings(self):
#         self.close()
#         self.app.callViewListings(self.userID,self.admin)
#
#     def myinvoices(self):
#         self.close()
#         self.app.callFindInvoices(self.userID,self.admin)
#
#     def manageaccs(self):
#         self.close()
#         self.app.callManageAccs()
#
#     def managelists(self):
#         self.close()
#         self.app.callManageListings()


from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog
import sqlite3
from datetime import datetime

class adminmenu(QDialog):
    def __init__(self, app: object, uid: int):
        super().__init__()
        loadUi("adminmenu.ui", self)
        self.app = app
        self.userID = uid
        self.admin = True
        self.welcometoast()

        self.gotobasket.clicked.connect(lambda: self.view_basket())
        self.gotocreate.clicked.connect(lambda: self.create_listing())
        self.gotoview.clicked.connect(lambda: self.view_listings())
        self.gotoupdateacc.clicked.connect(lambda: self.update_account())
        self.gotoinvoices.clicked.connect(lambda: self.find_invoices())
        self.manageaccounts.clicked.connect(lambda: self.manageaccs())
        self.managelistings.clicked.connect(lambda: self.managelists())
        self.gotocoupon.clicked.connect(lambda: self.create_coupon())

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

    def view_basket(self):
        self.close()
        self.app.callViewBasket(self.userID,self.admin)

    def create_listing(self):
        self.close()
        self.app.callCreationWindow(self.admin)

    def view_listings(self):
        self.close()
        self.app.callViewListings(self.userID,self.admin)

    def update_account(self):
        self.close()
        self.app.callProfileScreen(self.userID, True, self.admin)

    def find_invoices(self):
        self.close()
        self.app.callFindInvoices(self.userID,self.admin)

    def manageaccs(self):
        self.close()
        self.app.callManageAccs()

    def managelists(self):
        self.close()
        self.app.callManageListings()

    def create_coupon(self):
        self.close()
        self.app.callCouponCreation(self.userID,self.admin)