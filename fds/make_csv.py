import os
import pandas as pd

# 현재 디렉토리 주소 /fds/crawler
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
# 부모 디렉토리 주소 /fds/
PARENT_DIR = os.path.dirname((CUR_DIR))

file_list = os.listdir('{}/data/txt'.format(CUR_DIR))

datas = []

for file_name in file_list:
    with open('{}/data/txt/{}'.format(CUR_DIR, file_name), 'r') as f:
        line = f.readline()
        datas.append([line, 1])

df = pd.DataFrame(datas)
df.to_csv('{}/data/dataset/voice_fishing.csv'.format(CUR_DIR), header=None, index=None)
