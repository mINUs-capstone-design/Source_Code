import io
from google.cloud import speech_v1p1beta1 as speech
from google.oauth2 import service_account
from pydub import AudioSegment

pronunciation_map = {
    "0": "영",
    "1": "일",
    "2": "이",
    "3": "삼",
    "4": "사",
    "5": "오",
    "6": "육",
    "7": "칠",
    "8": "팔",
    "9": "구",
    "10": "십",
    "B": "비",
    "E": "이"

}
#--------------------------------------------------
def transcribe_audio(audio_file_path):
    credentials = service_account.Credentials.from_service_account_file('[].json')
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
        print("Transcript: ",transcript)
        transcript = "".join([pronunciation_map.get(word, word) for word in transcript.split()])
        return transcript


