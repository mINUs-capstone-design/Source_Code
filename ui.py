import sys

from PyQt5 import uic
from PyQt5.QtWidgets import *
import resource_rc
form_class = uic.loadUiType("./start.ui")[0]

form_checknoisewindow = uic.loadUiType("./check_noise.ui")[0]

form_selectsexwindow = uic.loadUiType("./select_sex.ui")[0]


form_noisedwindow = uic.loadUiType("./noise.ui")[0]

form_resultdwindow = uic.loadUiType("./result.ui")[0]

form_speakdwindow = uic.loadUiType("./speak.ui")[0]


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def nextpage(self):
        self.hide()
        self.next = SelectSexwindow()
        self.next.exec()
        self.show()

class SelectSexwindow(QDialog, QWidget, form_selectsexwindow):
    def __init__(self):
        super(SelectSexwindow, self).__init__()

        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)


    def nextcheckNoise(self):
        self.hide()
        self.second = check_noisewindow()
        self.second.exec()
        self.show()

    def backtomain(self):
        self.close()

class check_noisewindow(QDialog,QWidget,form_checknoisewindow):
    def __init__(self):
        super(check_noisewindow,self).__init__()
        self.initUi()
        self.show()

    def initUi(self):
        self.setupUi(self)

    def nextNoise(self):
        self.hide()
        self.nextnoise = noisewindow()
        self.nextnoise.exec()
        self.show()

    def backtoselectsex(self):
        self.hide()
        self.nextnoise = SelectSexwindow()
        self.nextnoise.exec()
        self.show()

class noisewindow(QDialog,QWidget,form_noisedwindow):
    def __init__(self):
        super(noisewindow,self).__init__()
        self.initUi()
        self.show()

    def initUi(self):
        self.setupUi(self)

    def nextSpeak(self):
        self.hide()
        self.nextspeak = speakwindow()
        self.nextspeak.exec()
        self.show()

class speakwindow(QDialog,QWidget,form_speakdwindow):
    def __init__(self):
        super(speakwindow,self).__init__()
        self.initUi()
        self.show()

    def initUi(self):
        self.setupUi(self)

    def nextResult(self):
        self.hide()
        self.nextresult = resultwindow()
        self.nextresult.exec()
        self.show()

class resultwindow(QDialog,QWidget,form_resultdwindow):
    def __init__(self):
        super(resultwindow,self).__init__()
        self.initUi()
        self.show()

    def initUi(self):
        self.setupUi(self)

    def nextClick(self):
        self.hide()
        self.second = form_resultdwindow()
        self.second.exec()
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()