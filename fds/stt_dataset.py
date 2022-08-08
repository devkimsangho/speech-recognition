import speech_recognition as sr
from pydub import AudioSegment
import os


# 현재 디렉토리 주소 /fds/crawler
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
# 부모 디렉토리 주소 /fds/
PARENT_DIR = os.path.dirname((CUR_DIR))

file_list = os.listdir('{}/data/flac'.format(CUR_DIR))

for file_name in range(1, len(file_list)+1):
    try:
        file_name = str(file_name)
        r = sr.Recognizer()
        audio = AudioSegment.from_file(CUR_DIR+'/data/flac/{}.flac'.format(file_name))
        audio_time = audio.duration_seconds
        tot = 0
        media = sr.AudioFile(CUR_DIR+'/data/flac/{}.flac'.format(file_name))
        res = ""
        with media as source:
            while tot < audio_time:
                if audio_time - tot > 60:
                    a = r.record(source, duration=60)
                    res = res+' '+r.recognize_google(a, language='ko-KR')
                    tot += 60
                else:
                    a = r.record(source)
                    res = res+' '+r.recognize_google(a, language='ko-KR')
                    break

        with open('{}/data/txt/{}.txt'.format(CUR_DIR, file_name), 'w+') as f:
            f.write(res)

        print('{} completed'.format(file_name))
    except sr.UnknownValueError as e:
        print('{}.flac file error'.format(file_name))
        with open('{}/data/error.txt'.format(CUR_DIR), 'a') as f:
            f.write('{}.flac\n'.format(file_name))
        continue
