# 데이터 전처리
from email import header
import pandas as pd
from keras_preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split

# lstm_model
from keras.layers import *
import keras
from keras.layers import Dense, Embedding, LSTM, Bidirectional, Concatenate, BatchNormalization, Dropout


# Word2Vec model
from gensim.models import KeyedVectors

from keras.callbacks import *


# function and Class
import os

from build_model_f import build_model
import preprocessing
from vectorize_data_f import vectorize_data
from gensim.models import Word2Vec, Phrases

# 현재 디렉토리 주소 /fds/crawler
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
# 부모 디렉토리 주소 /fds/
PARENT_DIR = os.path.dirname((CUR_DIR))
ROOT_DIR = os.path.dirname((PARENT_DIR))
