# ----------------------------------------------------------------
import os
import sys
import spidev
import io
import time,math
from PyQt5 import uic
from PyQt5.QtGui import QColor, QMovie, QFont
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import speak_tts


import torchvision.transforms as transforms
from PIL import Image
import torch
import torch.nn as nn
import torch.nn.functional as F

from pydub import AudioSegment

import random

# 추가...voice_code의 vad.py, mel.py
from voice_code import preprocessing, man_tts, woman_tts, noise_filter, opencv_ccoeff
import record

form_class = uic.loadUiType("./sub.ui")[0]

# ----------------------------------------------------------------


# 추가) random word 전역변수 설정 부분
# =======================================================
global_selected_sentence = ""
# =======================================================


# ----------------------------------------------------------------


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.checknoise.setHidden(True)
        self.selectsexual.setHidden(True)
        self.resultnoise.setHidden(True)
        self.result.setHidden(True)
        # button 기능 함수
        self.button_selectsexual.clicked.connect(self.uiselectsexual)
        #elf.button_startchecknoise.clicked.connect(self.uichecknoise)
        self.button_resultnoise.clicked.connect(self.uiresultnoise)
        #self.button_resultnoise.clicked.connect(self.show_noise_result)
        self.button_startrecord.clicked.connect(self.start_record)
        self.button_stoprecord.clicked.connect(self.uiloading)

        self.button_backtoselectsexual.clicked.connect(self.uiselectsexual)
        self.button_backtochecknoise.clicked.connect(self.uichecknoise)
        self.button_backtomain.clicked.connect(self.uimain)
        self.button_rerecord.clicked.connect(self.restart_record)
        self.button_exit.clicked.connect(self.end_function)

        self.checked_man =False
        self.checked_woman = False
        self.buttongroup_sexual = QButtonGroup(self)
        self.buttongroup_sexual.addButton(self.check_man, 1)
        self.buttongroup_sexual.addButton(self.check_woman, 2)
        self.buttongroup_sexual.setExclusive(True)
        
        self.check_man.clicked.connect(self.button_checked_man)
        self.check_woman.clicked.connect(self.button_checked_woman)
        

        self.button_speak_sentense.clicked.connect(self.speak_sentense_word)
        self.spi = spidev.SpiDev()
        self.spi.open(0,0)
        self.spi.max_speed_hz = 1350000
        
        
        self.timer = QTimer(self)
        
        
    def button_checked_man(self):
        self.checked_man = not self.checked_man
        if self.checked_man:
            self.check_man.setStyleSheet("border-image: url(./icons/checked_man.png);")
            self.check_woman.setStyleSheet("border-image: url(./icons/unchecked_woman.png);")
            self.uichecknoise()
            if self.checked_woman:
                self.checked_woman = not self.checked_woman
        else:
            self.check_man.setStyleSheet("border-image: url(./icons/unchecked_man.png);")
            self.check_woman.setStyleSheet("border-image: url(./icons/unchecked_woman.png);")
        

    def button_checked_woman(self):
        self.checked_woman = not self.checked_woman
        if self.checked_woman:
            self.check_man.setStyleSheet("border-image: url(./icons/unchecked_man.png);")
            self.check_woman.setStyleSheet("border-image: url(./icons/checked_woman.png);")
            self.uichecknoise()
            if self.checked_man:
                self.checked_man = not self.checked_man
        else:
            self.check_man.setStyleSheet("border-image: url(./icons/unchecked_man.png);")
            self.check_woman.setStyleSheet("border-image: url(./icons/unchecked_woman.png);")
        


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

    def select_random_word(self):
        
        # =======================================================
        # 추가) 전역변수 설정 : 랜덤선택된 단어 -> TTS에서 사용
        global global_selected_sentence
        # =======================================================
        
        # 파일에서 단어 리스트 읽어오기
        # 리스트로 변환 (=한 줄씩 단어로 인식)
        # 단어 리스트 중 랜덤하게 선택
        f = io.open('words_list.txt', 'r', encoding='utf-8')
        words_list = f.readlines()
        random_word = random.choice(words_list).strip()
        global_selected_sentence = random_word
        return random_word

    def uichecknoise(self):
        self.selectsexual.hide()
        self.checknoise.show()
        self.resultnoise.hide()
        self.result.hide()
        self.mainwindow.hide()


        self.selected_sentense = self.select_random_word()

        #self.given_sentense.setText(self.selected_sentense)  # 단어리스트 랜덤하게 뽑아와서 넣으면 완료
        self.given_sentense.setAlignment(Qt.AlignCenter)
        
    def read_sensor_data(self):
        #사운드 센서값을 불러오는 함수
        while True:
            r = self.spi.xfer2([1, (8 + 0) << 4, 0])
            adc_out = ((r[1] & 3) << 8) + r[2]
            analog_value = adc_out
            if analog_value <= 0:
                analog_value = 1
            db_value = round(20 * math.log10(analog_value), 1)
            time.sleep(0.5)
            print("db_value = ",db_value)
            return db_value
    
   
    def uiresultnoise(self):
        self.selectsexual.hide()
        self.checknoise.hide()
        self.resultnoise.show()
        self.button_stoprecord.hide()
        self.button_startrecord.show()
        self.result.hide()
        self.mainwindow.hide()
        self.select_word.setFontPointSize(20)
        self.select_word.setText(self.selected_sentense) #제시된 단어 적기
        self.select_word.setAlignment(Qt.AlignCenter)
        db_value =  self.read_sensor_data()  # 사운드센서 값 불러옴
        noise = str(db_value) + "db"
        if db_value > 20:
            self.present_db.setTextColor(QColor("Red"))
        elif db_value <= 20 and db_value > 10:
            self.present_db.setTextColor(QColor("Orange"))
        else:
            self.present_db.setTextColor(QColor("Green"))
        self.present_db.setText(noise)
        self.present_db.setAlignment(Qt.AlignCenter)
        if self.checked_man:
            print("man 불러오기 완료")
            man_tts.run_tts(global_selected_sentence)
        elif self.checked_woman:
            print("woman 불러오기 완료")
            woman_tts.run_tts(global_selected_sentence)

    def speak_sentense_word(self):
        file_name = "TTS_record"
        speak_tts.speak_sentense_tts(file_name)
    # 녹음시작
    def start_record(self):
        print(self.read_sensor_data())
        self.button_startrecord.hide()
        self.button_stoprecord.show()
        record.start()

    # 녹음종료
    def uiresult(self):
        self.selectsexual.hide()
        self.checknoise.hide()
        self.resultnoise.hide()
        self.mainwindow.hide()
        self.result.show()

    def uiloading(self):
        record.stop()
        # 유사도 측정을 녹음 후에 실행하기
        # 맨위에 __init__ 부분에 이어붙이면, 녹음 전에 먼저 실행됨...
        QTimer.singleShot(1000,self.vad_mel_test)

    def vad_mel_test(self):
        # 녹음 후 생긴 record.wav, tts에 VAD, MEL 적용
        preprocessing.wav_to_mel()
        self.similar_test()

    # 유사도 측정 함수
    def similar_test(self):
        # # 측정...
        x0 = "Mel_VAD_record.jpg"
        x1 = "Mel_VAD_TTS_record.jpg"
        #모델 불러오기
        model = prepare_model()
        # 비교하려는 이미지(.jpg)들의 경로
        opencv_score = opencv_ccoeff.compare_image(x0,x1)
        if opencv_score == 1 or opencv_score < 0:
            self.similar_score_text.setTextColor(QColor("Red"))
            self.similar_score_text.setFont(QFont('Arial', 10, QFont.Bold))
            self.similar_score_text.setFontPointSize(20)
            self.similar_score_text.setText(f"측정 불가")
        else:
            # x0 : 사용자가 녹음한 음성데이터의 Mel 이미지
            # x1 : 기준이 되는 TTS 음성데이터의 Mel 이미지
            x0_image = Image.open(x0)
            x1_image = Image.open(x1)
        
            convert_tensor = transforms.Compose([transforms.Resize((190,256)),transforms.ToTensor()])
            x0_image = convert_tensor(x0_image).unsqueeze(0)
            x1_image = convert_tensor(x1_image).unsqueeze(0)

            output1, output2 = model(x0_image, x1_image)
            euclidean_distance = F.pairwise_distance(output1,output2)

            siamese_similar_score = getScore(euclidean_distance.item())


            final_score = finalScore(opencv_score,siamese_similar_score)
            #length_final_score = get_length_change("VAD_record.wav","VAD_TTS_record.wav")*final_score
            print(siamese_similar_score)
            # print(final_score)

            # 유사도 측정 결과를 pyqt5 위젯에 표시...터미널X
            #print(f"score : {getScore(euclidean_distance.item())}")
        
            # 기존에 "유사도 안내 : 90%" 라고 출력하던 곳에 결과 출력
            # self.[].setText() 함수 이용
            # ex) self.text_label.setText('hello world') 형태...self는 함수에서 써야 함
            # f"" 안에 띄어쓰기 -> 위젯에서 가운데에 표시하려고 함 (앞에 8칸 띄기)
            if final_score < 33:
                self.similar_score_text.setTextColor(QColor("Red"))
            elif final_score >=33 and final_score < 66:
                self.similar_score_text.setTextColor(QColor("Orange"))
            else:
                self.similar_score_text.setTextColor(QColor("Green"))
            self.similar_score_text.setFont(QFont('Arial', 10, QFont.Bold))
            self.similar_score_text.setFontPointSize(20)
            self.similar_score_text.setText(f"유사도 안내 : {final_score}%")
        self.similar_score_text.setAlignment(Qt.AlignCenter)
        self.similar_score_text.setStyleSheet("background-color: rgba(255, 255, 255, 0); border: 1px solid black; border-radius: 10px;")
        self.uiresult()
    
    
    def show_noise_result(self):
        self.dialog.setWindowTitle("Dialog")
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.resize(300, 200)
        # db_value = self.read_sensor_data()  # 사운드센서 값 불러옴
        db_value = 30
        noise = str(db_value) + "db"
        self.noiselabel.move(30, 80)
        if db_value > 40:
            self.noiselabel.setAlignment(Qt.AlignCenter)
            self.noiselanel.setText("주변의 소음이 심합니다. 측정결과가 부정확합니다.")
            self.noiselabel.setStyleSheet("COLOR : red")
        elif db_value <= 40 and db_value > 20:
            self.noiselabel.setText("주변에 약간의 소음이 있습니다. 주의해주세요")
            self.noiselabel.setStyleSheet("COLOR : Orange")
        else:
            self.noiselabel.setText("테스트하기에 적당한 소음입니다. 녹음을 진행해주세요.")
            self.noiselabel.setStyleSheet("COLOR : green")
        self.dialog.setWindowTitle("소음측정결과")
        self.dialog.exec()

    def end_function(self):
        [os.remove(os.path.join('.', filename)) for filename in os.listdir('.') if filename.endswith('.wav')]
        [os.remove(os.path.join('.', filename)) for filename in os.listdir('.') if filename.endswith('.jpg')]
        self.close()
        
    def restart_record(self):
        [os.remove(os.path.join('.', filename)) for filename in os.listdir('.') if filename.endswith('.wav')]
        [os.remove(os.path.join('.', filename)) for filename in os.listdir('.') if filename.endswith('.jpg')]
        self.uiresultnoise()
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

