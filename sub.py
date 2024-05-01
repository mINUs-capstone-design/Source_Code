import sys

from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


form_class = uic.loadUiType("./sub.ui")[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.checknoise.setHidden(True)
        self.selectsexual.setHidden(True)
        self.resultnoise.setHidden(True)
        self.result.setHidden(True)
        self.button_selectsexual.clicked.connect(self.uiselectsexual)
        self.button_startchecknoise.clicked.connect(self.uichecknoise)
        self.button_resultnoise.clicked.connect(self.uiresultnoise)
        self.button_result.clicked.connect(self.uiresult)
        self.button_backtoselectsexual.clicked.connect(self.uiselectsexual)
        self.button_backtochecknoise.clicked.connect(self.uichecknoise)
        self.button_backtomain.clicked.connect(self.uimain)
        self.button_rerecord.clicked.connect(self.uiresultnoise)
        self.button_exit.clicked.connect(self.close)
        self.noise = None
        self.dialog = QDialog()
    def uimain(self):
        self.selectsexual.hide()
        self.checknoise.hide()
        self.resultnoise.hide()
        self.result.hide()
        self.mainwindow.show()
    def uiselectsexual(self):
        self.selectsexual.show()
        self.checknoise.hide()
        self.resultnoise.hide()
        self.result.hide()
        self.mainwindow.hide()

    def uichecknoise(self):
        self.selectsexual.hide()
        self.checknoise.show()
        self.resultnoise.hide()
        self.result.hide()
        self.mainwindow.hide()
        self.dialog.setWindowTitle("Dialog")
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.resize(300,200)
        self.noise = "noisecount"# 소음 입력 할것
        noiselabel = QLabel(self.dialog)
        noiselabel.move(100,100)
        noiselabel.setText(self.noise)
        self.dialog.show()

    def uiresultnoise(self):
        self.selectsexual.hide()
        self.checknoise.hide()
        self.resultnoise.show()
        self.result.hide()
        self.mainwindow.hide()
    def uiresult(self):
        self.selectsexual.hide()
        self.checknoise.hide()
        self.resultnoise.hide()
        self.result.show()
        self.mainwindow.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = WindowClass()
    ui.show()
    exit(app.exec_())