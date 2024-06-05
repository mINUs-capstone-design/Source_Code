import urllib3
import json
import base64
# openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/Pronunciation" # 영어


def score_etri(text):
    openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/PronunciationKor"  # 한국어

    accessKey = "d27cbccd-0b46-4fb9-8f93-77d391e3dd52"
    audioFilePath = "VAD_record.wav"
    languageCode = "korean"
    script = text

    file = open(audioFilePath, "rb")
    audioContents = base64.b64encode(file.read()).decode("utf8")
    file.close()

    requestJson = {
        "argument": {
            "language_code": languageCode,
            "script": script,
            "audio": audioContents
        }
    }

    http = urllib3.PoolManager()
    response = http.request(
        "POST",
        openApiURL,
        headers={"Content-Type": "application/json; charset=UTF-8", "Authorization": accessKey},
        body=json.dumps(requestJson)
    )

    print("[responseCode] " + str(response.status))
    print("[responBody]")
    print(str(response.data, "utf-8"))
    response_dict = json.loads(response.data)
    score = float(response_dict['return_object']['score'])
    print("etri score : ",score)
    return score


score_etri("김밥")