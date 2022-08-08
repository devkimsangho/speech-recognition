import datas
from build_model import build_lstm_model
from vectorize import integer_indexing
from w2v import word2vec_load
import os
import tensorflow as tf
from preprocessing import remove_spectial_character, tokenizer

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
    maxlen = 1582

    print('------- w2v load ------')
    tri_model = word2vec_load('{}/trained/w2v_model_1'.format(CUR_DIR))
    print('------ integer_indexing ------')
    x = integer_indexing(x_data, maxlen, tri_model, 'post')
    print('------model load---------')
    lstm_model = build_lstm_model(tri_model.vectors, x.shape[1])
    lstm_model.load_weights('{}/trained/lstm_model_1.h5'.format(CUR_DIR))
    print('------ predict------')
    pred = lstm_model.predict(x)
    # pred = tf.argmax(pred)
    print(pred)
