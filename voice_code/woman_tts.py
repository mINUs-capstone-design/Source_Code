# ----------------------------------------------------------------
from google.cloud import texttospeech
from google.oauth2 import service_account
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# TTS 변환 기능 함수
def run_tts(global_selected_sentence):

    credentials = service_account.Credentials.from_service_account_file('[key].json')

    client = texttospeech.TextToSpeechClient(credentials=credentials)
    
    #text_block = input("텍스트 입력 : ")
    
    synthesis_input = texttospeech.SynthesisInput(text=global_selected_sentence)

    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR",
        name="ko-KR-Standard-A",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(

        audio_encoding=texttospeech.AudioEncoding.LINEAR16, speaking_rate=0.85

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
# main문에서 run_tts 함수 실행
if __name__ == "__main__":
    run_tts()
# ----------------------------------------------------------------
