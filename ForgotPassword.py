# -*- coding: utf-8 -*-
from PyQt4 import QtCore
from PyQt4.QtGui import *

class ForgotPassword(QWidget):
    def __init__(self, previous_window):
        super(ForgotPassword, self).__init__()
        self.previousWindow = previous_window
        self._initUI()

    def _initUI(self):
        self.mainVerticalLayout = QVBoxLayout(self)
        self.email_line = QLineEdit(self)
        self.mainVerticalLayout.addWidget(self.email_line)
        horizontalLayout = QHBoxLayout(self)
        self.change_password_button = QPushButton(self)
        self.change_password_button.clicked.connect(self._ChangePassword)
        self.change_password_button.setStyleSheet('QPushButton {background-color: green; color: white;}')
        horizontalLayout.addWidget(self.change_password_button)
        self.cancel_button = QPushButton(self)
        horizontalLayout.addWidget(self.cancel_button)
        self.mainVerticalLayout.addLayout(horizontalLayout)
        self.email_line.setPlaceholderText(u"Адрес электронной почты")
        self.change_password_button.setText(u"Сменить пароль")
        self.cancel_button.setStyleSheet('QPushButton {background-color: red; color: white;}')
        self.cancel_button.clicked.connect(self._Close)
        self.cancel_button.setText(u"Отмена")

    def closeEvent(self, event):
        self._Close()

    def _ChangePassword(self):
        email = self.email_line.text()
        print(email)

    def _Close(self):
        self.close()
        self.previousWindow.show()
