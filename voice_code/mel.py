# ----------------------------------------------------------------
import os
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import glob
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# 디렉토리 내의 .wav 파일 목록 가져오기
def get_wav_files(directory):
    wav_files = []
    for file in os.listdir(directory):
        if file.endswith(".wav"):
            wav_files.append(os.path.join(directory, file))
    return wav_files
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# 현재 실행 중인 파일의 경로
current_directory = os.path.dirname(os.path.abspath(__file__))

# 경로 내 .wav 파일 목록 가져오기
wav_files = get_wav_files('.')
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# 디렉토리 내 .png 파일 삭제 함수
def delete_old_png_file():
    png_files = [file for file in os.listdir(current_directory) if file.endswith(".jpg")]
    if len(png_files) >= 6:
        oldest_file = min(png_files, key=os.path.getctime)
        os.remove(os.path.join(current_directory, oldest_file))
        print(f"기존 '{oldest_file}' 파일 삭제")
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# 이미지 변환 함수
def change_picture():
    output_dir = '.'
    
    # 이미지 읽어오기
    images = [file for file in os.listdir(current_directory) if file.endswith(".png")]
    cnt = 1
    
    # 이미지를 순회하며 작업 수행
    for img in images:
        img = img.convert("RGB")
        img.save(os.path.join(output_dir, f'c{cnt}.jpg'))
        cnt+=1
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# 각 .wav 파일을 불러와서 처리
for audio_file in wav_files:
    # 오디오 데이터 읽어오기
    y, sr = librosa.load(audio_file)

    # Mel-spectrogram 계산
    mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)
    
    # Mel-spectrogram을 데시벨로 변환
    mel_spectrogram_db = librosa.power_to_db(mel_spectrogram, ref=np.max)
    
    # Mel-spectrogram 플로팅
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(mel_spectrogram_db, sr=sr, x_axis='time', y_axis='mel')
    
    # plot 그래프 이미지만 나타내기
    plt.yticks(ticks=[])  # y축 tick 제거
    plt.xticks(ticks=[])  # x축 tick 제거
    
    # # x축, y축 각각 눈금 & 테두리 제거
    plt.gca().axes.get_xaxis().set_visible(False)
    plt.gca().axes.get_yaxis().set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    # 제목과 컬러바(색상표시바) 제거
    plt.title('')
    plt.colorbar().remove()
    
    # 그래프 영역에 맞게 이미지 크기 조정
    plt.tight_layout()
    
    # 그래프 영역에 맞게 이미지 크기 조정
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    
    # 축 비활성화하여 그래프 내용만 자르기
    plt.axis('off')

    # 이미지 저장
    output_filename = f"Mel_{os.path.splitext(os.path.basename(audio_file))[0]}.jpg"
    plt.savefig(output_filename, bbox_inches='tight', pad_inches=0)
    
    # 플롯 닫기
    plt.close()
    print("플롯이미지 생성 종료")
    
    # 이미지 파일 삭제 함수 호출
    delete_old_png_file()
    print("이미지 삭제 종료")
    
    # 이미지 변환 함수 호출
    change_picture()
    print("이미지 변환 완료")
# ----------------------------------------------------------------