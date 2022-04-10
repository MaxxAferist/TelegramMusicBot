from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
import sys
import random


class Menu_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(807, 569)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 807, 569))
        self.label.setText("")
        self.label.setObjectName("label")
        self.start_game = QtWidgets.QPushButton(self.centralwidget)
        self.start_game.setGeometry(QtCore.QRect(290, 180, 210, 61))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.start_game.setFont(font)
        self.start_game.setStyleSheet("QPushButton{\n"
"    position: relative;\n"
"    background-color: #FFFFF;\n"
"    border: 5px solid #9acd32;\n"
"      font: bold 16px;\n"
"    color: #9acd32;\n"
"    width: 200px;\n"
"    text-align: center;\n"
"    point-size: 16px;\n"
"     border-radius: 12px\n"
"}\n"
"\n"
"QPushButton:hover\n"
"{\n"
"   background-color:#9acd32;\n"
"    color:white\n"
"}")
        self.start_game.setObjectName("start_game")
        self.settings_button = QtWidgets.QPushButton(self.centralwidget)
        self.settings_button.setGeometry(QtCore.QRect(290, 260, 210, 61))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.settings_button.setFont(font)
        self.settings_button.setStyleSheet("QPushButton{\n"
"    position: relative;\n"
"    background-color: #FFFFF;\n"
"    border: 5px solid #9acd32;\n"
"      font: bold 16px;\n"
"    color: #9acd32;\n"
"    width: 200px;\n"
"    text-align: center;\n"
"    point-size: 16px;\n"
"     border-radius: 12px\n"
"}\n"
"\n"
"QPushButton:hover\n"
"{\n"
"   background-color:#9acd32;\n"
"    color:white\n"
"}")
        self.settings_button.setObjectName("settings_button")
        self.exit_button = QtWidgets.QPushButton(self.centralwidget)
        self.exit_button.setGeometry(QtCore.QRect(290, 340, 210, 61))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.exit_button.setFont(font)
        self.exit_button.setStyleSheet("QPushButton{\n"
"    position: relative;\n"
"    background-color: #FFFFF;\n"
"    border: 5px solid #9acd32;\n"
"      font: bold 16px;\n"
"    color: #9acd32;\n"
"    width: 200px;\n"
"    text-align: center;\n"
"    point-size: 16px;\n"
"     border-radius: 12px\n"
"}\n"
"\n"
"QPushButton:hover\n"
"{\n"
"   background-color:#9acd32;\n"
"    color:white\n"
"}")
        self.exit_button.setObjectName("exit_button")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.start_game.setText(_translate("MainWindow", "Играть"))
        self.settings_button.setText(_translate("MainWindow", "Настройки"))
        self.exit_button.setText(_translate("MainWindow", "Выход"))


class Game_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(801, 568)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 801, 568))
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(100, 30, 581, 91))
        self.label_2.setText("")
        self.label_2.setStyleSheet("QLabel{\n"
"text-align: center;\n"
"font-size: 16px;"
"}")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(300, 400, 200, 200))
        self.label_3.setText("Ошибки: 0/3")
        self.label_3.setStyleSheet("QLabel{\n"
                                   "text-align: center;\n"
                                   "font-size: 30px;"
                                   "}")
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(30, 220, 210, 61))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setAutoFillBackground(False)
        self.pushButton.setStyleSheet("QPushButton{\n"
"    position: relative;\n"
"    background-color: #FFFFF;\n"
"    border: 5px solid #9acd32;\n"
"      font: bold 14px;\n"
"    color: #9acd32;\n"
"    width: 200px;\n"
"    text-align: center;\n"
"    point-size: 10px;\n"
"     border-radius: 12px\n"
"}\n"
"\n"
"QPushButton:hover\n"
"{\n"
"   background-color:#9acd32;\n"
"    color:white\n"
"}")
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(30, 370, 210, 61))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("QPushButton{\n"
"    position: relative;\n"
"    background-color: #FFFFF;\n"
"    border: 5px solid #310062;\n"
"      font: bold 14px;\n"
"    color: #310062;\n"
"    width: 200px;\n"
"    text-align: center;\n"
"    point-size: 10px;\n"
"     border-radius: 12px\n"
"}\n"
"\n"
"QPushButton:hover\n"
"{\n"
"   background-color: #310062;\n"
"    color:white\n"
"}")
        self.pushButton_2.setText("")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(540, 370, 210, 61))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("QPushButton{\n"
"    position: relative;\n"
"    background-color: #FFFFF;\n"
"    border: 5px solid #ffff00;\n"
"      font: bold 14px;\n"
"    color: #ffff00;\n"
"    width: 200px;\n"
"    text-align: center;\n"
"    point-size: 10px;\n"
"     border-radius: 12px\n"
"}\n"
"\n"
"QPushButton:hover\n"
"{\n"
"   background-color:#ffff00;\n"
"    color:white\n"
"}")
        self.pushButton_3.setText("")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(540, 220, 210, 61))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setStyleSheet("QPushButton{\n"
"    position: relative;\n"
"    background-color: #FFFFF;\n"
"    border: 5px solid red;\n"
"      font: bold 14px;\n"
"    color: #FFFFFF;\n"
"    width: 200px;\n"
"    text-align: center;\n"
"    color:red;\n"
"    point-size: 10px;\n"
"     border-radius: 12px\n"
"}\n"
"\n"
"QPushButton:hover\n"
"{\n"
"   background-color:red;\n"
"    color:white\n"
"}")
        self.pushButton_4.setText("")
        self.pushButton_4.setObjectName("pushButton_4")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))


