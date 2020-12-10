# -*- coding: utf-8 -*-
from PyQt4 import QtCore
from PyQt4.QtGui import *
import sys
import hashlib

class CustomDateEdit(QDateEdit):
    def __init__(self, parent):
        super(CustomDateEdit, self).__init__(parent)
        self.setDisplayFormat("yyyy-MM-dd")
        self.isDataChanged = False
        self.dateChanged.connect(self._CH)

    def _CH(self):
        self.isDataChanged = True

    def paintEvent(self, event):
        if not self.isDataChanged:
            self.lineEdit().setText('')
            self.lineEdit().setPlaceholderText(u"Дата рождения")
        super(CustomDateEdit, self).paintEvent(event)

class Registration(QWidget):
    def __init__(self, previous_window, DBconnection):
        super(Registration, self).__init__()
        self.previousWindow = previous_window
        self.DBconnection = DBconnection
        self._initUI()

    def _initUI(self):
        self.mainVerticalLayout = QVBoxLayout(self)
        self.login_line = QLineEdit(self)
        self.mainVerticalLayout.addWidget(self.login_line)
        self.password_line = QLineEdit(self)
        self.password_line.setEchoMode(QLineEdit.Password)
        self.mainVerticalLayout.addWidget(self.password_line)
        horizontalLayout = QHBoxLayout(self)
        self.confirm_password_line = QLineEdit(self)
        self.confirm_password_line.setEchoMode(QLineEdit.Password)
        self.confirm_password_line.textChanged.connect(self._CheckPasswords)
        horizontalLayout.addWidget(self.confirm_password_line)
        self.confirmLabel = QLabel(self)
        horizontalLayout.addWidget(self.confirmLabel)
        self.mainVerticalLayout.addLayout(horizontalLayout)
        self.birth_date_line = CustomDateEdit(self)
        self.birth_date_line.setCalendarPopup(True)
        self.mainVerticalLayout.addWidget(self.birth_date_line)
        horizontalLayout = QHBoxLayout(self)
        self.enter_button = QPushButton(self)
        self.enter_button.setStyleSheet('QPushButton {background-color: green; color: white;}')
        self.enter_button.clicked.connect(self._AddUser)
        horizontalLayout.addWidget(self.enter_button)
        self.cancel_button = QPushButton(self)
        self.cancel_button.setStyleSheet('QPushButton {background-color: red; color: white;}')
        self.cancel_button.clicked.connect(self._Close)
        horizontalLayout.addWidget(self.cancel_button)
        self.mainVerticalLayout.addLayout(horizontalLayout)
        self.login_line.setPlaceholderText(u"Имя пользователя")
        self.confirm_password_line.setPlaceholderText(u"Повторите пароль")
        self.enter_button.setText(u"ОК")
        self.cancel_button.setText(u"Отмена")
        self.password_line.setPlaceholderText(u"Пароль")

    def closeEvent(self, event):
        self._Close()

    def _CheckPasswords(self):
        if self.password_line.text() != self.confirm_password_line.text():
            self.confirmLabel.setText(u"пароли не совпадают")
            self.confirmLabel.setStyleSheet("color: rgb(255, 0, 0)")
        else:
            self.confirmLabel.setText(u"пароли совпадают")
            self.confirmLabel.setStyleSheet("color: rgb(0, 255, 0)")

    def _AddUser(self):
        login = self.login_line.text()
        password = self.password_line.text()
        birth_date = self.birth_date_line.text()
        if (not login) or (not birth_date) or (not password):
            msg = QMessageBox.information(self, u"Внимание!", u"Вы не заполнили все поля.")
            return
        if password != self.confirm_password_line.text():
            msg = QMessageBox.information(self, u"Внимание!", u"Пароли не совпадают.")
            return
        if len(login) > 100:
            msg = QMessageBox.information(self, u'Внимание!', u'Запись слишком большая '
                                                              u'логин максимум 100 символов.')
            return
        password_hash = hashlib.md5(password.toLocal8Bit()).hexdigest()
        try:
            cursor = self.DBconnection.cursor()
            cursor.execute(u"select * from logins where login = '{}'".format(login))
            if len(cursor.fetchall()):
                msg = QMessageBox.information(self, u"Внимание!", u"Пользователь с таким логином уже существует.")
                return
            cursor.execute(u"insert into logins (login, password_hash, birth_date) VALUES ('{}', '{}', '{}')".format(
                login, password_hash, birth_date))
            cursor.close()
            self.DBconnection.commit()
        except Exception as e:
            print("Error while execute query:", e)
            sys.exit(1)
        msg = QMessageBox.information(self, u"Поздравляем!", u"Вы успешно зарегистрировались!")
        self._Close()

    def _Close(self):
        self.close()
        self.previousWindow.show()
