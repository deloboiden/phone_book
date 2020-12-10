# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtCore
from PyQt4.QtGui import *
from Registration import CustomDateEdit
from datetime import datetime, date, timedelta

class NewRecord(QDialog):
    def __init__(self, parent):
        super(NewRecord, self).__init__(parent)
        self.ok = False
        self.name, self.phone, self.birth_date = None, None, None
        self.mainVerticalLayout = QVBoxLayout(self)
        self.name_line = QLineEdit(self)
        self.mainVerticalLayout.addWidget(self.name_line)
        self.phone_line = QLineEdit(self)
        self.mainVerticalLayout.addWidget(self.phone_line)
        self.birth_date_line = CustomDateEdit(self)
        self.birth_date_line.setCalendarPopup(True)
        self.mainVerticalLayout.addWidget(self.birth_date_line)
        horizontalLayout = QHBoxLayout(self)
        self.enter_button = QPushButton(self)
        self.enter_button.clicked.connect(self.InsertRecord)
        self.enter_button.setStyleSheet('QPushButton {background-color: green; color: white;}')
        horizontalLayout.addWidget(self.enter_button)
        self.cancel_button = QPushButton(self)
        self.cancel_button.setStyleSheet('QPushButton {background-color: red; color: white;}')
        self.cancel_button.clicked.connect(self.close)
        horizontalLayout.addWidget(self.cancel_button)
        self.mainVerticalLayout.addLayout(horizontalLayout)
        self.name_line.setPlaceholderText(u"Имя")
        self.phone_line.setPlaceholderText(u"Номер")
        self.enter_button.setText(u"Добавить запись")
        self.cancel_button.setText(u"Отмена")

    def InsertRecord(self):
        self.name = self.name_line.text()
        self.phone = self.phone_line.text()
        self.birth_date = self.birth_date_line.text()
        if (not self.name) or (not self.birth_date) or (not self.phone):
            msg = QMessageBox.information(self, u'Внимание!', u'Вы не заполнили все поля.')
            return
        self.ok = True
        self.close()

class BirthdayDialog(QDialog):
    def __init__(self, parent, data):
        super(BirthdayDialog, self).__init__(parent)
        self.mainVerticalLayout = QVBoxLayout(self)
        self.InfoLabel = QLabel(self)
        self.InfoLabel.setText(u'близжайшие дни рождения у:')
        self.mainVerticalLayout.addWidget(self.InfoLabel)
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels([u'Имя', u'Номер телефона', u'Дата рождения'])
        self.mainVerticalLayout.addWidget(self.tableWidget)
        self.enter_button = QPushButton(self)
        self.enter_button.setText("OK")
        self.enter_button.clicked.connect(self.close)
        self.mainVerticalLayout.addWidget(self.enter_button)
        for record in data:
            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)
            self.tableWidget.setItem(row, 0, QTableWidgetItem(record[0]))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(record[1]))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(str(record[2])))



