import os
import subprocess

# []_tts.py 실행
print("TTS 작동 중")
subprocess.run(["python", "man_tts.py"])

# vad.py 실행
print("VAD 작동 중")
subprocess.run(["python", "vad.py"])

# mel_wav.py 실행
print("Mel spectrogram 작동 중")
subprocess.run(["python", "mel.py"])

print("실행 종료")