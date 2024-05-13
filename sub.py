import sys

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
        self.button_resultnoise.clicked.connect(self.show_noise_result)
        self.button_startrecord.clicked.connect(self.start_record)
        self.button_stoprecord.clicked.connect(self.uiresult)
        self.button_backtoselectsexual.clicked.connect(self.uiselectsexual)
        self.button_backtochecknoise.clicked.connect(self.uichecknoise)
        self.button_backtomain.clicked.connect(self.uimain)
        self.button_rerecord.clicked.connect(self.uiresultnoise)
        self.button_exit.clicked.connect(self.close)
        self.noise = None
        self.dialog = QDialog()
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


    def read_sensor_data(self):  # 사운드 센서값을 불러오는 함수
        while True:
            r = self.spi.xfer2([1, (8 + 0) << 4, 0])
            adc_out = ((r[1] & 3) << 8) + r[2]
            analog_value = adc_out
            if analog_value <= 0:
                analog_value = 1
            db_value = round(20 * math.log10(analog_value), 1)
            time.sleep(0.5)
            return db_value

    def uiresultnoise(self):
        self.selectsexual.hide()
        self.checknoise.hide()
        self.resultnoise.show()
        self.button_stoprecord.hide()
        self.button_startrecord.show()
        self.result.hide()
        self.mainwindow.hide()

    def start_record(self):
        self.button_startrecord.hide()
        self.button_stoprecord.show()
    def uiresult(self):
        self.selectsexual.hide()
        self.checknoise.hide()
        self.resultnoise.hide()
        self.result.show()
        self.mainwindow.hide()

    def show_noise_result(self):
        self.dialog.setWindowTitle("Dialog")
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.resize(300, 200)
        db_value = 5  # 사운드센서 값 불러옴
        self.noise = str(db_value) + "db"
        noiselabel = QLabel(self.dialog)
        noiselabel.move(100, 100)
        noiselabel.setText(self.noise)
        if db_value > 80:
            noiselabel.setStyleSheet("COLOR : red")
        elif db_value <= 80 and db_value > 60:
            noiselabel.setStyleSheet("COLOR : yellow")
        else:
            noiselabel.setStyleSheet("COLOR : green")
        self.dialog.setWindowTitle("소음측정결과")
        self.dialog.show()
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


class SiameseNetworkDataset(Dataset):

    def __init__(self, imageFolderDataset, transform=None, should_invert=False):
        self.imageFolderDataset = imageFolderDataset
        self.transform = transform
        self.should_invert = should_invert

    def __getitem__(self, index):
        img0_tuple = random.choice(self.imageFolderDataset.imgs)

        should_get_same_class = random.randint(0, 1)
        if should_get_same_class:
            while True:

                img1_tuple = random.choice(self.imageFolderDataset.imgs)
                if img0_tuple[1] == img1_tuple[1]:
                    break
        else:
            while True:

                img1_tuple = random.choice(self.imageFolderDataset.imgs)
                if img0_tuple[1] != img1_tuple[1]:
                    break

        img0 = Image.open(img0_tuple[0])
        img1 = Image.open(img1_tuple[0])

        if self.should_invert:
            img0 = PIL.ImageOps.invert(img0)
            img1 = PIL.ImageOps.invert(img1)

        if self.transform is not None:
            img0 = self.transform(img0)
            img1 = self.transform(img1)

        return img0, img1, torch.from_numpy(np.array([int(img1_tuple[1] != img0_tuple[1])], dtype=np.float32))
        # 두 이미지가 서로 다른 클래스면 1
        # 두 이미지가 서로 같은 클래스면 0

    def __len__(self):
        return len(self.imageFolderDataset.imgs)


class SiameseNetwork(nn.Module):
    def __init__(self):
        super(SiameseNetwork, self).__init__()
        self.cnn1 = nn.Sequential(
            nn.ReflectionPad2d(1),  # 가장자리의 특징들까지 고려
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
            nn.Linear(8 * 99 * 250, 500),
            nn.ReLU(inplace=True),

            nn.Linear(500, 500),
            nn.ReLU(inplace=True),

            nn.Linear(500, 5))

    def forward_once(self, x):
        output = self.cnn1(x)
        output = output.view(output.size()[0], -1)  # flatten
        output = self.fc1(output)
        return output

    def forward(self, input1, input2):
        output1 = self.forward_once(input1)
        output2 = self.forward_once(input2)
        return output1, output2


device = "cuda" if torch.cuda.is_available() else "cpu"
model = torch.load("siamese_net_v4.pt", map_location=device)
print(model)

folder_dataset_test = dset.ImageFolder(root=Config.testing_dir)
siamese_dataset = SiameseNetworkDataset(imageFolderDataset=folder_dataset_test,
                                        transform=transforms.Compose([transforms.Resize((99, 250)),
                                                                      transforms.ToTensor()
                                                                      ])
                                        , should_invert=False)

test_dataloader = DataLoader(siamese_dataset, num_workers=0, batch_size=1, shuffle=True)  # 1장씩 test

dataiter = iter(test_dataloader)
# x0,x1,label1 = next(dataiter) # test의 기준이 되는 img.
# 0 : same class , 1 : other class

for i in range(10):
    x0, x1, label1 = next(dataiter)
    concatenated = torch.cat((x0, x1), 0)

    # output1,output2 = model(Variable(x0).cuda(),Variable(x1).cuda())
    output1, output2 = model(Variable(x0), Variable(x1))
    euclidean_distance = F.pairwise_distance(output1, output2)
    imshow(torchvision.utils.make_grid(concatenated),
          'isNotSame : {:.0f}\nDissimilarity: {:.2f}'.format(label1.item(), euclidean_distance.item()))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = WindowClass()
    ui.show()
    exit(app.exec_())