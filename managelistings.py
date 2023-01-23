from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QTableWidgetItem

import sqlite3
from datetime import datetime, timedelta

class manageListings(QDialog):
    def __init__(self,app,uid):
        super(manageListings, self).__init__()
        loadUi("managelists.ui", self)
        self.confirmtoast.setText("")
        self.app = app
        self.userID = uid
        self.currentListingID = None
        self.mode = None
        self.activev = None

        self.conn = sqlite3.connect("auc_database.db",isolation_level=None)
        self.cur = self.conn.cursor()

        self.deletelist.clicked.connect(self.deletelisting)
        self.setactive.clicked.connect(self.makelistingactive)
        self.setinactive.clicked.connect(self.makelistinginactive)
        self.goback.clicked.connect(self.gotoadmenu)
        self.loadTable()

    def gotoadmenu(self):
        self.close()
        self.app.callAdminWindow(self.userID)

    def fetchlistingID(self):
        try:
            row = self.listingstable.currentRow()
            self.currentListingID = int(self.listingstable.item(row, 0).text())
            # print(self.currentUserID)
        except:
            self.confirmtoast.setText("Select a \nRecord")

    def deletelisting(self):
        self.mode = "Delete"
        self.fetchlistingID()
        self.confirmtoast.setText("Deleting \n listingID: " + str(self.currentListingID))
        self.confirmchoice.clicked.connect(self.deleterecord)

    def calcend_date(self,duration,durationunits):
        if durationunits == "Days":
            self.end_date = datetime.now().date() + timedelta(days=duration)
        elif durationunits == "Months":
            self.end_date = datetime.now().date() + timedelta(months=duration)
        elif durationunits == "Years":
            self.end_date = datetime.now().date() + timedelta(years=duration)

    def checkduration(self, duration):
        try:
            duration = int(duration)
            if duration < 1:
                return
            else:
                self.calcend_date(duration, self.durationunits.currentText())
                # print(self.end_date)
                return True
        except:
            self.confirmtoast.setText("Enter valid duration\n for listingID: " + str(self.currentListingID) + "\n to be Active")
            return

    def makelistingactive(self):
        self.mode = "ChangeList"
        self.fetchlistingID()
        self.confirmtoast.setText("Enter valid duration\n for listingID: " + str(self.currentListingID) + "\n to be Active")
        self.confirmchoice.clicked.connect(self.confirmactive)
    def confirmactive(self):
        if (self.checkduration(self.durationfield.text()))==True:
            self.activev = True
            self.cur.execute('UPDATE listings SET dateofend=? WHERE listingID=?', (self.end_date, self.currentListingID))
            self.updatelisting()

    def makelistinginactive(self):
        self.mode = "ChangeList"
        self.fetchlistingID()
        self.confirmtoast.setText("Making \n listingID: " + str(self.currentListingID) + "\nInactive")
        self.activev = False
        self.confirmchoice.clicked.connect(self.updatelisting)

    def loadTable(self):
        self.listingstable.setRowCount(0)

        self.cur.execute('SELECT listingID,title,category,format,dateofend,price,active FROM listings LIMIT 50')
        results = self.cur.fetchall()
        self.listingstable.setRowCount(50)

        for row_number, row_data in enumerate(results):
            self.listingstable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.listingstable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        header = self.listingstable.horizontalHeader()
        for i in range(7):
            header.setSectionResizeMode(i,QtWidgets.QHeaderView.Stretch)

    def deleterecord(self):
        if self.mode == "Delete":
            self.cur.execute('DELETE FROM listings WHERE listingID = ?', (self.currentListingID,))
            self.loadTable()

    def updatelisting(self):
        if self.mode == "ChangeList":
            self.cur.execute('UPDATE listings SET active=? WHERE listingID=?', (self.activev, self.currentListingID))
            self.loadTable()