def finalScore(opencv_score,siames_score):
    
    opencv_score = opencv_score*100
    opencv_score = round(opencv_score)
    final_score = opencv_score*0.5 + siames_score *0.5
    final_score = round(final_score)
    return final_score

def get_length_change(base,voice):
    # input : 두 음성데이터의 길이
    # output : 1~5점
    def get_fluency(base, target):
        score = 1
        distance = base - target
        ratio = abs((distance / base) * 100)
        if distance >= 0:
            if ratio <= 25:
                score = 5
            elif ratio <= 35:
                score = 4
            elif ratio <= 50:
                score = 3
            elif ratio <= 60:
                score = 2
            else:
                score = 1
        else:
            if ratio <= 10:
                score = 5
            elif ratio <= 15:
                score = 4
            elif ratio <= 20:
                score = 3
            elif ratio <= 25:
                score = 2
            else:
                score = 1


    # 오디오 파일 load
    base_audio = AudioSegment.from_file(base)
    voice_audio = AudioSegment.from_file(voice)

    # 단위 : ms
    base_length = len(base_audio)
    voice_length = len(voice_audio)

    # print(get_fluency(base_length, voice_length))
    # return get_fluency(base_length,voice_length)
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
            nn.Linear(8*190*256, 500),
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

def prepare_model():
    # 측정...
    device = "cpu"
    # 모델 이름 경로
    model = torch.load("siamese_net_r1.pt", map_location=device)
    return model
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
