# ----------------------------------------------------------------
import os
import sys
#import spidev

from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import time
import math
import record
import torchvision
import torchvision.datasets as dset
import torchvision.transforms as transforms
from torch.utils.data import DataLoader,Dataset
import matplotlib.pyplot as plt
import torchvision.utils
import numpy as np
import random
from PIL import Image
import torch
from torch.autograd import Variable
import PIL.ImageOps
import torch.nn as nn
from torch import optim
import torch.nn.functional as F

import button_rc

# 추가...voice_code의 vad.py, mel.py
from voice_code import vad, mel

form_class = uic.loadUiType("./sub.ui")[0]
# ----------------------------------------------------------------



# ----------------------------------------------------------------
# button 기능 함수
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
        #self.button_resultnoise.clicked.connect(self.show_noise_result)
        self.button_startrecord.clicked.connect(self.start_record)
        self.button_stoprecord.clicked.connect(self.uiresult)
        self.button_backtoselectsexual.clicked.connect(self.uiselectsexual)
        self.button_backtochecknoise.clicked.connect(self.uichecknoise)
        self.button_backtomain.clicked.connect(self.uimain)
        self.button_rerecord.clicked.connect(self.uiresultnoise)
        self.button_exit.clicked.connect(self.close)
        noise = None
        #self.spi = spidev.SpiDev()
        #self.spi.open(0,0)
        #self.spi.max_speed_hz = 1350000
        self.dialog = QDialog()
        self.noiselabel = QLabel(self.dialog)
        self.buttongroup_sexual = QButtonGroup(self)
        self.buttongroup_sexual.setExclusive(True)
        self.buttongroup_sexual.addButton(self.check_man,1)
        self.buttongroup_sexual.addButton(self.check_woman,2)
        

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
        self.noiselabel.clear()
    
    
    # def read_sensor_data(self):
    #     # 사운드 센서값을 불러오는 함수
    #     while True:
            
    #         r = self.spi.xfer2([1, (8 + 0) << 4, 0])
    #         adc_out = ((r[1] & 3) << 8) + r[2]
    #         analog_value = adc_out
    #         if analog_value <= 0:
    #             analog_value = 1
    #         db_value = round(20 * math.log10(analog_value), 1)
    #         time.sleep(0.5)
    #         return db_value
    
    
    def uiresultnoise(self):
        self.selectsexual.hide()
        self.checknoise.hide()
        self.resultnoise.show()
        self.button_stoprecord.hide()
        self.button_startrecord.show()
        #self.select_word.setPlainText(random(list))
        self.result.hide()
        self.mainwindow.hide()
    
    # 녹음시작
    def start_record(self):
        # 녹음 시작 전에, 유사도 측정한 파일들 삭제
        if os.path.exists("record_after_vad.wav"):
            os.remove("record_after_vad.wav")
        if os.path.exists("Mel_record_after_vad.jpg"):
            os.remove("Mel_record_after_vad.jpg")
            
        self.button_startrecord.hide()
        self.button_stoprecord.show()
        record.start()

    # 녹음종료
    def uiresult(self):
        self.selectsexual.hide()
        self.checknoise.hide()
        self.resultnoise.hide()
        record.stop()
        self.result.show()
        self.mainwindow.hide()

        # 녹음 후 생긴 record.wav에 VAD, MEL 적용
        new_record_file = "record_after_vad.wav"
        
        vad.take_vad(new_record_file)
        mel.take_mel(new_record_file)
        
        # VAD, MEL 적용 전 원본 .wav랑 .jpg 삭제
        os.remove("record.wav")
        os.remove("Mel_record.jpg")
        
        # 유사도 측정을 녹음 후에 실행하기
        # 맨위에 __init__ 부분에 이어붙이면, 녹음 전에 먼저 실행됨...
        self.similar_test()
    
    
    # 유사도 측정 함수
    def similar_test(self):
        # 측정...
        device = "cuda" if torch.cuda.is_available() else "cpu"
        # 모델 이름 경로
        model = torch.load("siamese_net_v4.pt", map_location=device)
        
        # 비교하려는 이미지(.jpg)들의 경로
        # x0 : 사용자가 녹음한 음성데이터의 Mel 이미지
        # x1 : 기준이 되는 TTS 음성데이터의 Mel 이미지
        x0 = Image.open("Mel_record_after_vad.jpg")
        x1 = Image.open("data/testing/korean/Mel_spectrum_VAD_KsponSpeech_000091.jpg")

        convert_tensor = transforms.Compose([transforms.Resize((99,250)),transforms.ToTensor()])
        x0 = convert_tensor(x0).unsqueeze(0)
        x1 = convert_tensor(x1).unsqueeze(0)
        print(x0.shape)
        print(x1.shape)

        output1, output2 = model(x0, x1)
        euclidean_distance = F.pairwise_distance(output1, output2)
        final_similar_score = getScore(euclidean_distance.item())

        # 유사도 측정 결과를 pyqt5 위젯에 표시...터미널X
        #print(f"score : {getScore(euclidean_distance.item())}")
        
        # 기존에 "유사도 안내 : 90%" 라고 출력하던 곳에 결과 출력
        # self.[].setText() 함수 이용
        # ex) self.text_label.setText('hello world') 형태...self는 함수에서 써야 함
        # f"" 안에 띄어쓰기 -> 위젯에서 가운데에 표시하려고 함 (앞에 8칸 띄기)
        self.check_word_4.setText(f"        유사도 안내 : {final_similar_score}%")
    
    
    
    
    # def show_noise_result(self):
    #     self.dialog.setWindowTitle("Dialog")
    #     self.dialog.setWindowModality(Qt.ApplicationModal)
    #     self.dialog.resize(300, 200)
    #     noise = None
    #     db_value = self.read_sensor_data()  # 사운드센서 값 불러옴
    #     noise = str(db_value) + "db"
    #     self.noiselabel.move(150, 100)
    #     self.noiselabel.setText(noise)
    #     if db_value > 40:
    #         self.noiselabel.setStyleSheet("COLOR : red")
    #     elif db_value <= 40 and db_value > 20:
    #         self.noiselabel.setStyleSheet("COLOR : yellow")
    #     else:
    #         self.noiselabel.setStyleSheet("COLOR : green")
    #     self.dialog.setWindowTitle("소음측정결과")
    #     self.dialog.exec()
        
    


    #list = ['안녕하세요', '바가지','도깨비','고구마','누룽지','주전자']
