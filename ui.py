import os
import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic
def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form_start = resource_path('start.ui')
form_class = uic.loadUiType(form_start)[0]

form_check_noise = resource_path('check_noise.ui')
form_checknoisewindow = uic.loadUiType(form_check_noise)[0]

form_select_word = resource_path('select_word.ui')
form_selectwordwindow = uic.loadUiType(form_select_word)[0]

form_noise = resource_path('noise.ui')
form_noisedwindow = uic.loadUiType(form_noise)[0]

form_result = resource_path('result.ui')
form_resultdwindow = uic.loadUiType(form_result)[0]

form_speak = resource_path('speak.uiui')
form_speakdwindow = uic.loadUiType(form_speak)[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def btn_main_to_second(self):
        self.hide()
        self.second = check_noisewindow()
        self.second.exec()
        self.show()

class check_noisewindow(QDialog,QWidget,form_checknoisewindow):
    def __init__(self):
        super(check_noisewindow,self).__init__()
        self.initUi()
        self.show()

    def initUi(self):
        self.setupUi(self)

    def btn_second_to_main(self):
        self.close()

class selectwindow(QDialog,QWidget,form_selectwordwindow):
    def __init__(self):
        super(selectwindow,self).__init__()
        self.initUi()
        self.show()

    def initUi(self):
        self.setupUi(self)

    def btn_second_to_main(self):
        self.close()
class select_wordwindow(QDialog,QWidget,form_selectwordwindow):
    def __init__(self):
        super(select_wordwindow,self).__init__()
        self.initUi()
        self.show()

    def initUi(self):
        self.setupUi(self)

    def btn_second_to_main(self):
        self.close()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()