import sys

from PyQt5 import uic
from PyQt5.QtWidgets import *

form_selectwordwindow = uic.loadUiType("./select_word.ui")[0]

class SelectWordwindow(QDialog, QWidget, form_selectwordwindow):
    def __init__(self):
        super(SelectWordwindow, self).__init__()
        self.setupUi(self)
        self.show()


    def initUi(self):
        self.setupUi(self)

        def nextcheckNoise(self):
            self.hide()
            self.second = check_noisewindow()
            self.second.exec()
            self.second.show()

