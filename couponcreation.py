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

        self.goback.clicked.connect(self.gobackpage)

    def gobackpage(self):
        if self.admin:
            self.close()
            self.app.callAdminWindow(self.userID)
        else:
            self.close()
            self.app.callMainWindow(self.userID)
