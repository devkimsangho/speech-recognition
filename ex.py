import re
import pandas as pd
import os

from fds.model.preprocessing import remove_spectial_character
# 현재 디렉토리 주소 /fds/crawler
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
# 부모 디렉토리 주소 /fds/
PARENT_DIR = os.path.dirname((CUR_DIR))

dataset = pd.read_csv('{}/fds/data/dataset/dataset.csv'.format(CUR_DIR), names=['text', 'fishing'])
dataset = remove_spectial_character(dataset)
print(dataset)
