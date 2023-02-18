from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog

import sqlite3
import hashlib
import re
import os

class CreateAccScreen(QDialog):
    def __init__(self,app):
        super(CreateAccScreen, self).__init__()
        loadUi("createacc.ui",self)
        # Hides the password when typing into the field
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpasswordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signup.clicked.connect(self.signupfunction)
        self.goback.clicked.connect(self.backtowelcome)
        self.app = app
        self.userID = 0
    def validatepass(self,password):
        if len(password) < 8:
            self.error.setText("Make sure your password is at least 8 letters")
            return False

        if re.search('[0-9]', password) is None:
            self.error.setText("Make sure your password has a number in it")
            return False

        if re.search('[A-Z]', password) is None:
            self.error.setText("Make sure your password has a capital letter in it")
            return False

        return True

    def backtowelcome(self):
        self.close()
        self.app.callWelcomeScreen()

    def signupfunction(self):
        username = self.usernamefield.text()
        password = self.passwordfield.text()

        if not self.validatepass(password):
            return

        confirmpassword = self.confirmpasswordfield.text()

        if not all([username, password, confirmpassword]):
            self.error.setText("Please fill in all inputs.")
            return

        if password != confirmpassword:
            self.error.setText("Passwords do not match.")
            return

        conn = sqlite3.connect("auc_database.db")
        cur = conn.cursor()
        cur.execute('SELECT COUNT(username) FROM users WHERE username=?', (username,))
        count = cur.fetchone()[0]

        if count != 0:
            self.error.setText("Username already exists")
            conn.close()
            return

        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

        user_info = (username, key, salt)

        cur.execute('''INSERT INTO users (admin, username, password, salt)
                        VALUES (0,?,?,?)''', user_info)

        cur.execute('SELECT userID FROM users WHERE username=?', (username,))
        userID = cur.fetchone()[0]
        conn.commit()
        conn.close()

        self.close()
        self.app.callProfileScreen(userID)
