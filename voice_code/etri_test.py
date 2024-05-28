import urllib3
import json
import base64
# openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/Pronunciation" # 영어
openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/PronunciationKor" # 한국어

accessKey = "767a5874-a73e-40df-ae2c-2557c512c2e5"
audioFilePath = "api_test/김치.wav"
languageCode = "korean"
script = "김치"


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
    headers={"Content-Type": "application/json; charset=UTF-8","Authorization": accessKey},
    body=json.dumps(requestJson)
)

print("[responseCode] " + str(response.status))
print("[responBody]")
print(str(response.data,"utf-8"))