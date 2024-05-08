import pyaudio
import wave

MIC_DEVICE_ID = 1

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1

RATE = 16000

SAMPLE_SIZE = 2

def record(record_seconds):
    p = pyaudio.PyAudio()
    stream = p.open(input_device_index=MIC_DEVICE_ID,
                    format=FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    frames_per_buffer=CHUNK)
    frames = []

    for i in range(0,int(RATE / CHUNK * record_seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    return frames