from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog,QTableWidgetItem

import sqlite3
import locale

class couponCreation(QDialog):
    def __init__(self, app, uid ,admin):
        super(couponCreation, self).__init__()
        loadUi("createcoupon.ui", self)
        self.app = app
        self.userID = uid
        self.admin = admin

        self.conn = sqlite3.connect("auc_database.db",isolation_level=None)
        self.cur = self.conn.cursor()

        self.goback.clicked.connect(self.gobackpage)
        self.activatecoupon.clicked.connect(self.activateCoupon)


    def gobackpage(self):
        self.close()
        if self.admin:
            self.app.callAdminWindow(self.userID)
        else:
            self.app.callMainWindow(self.userID)

    # def activateCoupon(self):
    #     if (self.couponfield.text()!="") or (self.quantityfield.text()!=""):
    #         try:
    #             int(self.quantityfield.text())
    #             self.cur.execute('''
    #                             INSERT INTO coupons
    #                             (coupontag,
    #                             quantity,
    #                             usability,
    #                             active)
    #                             VALUES (?,?,'All',1)
    #                             ''',(str(self.couponfield.text()),int(self.quantityfield.text())))
    #
    #             self.close()
    #             if self.admin:
    #                 self.app.callAdminWindow(self.userID)
    #             else:
    #                 self.app.callMainWindow(self.userID)
    #         except:
    #             self.error.setText("Enter valid data into fields")
    #     else:
    #         self.error.setText("Enter valid data into fields")

    def activateCoupon(self):
        coupon_text = self.couponfield.text()
        quantity_text = self.quantityfield.text()
        discount_text = self.discountfield.text()

        if not coupon_text or not quantity_text or not discount_text:
            self.error.setText("Please fill in all fields")
            return

        try:
            quantity = int(quantity_text)
            discount = float(discount_text)
            if (discount <= 0) or (quantity<=0):
                return

            self.cur.execute('''
                            INSERT INTO coupons
                            (coupontag,
                            quantity,
                            usability,
                            discount,
                            userID,
                            active)
                            VALUES (?,?,'User',?,?,1)
                            ''',(coupon_text,quantity,discount,self.userID))

            self.close()
            if self.admin:
                self.app.callAdminWindow(self.userID)
            else:
                self.app.callMainWindow(self.userID)

        except Exception:
            self.error.setText("Enter valid data into fields")