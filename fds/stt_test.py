import speech_recognition as sr
import os

# 현재 디렉토리 주소 /fds/crawler
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
# 상위 디렉토리 주소 /fds
PARENT_DIR = os.path.dirname((CUR_DIR))

r = sr.Recognizer()

test = sr.AudioFile(CUR_DIR+'/data/convert/15master.flac')
with test as source:
    audio = r.record(source, offset=30, duration=10)

res = r.recognize_google(audio, language='ko-KR')
print(res)
