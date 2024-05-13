import queue, os, threading
import time
import keyboard

import sounddevice as sd
import soundfile as sf
from scipy.io.wavfile import write

SAMPLERATE = 16000
CHANNELS = 1
q = queue.Queue()
recorder = False
recording = False

def complicated_record():
    filename = "./record.wav"
     # 파일이 존재하지 않으면 새로 생성
    with sf.SoundFile(filename, mode='w', samplerate=SAMPLERATE, subtype='PCM_16', channels=CHANNELS) as file:
        with sd.InputStream(samplerate=SAMPLERATE, dtype='int16', channels=CHANNELS, callback=complicated_save):
            while recording:
                file.write(q.get())


def complicated_save(indata,frames,time,status):
    q.put(indata.copy())

def start():
    global recorder
    global recording
    recording = True
    recorder = threading.Thread(target=complicated_record)
    print("start recording")
    recorder.start()

def stop():
    global recorder
    global recording
    recording = False
    recorder.join()
    print("record stop")


def on_press_z(event):
    if event.name == 'z':
        start()
def on_press_x(event):
    if event.name == 'x':
        stop()

keyboard.on_press(on_press_z)
keyboard.on_press(on_press_x)