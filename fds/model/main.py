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

if __name__ == '__main__':

    dataset = pd.read_csv('{}/data/dataset/dataset.csv'.format(PARENT_DIR), names=['text', 'fishing'])
    dataset = preprocessing.remove_spectial_character(dataset)
    dataset['length'] = dataset['text'].apply(lambda x: len(x))
    print(len(dataset))
    dataset = dataset.drop(dataset[dataset['length'] > 4000].index)
    print(len(dataset))
    print('Dataset 분리\n')
    # 데이터 셋 분리
    train = dataset[:4784]
    test = dataset[4784:]

    # print('토큰화 \n')
    # # 토큰화 진행
    train['tokenized'] = train['text(clean)'].apply(preprocessing.tokenizer)
    test['tokenized'] = test['text(clean)'].apply(preprocessing.tokenizer)

    # print('train/val 분리\n')
    # train set test-val 분리
    train, val = train_test_split(train, test_size=0.3, random_state=42)
    train = pd.read_csv('{}/data/dataset/train_ex.csv'.format(PARENT_DIR), names=['text', 'fishing', 'text(clean)', 'tokenized'])
    val = pd.read_csv('{}/data/dataset/val_ex.csv'.format(PARENT_DIR), names=['text', 'fishing', 'text(clean)', 'tokenized'])
    test = pd.read_csv('{}/data/dataset/test_ex.csv'.format(PARENT_DIR), names=['text', 'fishing', 'text(clean)', 'tokenized'])
    print('w2v model load\n')
    bigrams = Phrases(sentences=train.tokenized)
    trigrams = Phrases(sentences=bigrams[train.tokenized])

    N_SPLITS = 5
    EMBEDDING_SIZE = 256

    tri_model = Word2Vec(sentences=trigrams[bigrams[train.tokenized]], vector_size=EMBEDDING_SIZE, window=10, min_count=10, workers=4, sg=1)
    tri_model.wv.save_word2vec_format('w2v_model')
    # tri_model = KeyedVectors.load_word2vec_format('{}/w2v_model'.format(ROOT_DIR))
    print('x data tokenized\n')
    X_data = train.tokenized
    input_length = max(list(map(len, X_data)))

    print('X, pad_sequences\n')
    X = pad_sequences(
        sequences=vectorize_data(X_data, vocab=tri_model.wv.key_to_index),
        maxlen=input_length,
        padding='post'
    )
    y = train['fishing'].values

    print('X_test, X_val pad_sequences\n')
    X_test = pad_sequences(sequences=vectorize_data(test.tokenized, vocab=tri_model.wv.key_to_index), maxlen=input_length, padding='post')
    X_val = pad_sequences(sequences=vectorize_data(val.tokenized, vocab=tri_model.wv.key_to_index), maxlen=input_length, padding='post')
    y_val = val['fishing'].values

    print('build_model\n')
    model_lstm = build_model(embedding_matrix=tri_model.wv.vectors, input_length=X.shape[1])
    early_stopping_callback = keras.callbacks.EarlyStopping(monitor='val_loss', min_delta=0, patience=5, verbose=0, mode='auto')
    model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint('{}/lstm_model.h5'.format(CUR_DIR), verbose=0, save_best_only=True, monitor='val_loss')

    print('trained\n')
    batch_size = 4
    trained = model_lstm.fit(X, y, epochs=30, batch_size=batch_size, validation_data=(X_val, y_val), callbacks=[early_stopping_callback, model_checkpoint_callback])
