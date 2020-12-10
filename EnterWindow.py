# -*- coding: utf-8 -*-
from PyQt4 import QtCore
from PyQt4.QtGui import *
from ForgotPassword import ForgotPassword
from Registration import Registration
from MainWindow import MainWindow
import hashlib
import sys

class EnterWindow(QWidget):
    def __init__(self, DBconnection):
        super(EnterWindow, self).__init__()
        self.DBconnection = DBconnection
        self._initUI()
        if not self._RememberEnter():
            self.show()

    def _initUI(self):
        self.mainVerticalLayout = QVBoxLayout(self)
        self.login_line = QLineEdit(self)
        self.mainVerticalLayout.addWidget(self.login_line)
        self.password_line = QLineEdit(self)
        self.password_line.setEchoMode(QLineEdit.Password)
        self.mainVerticalLayout.addWidget(self.password_line)
        horizontalLayout = QHBoxLayout(self)
        self.enter_button = QPushButton(self)
        self.enter_button.setStyleSheet('QPushButton {background-color: green; color: white;}')
        self.enter_button.clicked.connect(self._Enter)
        horizontalLayout.addWidget(self.enter_button)
        self.registration_button = QPushButton(self)
        self.registration_button.clicked.connect(self._ShowRegistrationWindow)
        horizontalLayout.addWidget(self.registration_button)
        self.cancel_button = QPushButton(self)
        self.cancel_button.clicked.connect(self.close)
        self.cancel_button.setStyleSheet('QPushButton {background-color: red; color: white;}')
        horizontalLayout.addWidget(self.cancel_button)
        self.mainVerticalLayout.addLayout(horizontalLayout)
        self.remember_checkbox = QCheckBox(self)
        self.mainVerticalLayout.addWidget(self.remember_checkbox)
        self.show_password_checkbox = QCheckBox(self)
        self.show_password_checkbox.clicked.connect(self._ShowPassword)
        self.mainVerticalLayout.addWidget(self.show_password_checkbox)
        self.forgot_password_button = QPushButton(self)
        self.forgot_password_button.setFlat(True)
        self.mainVerticalLayout.addWidget(self.forgot_password_button)
        font = QFont()
        font.setUnderline(True)
        self.forgot_password_button.setFont(font)
        self.forgot_password_button.setStyleSheet("color: rgb(0, 0, 255)")
        self.forgot_password_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.forgot_password_button.clicked.connect(self._ShowForgotPasswordWindow)
        self.login_line.setPlaceholderText(u"Имя пользователя")
        self.password_line.setPlaceholderText(u"Пароль")
        self.enter_button.setText(u"Войти")
        self.registration_button.setText(u"Регистрация")
        self.cancel_button.setText(u"Отмена")
        self.remember_checkbox.setText(u"Запомнить меня")
        self.show_password_checkbox.setText(u"Показать пароль")
        self.forgot_password_button.setText(u"Забыли пароль?")

    def _ShowForgotPasswordWindow(self):
        self.hide()
        self.ForgotPassword = ForgotPassword(self)
        self.ForgotPassword.show()

    def _ShowRegistrationWindow(self):
        self.hide()
        self.Registration = Registration(self, self.DBconnection)
        self.Registration.show()

    def _ShowPassword(self, checked):
        if checked:
            self.password_line.setEchoMode(QLineEdit.Normal)
        else:
            self.password_line.setEchoMode(QLineEdit.Password)

    def RememberLogin(self, login_id, checked):
        try:
            cursor = self.DBconnection.cursor()
            cursor.execute(u"update logins set remembered = {} where id = {}".format(checked, login_id))
            cursor.close()
            self.DBconnection.commit()
        except Exception as e:
            print("Error while execute query:", e)
            sys.exit(1)

    def _RememberEnter(self):
        try:
            cursor = self.DBconnection.cursor()
            cursor.execute("select id, login from logins where remembered = TRUE")
            login = cursor.fetchall()
            cursor.close()
        except Exception as e:
            print("Error while execute query:", e)
            sys.exit(1)
        if len(login):
            self.hide()
            self.mainWindow = MainWindow(self, login[0][1], login[0][0], self.DBconnection)
            self.mainWindow.show()
            return True
        else:
            return False

    def _Enter(self):
        login = self.login_line.text()
        password = self.password_line.text()
        remember = self.remember_checkbox.isChecked()
        if (not login) or (not password):
            msg = QMessageBox.information(self, u'Внимание!', u'Вы не заполнили все поля.')
            return
        password_hash = hashlib.md5(password.toLocal8Bit()).hexdigest()
        try:
            cursor = self.DBconnection.cursor()
            cursor.execute(u"select id from logins where login = '{}' and password_hash = '{}'".format(
                login, password_hash))
            login_id = cursor.fetchall()
            cursor.close()
        except Exception as e:
            print("Error while execute query:", e)
            sys.exit(1)
        if len(login_id):
            self.RememberLogin(login_id[0][0], remember)
            self.hide()
            self.mainWindow = MainWindow(self, login, login_id[0][0], self.DBconnection)
            self.mainWindow.show()
        else:
            msg = QMessageBox.information(self, u'Внимание!', u'Неправильное имя пользователя или пароль.')
            self.login_line.setText('')
            self.password_line.setText('')
