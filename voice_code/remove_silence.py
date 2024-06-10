from pydub import AudioSegment
from pydub.silence import detect_silence


def remove_after_silence(input_file, silence_duration=300):
    # 오디오 파일 로드
    audio = AudioSegment.from_file(input_file)

    # 무음 구간 탐지 (silence_duration 밀리초 이상인 무음 구간 탐지)
    silence_threshold = -100  # dBFS, 무음으로 간주할 데시벨 수준
    silent_ranges = detect_silence(audio, min_silence_len=silence_duration, silence_thresh=silence_threshold)

    if silent_ranges:
        # 첫 번째 무음 구간의 시작 시간
        first_silence_start = silent_ranges[0][0]

        # 첫 번째 무음 구간까지의 오디오 자르기
        trimmed_audio = audio[:first_silence_start]

        # 결과 저장
        trimmed_audio.export(input_file, format="wav")
        print(f"파일이 성공적으로 저장되었습니다: {input_file}")
    else:
        print("지정된 길이 이상의 무음 구간이 없습니다. 원본 파일을 그대로 사용합니다.")


# 사용 예시
# input_file = "path/to/your/input_file.wav"
# output_file = "path/to/your/output_file.wav"
# remove_after_silence(input_file)
