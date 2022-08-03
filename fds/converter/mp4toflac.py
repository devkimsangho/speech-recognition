from pydub import AudioSegment
import os

# 현재 디렉토리 주소 /fds/crawler
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
# 부모 디렉토리 주소 /fds/
PARENT_DIR = os.path.dirname((CUR_DIR))

file_list = os.listdir('{}/data/this_voice'.format(PARENT_DIR))
print('{} files will be converted...'.format(len(file_list)))
for i in range(len(file_list)):
    file_name = file_list[i]
    print('{} / {} files covert completed...'.format(i+1, len(file_list)), end='\r')
    sound = AudioSegment.from_file("{}/data/this_voice/{}".format(PARENT_DIR, file_name))
    sound.export("{}/data/convert/{}.flac".format(PARENT_DIR, file_name[:-4]), format='flac')
print('')
print('done')
