import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import *
from requests import request
from data import db_session
from data.users import User
from data.searches import Search
from PyQt5 import QtCore, QtGui, QtWidgets
from ctypes import *
from quest_game import Menu
import requests

KOEF = windll.user32.GetSystemMetrics(0) / 1920


class Window_start(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 400)
        MainWindow.setWindowOpacity(1.0)
        MainWindow.setToolTipDuration(-1)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 20, 480, 30))
        self.label.setStyleSheet("font: 25 16pt \"Microsoft YaHei Light\";")
        self.label.setIndent(-1)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 480, 30))
        self.label_2.setStyleSheet("font: 25 16pt \"Microsoft YaHei Light\";")
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(50, 140, 150, 25))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(310, 140, 150, 25))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(50, 100, 140, 30))
        self.label_3.setStyleSheet("font: 25 16pt \"Microsoft YaHei Light\";")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(310, 100, 140, 30))
        self.label_4.setStyleSheet("font: 25 16pt \"Microsoft YaHei Light\";")
        self.label_4.setObjectName("label_4")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(180, 180, 140, 40))
        self.pushButton.setObjectName("pushButton")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(10, 240, 480, 40))
        self.label_5.setStyleSheet("font: 25 16pt \"Microsoft YaHei Light\";")
        self.label_5.setObjectName("label_5")
        self.hidden_label = QtWidgets.QLabel(self.centralwidget)
        self.hidden_label.setGeometry(QtCore.QRect(20, 340, 200, 30))
        self.hidden_label.setStyleSheet(
            "font: 25 10pt \"Microsoft YaHei Light\";")
        self.hidden_label.setObjectName("hidden_label")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(180, 285, 140, 40))
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 500, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Приветсвуем"))
        self.label.setText(_translate(
            "MainWindow", f"<html><head/><body><p align=\"center\"><span style=\" font-size:{16 * KOEF}pt;\">Приветствуем, в игре &quot;Споп&quot;</span></p></body></html>"))
        self.label_2.setText(_translate(
            "MainWindow", f"<html><head/><body><p align=\"center\"><span style=\" font-size:{16 * KOEF}pt;\">Введите логин и пароль</span></p></body></html>"))
        self.label_3.setText(_translate(
            "MainWindow", f"<html><head/><body><p align=\"center\"><span style=\" font-size:{16 * KOEF}pt;\">Логин</span></p></body></html>"))
        self.label_4.setText(_translate(
            "MainWindow", f"<html><head/><body><p align=\"center\"><span style=\" font-size:{16 * KOEF}pt;\">Пароль</span></p></body></html>"))
        self.pushButton.setText(_translate("MainWindow", "Войти"))
        self.label_5.setText(_translate(
            "MainWindow", f"<html><head/><body><p align=\"center\"><span style=\" font-size:{16 * KOEF}pt;\">Если у вас нет регистрации(Нелегалы)</span></p></body></html>"))
        self.pushButton_2.setText(_translate("MainWindow", "Регистрация"))


class Window_reg(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 250)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 480, 50))
        self.label.setStyleSheet("font: 25 16pt \"Microsoft YaHei Light\";")
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(220, 60, 150, 25))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(220, 100, 150, 25))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 55, 181, 30))
        self.label_2.setStyleSheet("font: 25 16pt \"Microsoft YaHei Light\";")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 95, 181, 30))
        self.label_3.setStyleSheet("font: 25 16pt \"Microsoft YaHei Light\";")
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(290, 140, 191, 41))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.hidden_label = QtWidgets.QLabel(self.centralwidget)
        self.hidden_label.setGeometry(QtCore.QRect(20, 190, 480, 30))
        self.hidden_label.setStyleSheet(
            "font: 25 10pt \"Microsoft YaHei Light\";")
        self.hidden_label.setObjectName("hidden_label")
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 500, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate(
            "MainWindow", f"<html><head/><body><p align=\"center\"><span style=\" font-size:{22 * KOEF}pt;\">Регистрация</span></p></body></html>"))
        self.label_2.setText(_translate(
            "MainWindow", f"<html><head/><body><p align=\"right\"><span style=\" font-size:{16 * KOEF}pt;\">Логин</span></p></body></html>"))
        self.label_3.setText(_translate(
            "MainWindow", f"<html><head/><body><p align=\"right\"><span style=\" font-size:{16 * KOEF}pt;\">Пароль</span></p></body></html>"))

        self.pushButton.setText(_translate("MainWindow", "Зарегистрироваться"))


class MainWindow(QMainWindow, Window_start):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.start)
        self.pushButton_2.clicked.connect(self.go_reg)

    def start(self):
        self.hidden_label.setText('')
        login = self.lineEdit.text()
        password = self.lineEdit_2.text()
        if login and password:
            json_push = {
                'name': login,
                'password': password
            }
            resp = requests.post(
                'http://localhost:8000/api/game/login/name', json=json_push).json()
            if not resp.get('result') and resp.get('error') == 415:
                self.hidden_label.setText('Такого имени не существует!')
            elif resp.get('result'):
                user_id = resp.get('user_id')
                self.user_id = user_id
                self.go_menu()
            else:
                self.hidden_label.setText('Неправильный пароль')

    def go_reg(self):
        self.ex = Reg_Window()
        self.ex.show()
        self.close()

    def go_menu(self):
        self.menu = Menu(self.user_id)
        self.menu.show()
        self.close()


class Reg_Window(QMainWindow, Window_reg):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.added)

    def added(self):
        self.hidden_label.setText('')
        login = self.lineEdit.text()
        password = self.lineEdit_2.text()
        if login and password:
            json_push = {'name': login,
                         'password': password}
            resp = requests.post(
                'http://localhost:8000/api/game/register/user', json=json_push).json()
            if not resp.get('OK'):
                self.hidden_label.setText('Такое имя уже существует!')
                return 2
            self.go_main()

    def go_main(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