class Menu(QMainWindow, Menu_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pixmap = QPixmap('static/image/background.jpg')
        self.label.setPixmap(self.pixmap)
        self.exit_button.clicked.connect(self.exit)
        self.start_game.clicked.connect(self.go_game)

    def go_game(self):
        self.ex = Game()
        self.ex.show()
        self.close()

    def exit(self):
        sys.exit(app.exec_())


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(374, 195)
        font = QtGui.QFont()
        font.setPointSize(16)
        Dialog.setFont(font)
        self.lb2 = QtWidgets.QLabel(Dialog)
        self.lb2.setGeometry(QtCore.QRect(20, 30, 331, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.lb2.setFont(font)
        self.lb2.setText("")
        self.lb2.setObjectName("lb2")
        self.lb2.setStyleSheet("QLabel{"
                               "text-align: center"
                               "}")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(280, 150, 75, 23))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Ок"))


class Win_or_Lose(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.exit)

    def win(self):
        self.lb2.setText('Поздравляю, вы победили!')

    def lose(self):
        self.lb2.setText('Вы проиграли!')

    def exit(self):
        sys.exit(app.exec_())


class Game(QMainWindow, Game_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Game')
        self.count = 0
        self.mistakes = 0
        self.dct = {}
        self.preparation()
        self.pushButton.clicked.connect(lambda: self.game(self.pushButton.text()))
        self.pushButton_2.clicked.connect(lambda: self.game(self.pushButton_2.text()))
        self.pushButton_3.clicked.connect(lambda: self.game(self.pushButton_3.text()))
        self.pushButton_4.clicked.connect(lambda: self.game(self.pushButton_4.text()))

    def preparation(self):
        con = sqlite3.connect('db/music.db')
        cur = con.cursor()
        lst_but = [self.pushButton, self.pushButton_2, self.pushButton_3, self.pushButton_4]
        id = random.randint(1, cur.execute('SELECT COUNT(1) FROM songs').fetchone()[0])
        self.dct[cur.execute(f'SELECT artist FROM songs WHERE id = {id}').fetchone()[0]] = 1
        title = cur.execute(f'SELECT title FROM songs WHERE id = {id}').fetchone()[0]
        self.label_2.setText(f'Кто автор песни {title}? {self.count}/5')
        lst_id = [id]

        true_button = random.choice(lst_but)
        true_button.setText(list(self.dct.keys())[0])
        for i in lst_but:
            if not i.text():
                list_names = [cur.execute(f'SELECT artist FROM songs WHERE id = {i}').fetchone()[0] for i in lst_id]
                id_false = random.randint(1, cur.execute('SELECT COUNT(1) FROM songs').fetchone()[0])
                while cur.execute(f'SELECT artist FROM songs WHERE id = {id_false}').fetchone()[0] in list_names:
                    id_false = random.randint(1, cur.execute('SELECT COUNT(1) FROM songs').fetchone()[0])
                lst_id.append(id_false)
                self.dct[cur.execute(f'SELECT artist FROM songs WHERE id = {id_false}').fetchone()[0]] = 0
                i.setText(cur.execute(f'SELECT artist FROM songs WHERE id = {id_false}').fetchone()[0])
        con.close()

    def game(self, ans):
        print(self.dct)
        if self.dct[ans] == 1:
            self.dct = {}
            self.count += 1
            if self.count == 5:
                self.win = Win_or_Lose()
                self.win.win()
                self.win.show()
            else:
                self.pushButton.setText('')
                self.pushButton_2.setText('')
                self.pushButton_3.setText('')
                self.pushButton_4.setText('')
                self.preparation()
        else:
            self.mistakes += 1
            self.label_3.setText(f'Ошибки: {self.mistakes}/3')
            if self.mistakes == 3:
                self.win = Win_or_Lose()
                self.win.lose()
                self.win.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Menu()
    ex.show()
    sys.exit(app.exec_())