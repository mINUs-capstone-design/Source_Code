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
def take_vad(wav_file):
    # 녹음된 파일에 VAD 알고리즘을 적용하는 함수

    # 예제 오디오 신호
    wav_file_name = glob.glob('*.wav')
    recent_file = max(wav_file_name, key=os.path.getmtime)

    y, sr = librosa.load(recent_file)

    # 오디오 신호 자르기
    y_trimmed, index = librosa.effects.trim(y, top_db=30)

    # 잘린 신호를 WAV 파일로 저장
    #current_time = datetime.datetime.now().strftime('%Y%m%d_%H-%M-%S')

    voice_code = os.path.dirname(os.path.abspath(__file__))
    source_code = os.path.join(voice_code, "..")
    after_wav_file = os.path.join(source_code, "record_after_vad.wav")

    # VAD 결과를 파일로 저장
    sf.write(after_wav_file, y_trimmed, sr)

    # 원본 녹음 파일 삭제
    #os.remove(wav_file)

    print("VAD 실행 후 추출 완료...")
# ----------------------------------------------------------------
