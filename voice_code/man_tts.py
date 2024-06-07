# ----------------------------------------------------------------
from google.cloud import texttospeech
from google.oauth2 import service_account
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# TTS 변환 기능 함수
def run_tts(global_selected_sentence):

    credentials = service_account.Credentials.from_service_account_file('majestic-cairn-422006-c4-adf3cfa75c37.json')

    client = texttospeech.TextToSpeechClient(credentials=credentials)
    
    #text_block = input("텍스트 입력 : ")
    
    synthesis_input = texttospeech.SynthesisInput(text=global_selected_sentence)

    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR",
        name="ko-KR-Wavenet-C",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16, speaking_rate=0.85, sample_rate_hertz = 22050

    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    
    #OUTPUT = input("저장할 파일이름 & 확장자 입력 : ")

    with open("TTS_record.wav", "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "TTS_record.wav"')
# ----------------------------------------------------------------

# ----------------------------------------------------------------
#main문에서 run_tts 함수 실행
if __name__ == "__main__":
    run_tts("집을 가다")
# ----------------------------------------------------------------
