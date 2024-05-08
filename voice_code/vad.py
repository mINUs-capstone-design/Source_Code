# ----------------------------------------------------------------
import os
import numpy as np
import librosa
import librosa.effects
import librosa.display
import soundfile as sf
import datetime
import glob
import scipy
from scipy.io.wavfile import read
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# 예제 오디오 신호
wav_file_name = glob.glob('*.wav')
recent_file = max(wav_file_name, key=os.path.getmtime)
print(recent_file)

y, sr = librosa.load(recent_file)

# 오디오 신호 자르기
y_trimmed, index = librosa.effects.trim(y, top_db=30)
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# 잘린 신호를 WAV 파일로 저장
current_directory = os.path.dirname(os.path.abspath(__file__))
current_time = datetime.datetime.now().strftime('%Y%m%d_%H-%M-%S')

sf.write('after_VAD_record.wav', y_trimmed, sr)


# 추출 전 원본 음원 파일 삭제
os.remove(recent_file)
print("VAD 실행 후 추출 완료...저장된 이름은 after_VAD_record.wav")
# ----------------------------------------------------------------