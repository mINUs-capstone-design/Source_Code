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
    with sf.SoundFile("/record.wav",mode='w',samplerate=SAMPLERATE,subtype='PCM_16',channels=CHANNELS) as file:
        with sd.InputStream(samplerate=SAMPLERATE,dtype='int16',channels=CHANNELS,callback=complicated_record()):
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

start()
time.sleep(3)
stop()