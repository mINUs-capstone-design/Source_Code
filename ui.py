import sys

from PyQt5 import uic
from PyQt5.QtWidgets import *
import resource_rc
form_class = uic.loadUiType("./start.ui")[0]

form_checknoisewindow = uic.loadUiType("./check_noise.ui")[0]

form_selectwordwindow = uic.loadUiType("./select_word.ui")[0]

form_noisedwindow = uic.loadUiType("./noise.ui")[0]

form_resultdwindow = uic.loadUiType("./result.ui")[0]

form_speakdwindow = uic.loadUiType("./speak.ui")[0]


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def nextpage(self):
        self.hide()
        self.next = SelectWordwindow()
        self.next.exec_()
        self.show()



class SelectWordwindow(QDialog, QWidget, form_selectwordwindow):
    def __init__(self):
        super(SelectWordwindow, self).__init__()
        print("error1")
        self.initUI()
        print("errorinit")
        self.show()

    def end(self):
        self.close()
    def initUI(self):
        self.setupUi(self)


    def nextcheckNoise(self):
        self.hide()
        self.second = check_noisewindow()
        self.second.exec()
        self.second.show()


class check_noisewindow(QDialog,QWidget,form_checknoisewindow):
    def __init__(self):
        super(check_noisewindow,self).__init__()
        self.initUi()
        self.show()

    def initUi(self):
        self.setupUi(self)

    def nextNoise(self):
        self.hide()
        self.second = noisewindow()
        self.second.exec()
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
        self.second = speakwindow()
        self.second.exec()
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
        self.second = resultwindow()
        self.second.exec()
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