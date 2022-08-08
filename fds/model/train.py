from build_model import build_lstm_model
import tensorflow as tf
import keras
from keras.callbacks import EarlyStopping
from w2v import word2vec_load
import os
import datas
import pandas as pd
from vectorize import vectorize_data, integer_indexing


def model_train(X, y, X_val, y_val, tri_model, batch_size, path):
    model_lstm = build_lstm_model(embedding_matrix=tri_model.vectors, input_length=X.shape[1])
    early_stopping_callback = EarlyStopping(monitor='val_loss', min_delta=0, patience=5, verbose=0, mode='auto')
    model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(path, verbose=0, save_best_only=True, monitor='val_loss')
    trained = model_lstm.fit(X, y, epochs=30, batch_size=batch_size, validation_data=(X_val, y_val), callbacks=[early_stopping_callback, model_checkpoint_callback])
    return trained


if __name__ == '__main__':
    # 현재 디렉토리 주소 /fds/crawler
    CUR_DIR = os.path.dirname(os.path.abspath(__file__))
    # 부모 디렉토리 주소 /fds/
    PARENT_DIR = os.path.dirname((CUR_DIR))

    tri_model = word2vec_load('{}/trained/w2v_model'.format(CUR_DIR))
    print('padding')
    # 정수 패딩
    dataset = datas.load_data('{}/data/dataset/dataset.csv'.format(PARENT_DIR))
    fishings = dataset[dataset['fishing'] == 1]
    normals = dataset[dataset['fishing'] == 0]
    train_fishings = fishings[:len(fishings)//3]
    val_fishings = fishings[len(fishings)//3:2*len(fishings)//3]
    test_fishings = fishings[2*len(fishings)//3:]
    train_normals = normals[:len(normals)//3]
    val_normals = normals[len(normals)//3:2*len(normals)//3]
    test_normals = normals[2*len(normals)//3:]

    print('split')
    train = pd.concat([train_fishings, train_normals], ignore_index=True)
    train = train.sample(frac=1).reset_index(drop=True)

    val = pd.concat([val_fishings, val_normals], ignore_index=True)
    val = val.sample(frac=1).reset_index(drop=True)

    test = pd.concat([test_fishings, test_normals], ignore_index=True)
    test = test.sample(frac=1).reset_index(drop=True)

    print('tokenized')
    X_data = train.tokenized
    input_length = max(list(map(len, X_data)))

    print('integer indexing')
    X = integer_indexing(data=X_data, maxlen=input_length, tri_model=tri_model, padding='post')
    y = train['fishing'].values

    X_val = integer_indexing(data=val.tokenized, maxlen=input_length, tri_model=tri_model, padding='post')

    y_val = val['fishing'].values

    X_test = integer_indexing(data=test.tokenized, maxlen=input_length, tri_model=tri_model, padding='post')

    print('build model')
    model = build_lstm_model(embedding_matrix=tri_model.vectors, input_length=X.shape[1])
    batch_size = 32
    print('trained')
    trained = model_train(X, y, X_val, y_val, tri_model, batch_size=batch_size, path='{}/trained/lstm_model.h5'.format(CUR_DIR))
