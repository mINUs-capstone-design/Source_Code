import pygame
import os

def speak_sentense_tts(file_name):
    audio_directory ="."
    audio_files = list_audio_files(audio_directory)
    chosen_file = choose_audio_file(audio_files,file_name)
    chosen_file_path = os.path.join(audio_directory,chosen_file)
    print(chosen_file_path)
    play_audio(chosen_file_path)

def list_audio_files(directory):
    """지정된 디렉터리에서 오디오 파일 목록을 반환합니다."""
    return [f for f in os.listdir(directory) if f.endswith(('.wav', '.mp3'))]

def choose_audio_file(files,file_name):
    possible_extensions = ['.wav', '.mp3']

    for ext in possible_extensions:
        chosen_file = file_name + ext
        if chosen_file in files:
            print(chosen_file)
            return chosen_file

    return None
def play_audio(file_path):
    pygame.mixer.init()
    # 음성 파일 로드
    print(file_path)
    pygame.mixer.music.load(file_path)
    # 음성 파일 재생
    pygame.mixer.music.play()

    # 음성이 끝날 때까지 기다림
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

if __name__ == "__main__":
    file_name = "record"
    speak_sentense_tts(file_name)
