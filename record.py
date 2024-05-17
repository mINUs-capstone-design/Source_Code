import queue, os, threading
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
    filename = "record.wav"
     # 파일이 존재하지 않으면 새로 생성
    with sf.SoundFile(filename, mode='w', samplerate=SAMPLERATE, subtype='PCM_16', channels=CHANNELS) as file:
        with sd.InputStream(samplerate=SAMPLERATE, device=None, dtype='int16', channels=CHANNELS, callback=complicated_save):
            while recording:
                file.write(q.get())
                print("녹음중")
                


def complicated_save(indata,frames,time,status):
    if status:
        print('status:', status)
        print('data:',indata)
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
    recorder.join()
    print("record stop")

def on_press_z(event):
    if event.name == 'z':
        start()

# 'x' 키를 누르면 녹음 종료
def on_press_x(event):
    if event.name == 'x':
        stop()

# 키 이벤트 핸들러 등록
keyboard.on_press(on_press_z)
keyboard.on_press(on_press_x)

# 프로그램이 종료될 때 키 이벤트 핸들러 제거
keyboard.wait('esc')
keyboard.unhook_all()