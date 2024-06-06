import io
from google.cloud import speech_v1p1beta1 as speech
from google.oauth2 import service_account
from pydub import AudioSegment

pronunciation_map = {
    "영": "영",
    "일": "일",
    "이": "이",
    "삼": "삼",
    "사": "사",
    "오": "오",
    "육": "육",
    "칠": "칠",
    "팔": "팔",
    "구": "구",
    "십": "십",
    "공": "공",
    "하나": "하나",
    "둘": "둘",
    "셋": "셋",
    "넷": "넷",
    "다섯": "다섯",
    "여섯": "여섯",
    "일곱": "일곱",
    "여덟": "여덟",
    "아홉": "아홉",
    "열": "열",
}
#--------------------------------------------------
def transcribe_audio(audio_file_path):
    credentials = service_account.Credentials.from_service_account_file('speech-to-text-425408-a797567b8e72.json')
    client = speech.SpeechClient(credentials=credentials)

    # pydub를 사용하여 오디오 파일을 불러오고 WAV 형식으로 변환
    audio = AudioSegment.from_file(audio_file_path)
    audio = audio.set_channels(1)  # Mono 채널로 변환
    audio = audio.set_frame_rate(22050)  # 샘플 레이트를 16000Hz로 설정 (필요에 따라 변경 가능)

    # 메모리 내에서 바이너리 데이터로 변환
    audio_buffer = io.BytesIO()
    audio.export(audio_buffer, format="wav")
    audio_buffer.seek(0)
    content = audio_buffer.read()

    recognition_audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=22050,
        language_code="ko-KR",
    )

    response = client.recognize(config=config, audio=recognition_audio)

    for result in response.results:
        transcript = result.alternatives[0].transcript.strip()
        print("Transcript: {}",transcript)
        transcript = "".join([pronunciation_map.get(word, word) for word in transcript.split()])
        return transcript

# 예제로 사용할 오디오 파일의 경로
# audio_file_path = "record.wav"
#
# transcribe_audio(audio_file_path)
