from pydub import AudioSegment
import os

# 현재 디렉토리 주소 /fds/crawler
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname((CUR_DIR))

sound = AudioSegment.from_file("{}/data/this_voice/15master.mp4".format(PARENT_DIR))
sound.export("{}/data/convert/15master.flac".format(PARENT_DIR), format='flac')