class MainWindow(QWidget):
    def __init__(self, previous_window, login, login_id, DBconnection):
        super(MainWindow, self).__init__()
        self.previousWindow = previous_window
        self.login = login
        self.login_id = login_id
        self.DBconnection = DBconnection
        self.bookmarks = [u'аб', u'вг', u'де', u'жзий', u'кл', u'мн', u'оп',
                          u'рс', u'ту', u'фх', u'цчшщ', u'ьъыэ', u'юя']
        self._initUI()
        self._FillTable()
        self.enteredItem = None
        self.enteredItemRowData = []

    def _initUI(self):
        self.mainVerticalLayout = QVBoxLayout(self)
        horizontalLayout = QHBoxLayout(self)
        self.loginLabel = QLabel(self)
        self.loginLabel.setText(u'Вы вошли как')
        horizontalLayout.addWidget(self.loginLabel)
        self.login_button = QPushButton(self)
        self.login_button.setText(self.login)
        self.login_button.clicked.connect(self._Relogin)
        self.login_button.setFlat(True)
        font = QFont()
        font.setUnderline(True)
        self.login_button.setFont(font)
        self.login_button.setStyleSheet("color: rgb(0, 0, 255)")
        self.login_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        horizontalLayout.addWidget(self.login_button)
        self.mainVerticalLayout.addLayout(horizontalLayout)
        self.tabWidget = QTabWidget(self)
        self.tabWidget.setTabPosition(QTabWidget.West)
        self.mainVerticalLayout.addWidget(self.tabWidget)
        horizontalLayout = QHBoxLayout(self)
        self.newButton = QPushButton(self)
        self.newButton.setText(u'добавить запись')
        self.newButton.setStyleSheet('QPushButton {background-color: green; color: white;}')
        self.newButton.clicked.connect(self._NewRecord)
        horizontalLayout.addWidget(self.newButton)
        self.deleteButton = QPushButton(self)
        self.deleteButton.setText(u'удалить запись')
        self.deleteButton.setStyleSheet('QPushButton {background-color: red; color: white;}')
        self.deleteButton.clicked.connect(self.DeleteRecord)
        horizontalLayout.addWidget(self.deleteButton)
        self.mainVerticalLayout.addLayout(horizontalLayout)

    def _AddNewTab(self, bookmark):
        tab = QWidget()
        verticalLayout = QVBoxLayout(tab)
        tableWidget = QTableWidget(tab)
        tableWidget.setColumnCount(3)
        tableWidget.setHorizontalHeaderLabels([u'Имя', u'Номер телефона', u'Дата рождения'])
        tableWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        tableWidget.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        tableWidget.setColumnWidth(1, 100)
        verticalLayout.addWidget(tableWidget)
        if bookmark == u'другие':
            self.tabWidget.addTab(tab, bookmark)
            return tableWidget
        for i in range(self.tabWidget.count()):
            if self.tabWidget.tabText(i) == u'другие' or \
                    self.bookmarks.index(unicode(self.tabWidget.tabText(i))) > self.bookmarks.index(bookmark):
                self.tabWidget.insertTab(i, tab, bookmark)
                return tableWidget
        self.tabWidget.addTab(tab, bookmark)
        return tableWidget

    def _InsertNewItem(self, tableWidget, row, name, phone, birth_date):
        tableWidget.insertRow(row)
        tableWidget.setItem(row, 0, QTableWidgetItem(name))
        tableWidget.setItem(row, 1, QTableWidgetItem(phone))
        tableWidget.setItem(row, 2, QTableWidgetItem(str(birth_date)))

    def _AddTableRecord(self, name, phone, birth_date):
        name = unicode(name)
        for bookmark in self.bookmarks:
            if name[0] in bookmark:
                for i in range(self.tabWidget.count()):
                    if self.tabWidget.tabText(i) == bookmark:
                        tableWidget = self.tabWidget.widget(i).findChild(QTableWidget)
                        numRows = tableWidget.rowCount()
                        self._InsertNewItem(tableWidget, numRows, name, phone, birth_date)
                        msg = QMessageBox.information(self, u'Внимание!',
                                                                u'Запись {}, {}, {} добавлена на вкладку {}'.format(
                                                                    name, phone, birth_date, bookmark
                                                                ))
                        return

                tableWidget = self._AddNewTab(bookmark)
                self._InsertNewItem(tableWidget, 0, name, phone, birth_date)
                tableWidget.cellChanged.connect(self.RefractorRecord)
                tableWidget.itemDoubleClicked.connect(self.EnterInItem)
                msg = QMessageBox.information(self, u'Внимание!',
                                                        u'Запись {}, {}, {} добавлена на вкладку {}'.format(
                                                            name, phone, birth_date, bookmark
                                                        ))
                return
        for i in range(self.tabWidget.count()):
            if self.tabWidget.tabText(i) == u'другие':
                tableWidget = self.tabWidget.widget(i).findChild(QTableWidget)
                numRows = tableWidget.rowCount()
                self._InsertNewItem(tableWidget, numRows, name, phone, birth_date)
                msg = QMessageBox.information(self, u'Внимание!',
                                                        u'Запись {}, {}, {} добавлена на вкладку {}'.format(
                                                            name, phone, birth_date, u'другие'
                                                        ))
                return
        tableWidget = self._AddNewTab(u'другие')
        self._InsertNewItem(tableWidget, 0, name, phone, birth_date)
        tableWidget.cellChanged.connect(self.RefractorRecord)
        tableWidget.itemDoubleClicked.connect(self.EnterInItem)
        msg = QMessageBox.information(self, u'Внимание!',
                                                u'Запись {}, {}, {} добавлена на вкладку {}'.format(
                                                    name, phone, birth_date, u'другие'
                                                ))

    def DeleteRecord(self):
        if self.tabWidget.currentIndex() < 0:
            return
        tableWidget = self.tabWidget.currentWidget().findChild(QTableWidget)
        currentRow = tableWidget.currentRow()
        if currentRow > -1:
            name = tableWidget.item(currentRow, 0).text()
            phone = tableWidget.item(currentRow, 1).text()
            birth_date = tableWidget.item(currentRow, 2).text()
            msg = QMessageBox()
            msg.setWindowTitle(u"Внимание!")
            msg.setText(u"Удалить запись: {}, {}, {}".format(name, phone, birth_date))
            okButton = msg.addButton(u'Удалить', QMessageBox.AcceptRole)
            okButton.setStyleSheet('QPushButton {background-color: green; color: white;}')
            cancel_button = msg.addButton(u'Отмена', QMessageBox.RejectRole)
            cancel_button.setStyleSheet('QPushButton {background-color: red; color: white;}')
            msg.exec_()
            if msg.clickedButton() == okButton:
                try:
                    cursor = self.DBconnection.cursor()
                    cursor.execute(u"delete from records where login_id = {} and name = '{}' and telephone_number = '{}'"
                                   u" and birth_date = '{}'".format(self.login_id, name, phone, birth_date))
                    self.DBconnection.commit()
                    cursor.close()
                except Exception as e:
                    print("Error while execute query:", e)
                    sys.exit(1)
                tableWidget.removeRow(currentRow)
                if tableWidget.rowCount() == 0:
                    self.tabWidget.removeTab(self.tabWidget.currentIndex())

    def RefractorRecord(self, row, column):
        columnDictionary = {0:'name', 1:'telephone_number', 2:'birth_date'}
        tableWidget = self.tabWidget.currentWidget().findChild(QTableWidget)
        if tableWidget.item(row, column) == self.enteredItem:
            newdata = tableWidget.item(row, column).text()
            if column == 2:
                try:
                    datetime.strptime(newdata, "%Y-%m-%d")
                except Exception:
                    msg = QMessageBox.information(self, u'Внимание!', u'Дата в неправильном формате')
                    tableWidget.item(row, column).setText(self.enteredItemRowData[2])
                    return
            if column == 0:
                tableWidget.removeRow(row)
                if tableWidget.rowCount() == 0:
                    self.tabWidget.removeTab(self.tabWidget.currentIndex())
                self._AddTableRecord(newdata, self.enteredItemRowData[1], self.enteredItemRowData[2])
            try:
                cursor = self.DBconnection.cursor()
                cursor.execute(u"UPDATE records SET {} = '{}' where login_id = {} and name = '{}' and telephone_number "
                               u"= '{}' and birth_date = '{}'".format(columnDictionary[column], newdata, self.login_id,
                                                                     self.enteredItemRowData[0],
                                                                     self.enteredItemRowData[1],
                                                                     self.enteredItemRowData[2]))
                self.DBconnection.commit()
                cursor.close()
            except Exception as e:
                print("Error while execute query:", e)
                sys.exit(1)

    def _Relogin(self):
        msg = QMessageBox()
        msg.setWindowTitle(u"{} это не вы?".format(self.login))
        msg.setText(u"Зайти под другим пользователем?")
        okButton = msg.addButton(u'Да', QMessageBox.AcceptRole)
        msg.addButton(u'Отмена', QMessageBox.RejectRole)
        msg.exec_()
        if msg.clickedButton() == okButton:
            self.previousWindow.RememberLogin(self.login_id, False)
            self.previousWindow.login_line.clear()
            self.previousWindow.password_line.clear()
            self.close()
            self.previousWindow.show()

    def EnterInItem(self, item):
        tableWidget = self.tabWidget.currentWidget().findChild(QTableWidget)
        row = tableWidget.row(item)
        self.enteredItem = item
        self.enteredItemRowData = [tableWidget.item(row, 0).text(), tableWidget.item(row, 1).text(),
                                   tableWidget.item(row, 2).text()]

    def _FillTable(self):
        self.tabWidget.clear()
        try:
            cursor = self.DBconnection.cursor()
            cursor.execute(u"select name, telephone_number, birth_date from records where login_id = "
                              u"{} order by name".format(self.login_id), self.DBconnection)
            records = cursor.fetchall()
            cursor.close()
        except Exception as e:
            print("Error while execute query:", e)
            sys.exit(1)
        today = date.today()
        birthdays = [rec for rec in records if rec[2] >= today and rec[2] <= today + timedelta(days=7)]
        if len(birthdays):
            d = BirthdayDialog(self, birthdays)
            d.exec_()
        for bookmark in self.bookmarks:
            bookmarkRecords = [rec for rec in records if rec[0][0] in bookmark]
            records = [rec for rec in records if rec not in bookmarkRecords]
            if len(bookmarkRecords):
                tableWidget = self._AddNewTab(bookmark)
                for record in bookmarkRecords:
                    numRows = tableWidget.rowCount()
                    self._InsertNewItem(tableWidget, numRows, record[0], record[1],
                                        record[2])
                tableWidget.cellChanged.connect(self.RefractorRecord)
                tableWidget.itemDoubleClicked.connect(self.EnterInItem)
                tableWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        if len(records):
            tableWidget = self._AddNewTab(u'другие')
            for record in records:
                numRows = tableWidget.rowCount()
                self._InsertNewItem(tableWidget, numRows, record[0], record[1],
                                    record[2])
            tableWidget.cellChanged.connect(self.RefractorRecord)
            tableWidget.itemDoubleClicked.connect(self.EnterInItem)

    def _NewRecord(self):
        d = NewRecord(self)
        d.exec_()
        if d.ok:
            if len(d.name) > 100 or len(d.phone) > 100:
                msg = QMessageBox.information(self, u'Внимание!', u'Запись слишком большая '
                                                                  u'имя и номер максимум 100 символов.')
                return
            try:
                cursor = self.DBconnection.cursor()
                cursor.execute(u"select * from records where login_id = {} and name = '{}' and telephone_number = '{}'"
                               u" and birth_date = '{}'".format(self.login_id, d.name, d.phone, d.birth_date))
                if len(cursor.fetchall()):
                    msg = QMessageBox.information(self, u'Внимание!', u'Запись с такими данными уже '
                                                                               u'существует.')
                    return
                cursor.execute(u"insert into records (login_id, name, telephone_number, birth_date) VALUES "
                               u"({}, '{}', '{}', '{}')".format(self.login_id, d.name, d.phone, d.birth_date))
                self.DBconnection.commit()
                cursor.close()
            except Exception as e:
                print("Error while execute query:", e)
                sys.exit(1)
            self._AddTableRecord(d.name, d.phone, d.birth_date)

    def closeEvent(self, event):
        self._Close()

    def _Close(self):
        self.close()
        self.previousWindow.close()
