from pydub import AudioSegment
from pydub.silence import detect_nonsilent


def nonsilent_parts(input_file):
    # 오디오 파일 로드
    audio = AudioSegment.from_file(input_file)
    min_silence_len = 100
    silence_thresh = -100
    # 소리가 나는 구간 탐지
    nonsilent_ranges = detect_nonsilent(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)
    
    # 소리가 나는 구간 추출
    nonsilent_audio = AudioSegment.empty()
    print(nonsilent_ranges)
    for start, end in nonsilent_ranges:
        nonsilent_audio = audio[start:end]
        

    # 결과 저장
    nonsilent_audio.export(input_file, format="wav")
    print(f"파일이 성공적으로 저장되었습니다: {input_file}")


# 사용 예시
# input_file = "path/to/your/input_file.wav"
# output_file = "path/to/your/output_file.wav"
# extract_nonsilent_parts(input_file, output_file)
