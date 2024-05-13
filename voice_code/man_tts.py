# ----------------------------------------------------------------
from google.cloud import texttospeech
from google.oauth2 import service_account
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# TTS 변환 기능 함수
def run_tts():

    credentials = service_account.Credentials.from_service_account_file('[keyname].json')

    client = texttospeech.TextToSpeechClient(credentials=credentials)
    
    text_block = input("텍스트 입력 : ")
    
    synthesis_input = texttospeech.SynthesisInput(text=text_block)

    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR",
        name="ko-KR-Standard-C",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    
    OUTPUT = input("저장할 파일이름 & 확장자 입력 : ")
    
    with open(OUTPUT, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{OUTPUT}"')
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# main문에서 run_tts 함수 실행
if __name__ == "__main__":
    run_tts()
# ----------------------------------------------------------------