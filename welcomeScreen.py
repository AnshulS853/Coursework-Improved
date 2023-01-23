from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog

class WelcomeScreen(QDialog):
    def __init__(self,app):
        # Constructor function for the welcome screen
        super(WelcomeScreen, self).__init__()
        loadUi("welcomescreen.ui", self)
        # connecting buttons to functions when clicked
        self.app = app
        self.login.clicked.connect(self.gotologin)
        self.create.clicked.connect(self.gotocreate)

    def gotologin(self):
        self.close()
        self.app.callLoginScreen()

    def gotocreate(self):
        self.close()
        self.app.callCreateScreen()


