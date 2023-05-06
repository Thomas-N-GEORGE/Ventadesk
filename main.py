"""Our program entry point."""

import typing
from PyQt6 import QtCore, uic
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QPushButton,
    QLineEdit,
    QTreeWidgetItem,
)

import os
import sys

from application import AppWindow
from api_connect import login


class MyWindow(QMainWindow):
    """Our main window class."""

    def __init__(self):
        """Initialize."""

        QMainWindow.__init__(self)
        self.label = QLabel(parent=self)
        self.btn_connect = QPushButton(parent=self)
        self.line_email = QLineEdit(parent=self)
        self.line_password = QLineEdit(parent=self)
        self.setup_ui()
        self.setup_links()

    def setup_ui(self):
        """Graphical setup."""

        self.setWindowTitle("Ventadesk")  # Window title
        self.setFixedSize(500, 350)
        
        self.label.setText("Bienvenue, employé(e)")
        self.label.adjustSize()

        self.line_email.move(0, 30)
        self.line_email.setPlaceholderText("Votre email")
        self.line_password.move(0, 60)
        self.line_password.setPlaceholderText("Votre MdP")
        
        self.btn_connect.move(0, 90)
        self.btn_connect.setText("Connexion")

    def setup_links(self):
        """Connecting links."""

        # self.btn_connect.clicked.connect(self.change_message)
        self.btn_connect.clicked.connect(self.login_api)

    def change_message(self):
        """Slot for btn clicked."""

        self.label.setText(f"Hi, {self.line_email.text()}, how are you ?")
        self.label.adjustSize()
        self.line_email.clear()
        self.line_password.clear()

    def greetings(self):
        """Greetings when logged in."""

        self.label.setText(f"Hi, {self.line_email.text()}, you are successfully connected !")
        self.label.adjustSize()
        self.line_email.clear()
        self.line_password.clear()

    def login_api(self):
        """Slot to login to API."""

        is_logged = login(email=self.line_email.text(), password=self.line_password.text())
        if is_logged:
            self.greetings()





def main():
    """Main application."""

    app = QApplication(sys.argv)  # App object
    # win = MyWindow()  # Window objec, to be able to halt program properly
    win = AppWindow()
    win.show()  # Show window
    app.exec()  # Run app


if __name__ == "__main__":
    main()
