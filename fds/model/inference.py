import datas
from build_model import build_lstm_model
from vectorize import integer_indexing
from w2v import word2vec_load
import os
import tensorflow as tf
from preprocessing import remove_spectial_character, tokenizer
from attention import Attention
from keras.models import load_model
if __name__ == '__main__':
    # 현재 디렉토리 주소 /fds/crawler
    CUR_DIR = os.path.dirname(os.path.abspath(__file__))
    # 부모 디렉토리 주소 /fds/
    PARENT_DIR = os.path.dirname((CUR_DIR))
    print('------ load data-------')
    data = datas.load_predict_data('{}/data/dataset/test.csv'.format(PARENT_DIR))
    data = remove_spectial_character(data)
    print('------tokenized------')
    data['tokenized'] = data['text(clean)'].apply(tokenizer)
    x_data = data.tokenized
    maxlen = 1179

    print('------- w2v load ------')
    tri_model = word2vec_load('{}/trained/w2v_model'.format(CUR_DIR))
    print('------ integer_indexing ------')
    x = integer_indexing(x_data, maxlen, tri_model, 'post')
    print('------model load---------')
    lstm_model = load_model('{}/trained/lstm_model.h5'.format(CUR_DIR), custom_objects={'Attention': Attention})
    # lstm_model = build_lstm_model(tri_model.vectors, x.shape[1])
    # lstm_model.load_weights('{}/trained/lstm_model_1.h5'.format(CUR_DIR))
    print('------ predict------')
    print(lstm_model.layers[0].input_shape[1])
    pred = lstm_model.predict(x)
    print(pred)
    print('argmax')
    pred = tf.argmax(pred, axis=-1)
    print(pred)
