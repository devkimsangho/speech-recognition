# 데이터 전처리
import numpy as np

# lstm_model
from keras.layers import *
from keras import optimizers
import keras
from keras.layers import Dense, Embedding, LSTM, Bidirectional, Concatenate, BatchNormalization, Dropout
from keras.callbacks import *
from Attention_c import Attention


def build_model(embedding_matrix: np.ndarray, input_length: int):
    model = keras.Sequential()

    model.add(Embedding(input_dim=embedding_matrix.shape[0], output_dim=embedding_matrix.shape[1], input_length=input_length, weights=[embedding_matrix], trainable=False))
    # 양방향 LSTM 층
    model.add(Bidirectional(LSTM(128, dropout=0.2, recurrent_activation='sigmoid', recurrent_dropout=0, return_sequences=True)))
    model.add(Attention(input_length))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='tanh'))
    model.add(Dropout(0.4))
    model.add(Dense(32, activation='tanh'))
    model.add(Dropout(0.4))

    model.add(Dense(2, activation='Softmax'))
    adam = optimizers.Adam(learning_rate=0.001, amsgrad=True)
    model.compile(loss='sparse_categorical_crossentropy', optimizer=adam, metrics=['accuracy'])
    model.summary()
    return model