# ----------------------------------------------------------------



# ----------------------------------------------------------------
class Config():
    testing_dir = "./testing"


def imshow(img, text=None, should_save=False):
    npimg = img.numpy()
    plt.axis("off")
    if text:
        plt.text(75, 8, text, style='italic', fontweight='bold',
                 bbox={'facecolor': 'white', 'alpha': 0.8, 'pad': 10})
    plt.imshow(np.transpose(npimg, (1, 2, 0)))
    plt.show()


def show_plot(iteration, loss):
    plt.plot(iteration, loss)
    plt.show()
# ----------------------------------------------------------------



# ----------------------------------------------------------------
# 유사도 점수 측정 함수
def getScore(dissimilarity):
  
  if dissimilarity >= 2.0:
    score = 0
  else:
    score = 100 - dissimilarity*50
    score = round(score)
  
  return score


# 유사도 측정 모델
class SiameseNetwork(nn.Module):
    def __init__(self):
        super(SiameseNetwork, self).__init__()
        self.cnn1 = nn.Sequential(
            nn.ReflectionPad2d(1),
            nn.Conv2d(3, 4, kernel_size=3),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(4),

            nn.ReflectionPad2d(1),
            nn.Conv2d(4, 8, kernel_size=3),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(8),


            nn.ReflectionPad2d(1),
            nn.Conv2d(8, 8, kernel_size=3),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(8),


        )

        self.fc1 = nn.Sequential(
            nn.Linear(8*99*250, 500),
            nn.ReLU(inplace=True),

            nn.Linear(500, 500),
            nn.ReLU(inplace=True),

            nn.Linear(500, 5))

    def forward_once(self, x):
        output = self.cnn1(x)
        output = output.view(output.size()[0], -1) # flatten
        output = self.fc1(output)
        return output

    def forward(self, input1, input2):
        output1 = self.forward_once(input1)
        output2 = self.forward_once(input2)
        return output1, output2


# 나머진 위에 함수로 옮김
# ...

# ----------------------------------------------------------------



# ----------------------------------------------------------------
# main문
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = WindowClass()
    ui.show()
    exit(app.exec_())
# ----------------------------------------------------------------
