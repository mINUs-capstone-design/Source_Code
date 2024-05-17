import pygame

def speak_sentense_tts(select_sentense):
    # 초기화
    pygame.mixer.init()
    # 음성 파일 로드
    pygame.mixer.music.load(select_sentense)
    # 음성 파일 재생
    pygame.mixer.music.play()

    # 음성이 끝날 때까지 기다림
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
