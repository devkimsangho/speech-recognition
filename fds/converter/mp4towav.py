import moviepy.editor as mp
import os

# 현재 디렉토리 주소 /fds/crawler
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname((CUR_DIR))

my_clip = mp.VideoFileClip(r"{}/data/this_voice/2번_3차례 신고된 여성 전화금융사기범 (음성_2).mp4".format(PARENT_DIR))
print(my_clip)

my_clip.audio.write_audiofile(r"{}/data/convert/2번_3차례 신고된 여성 전화금융사기범 (음성_2).mp3".format(PARENT_DIR))
