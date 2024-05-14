import queue, os, threading
import time

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
                if not recording:
                    break
                data = q.get()
                if data is not None:  # 큐에서 음성 데이터를 가져옴
                    file.write(data)
                print("녹음중")
                


def complicated_save(indata,frames,time,status):
    if status:
        print('status:', status)
    q.put(indata.copy())  

def start():
    global recorder
    global recording
    recording = True
    recorder = threading.Thread(target=complicated_record)
    print("start recording")
    recorder.start()
    

def stop():
    global recording
    recording = False
    
    print("record stop")
