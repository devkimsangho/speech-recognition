import os
import datas
from gensim.models import Word2Vec, Phrases
from gensim.models import KeyedVectors
from preprocessing import remove_spectial_character, tokenizer


# 현재 디렉토리 주소 /fds/crawler
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
# 부모 디렉토리 주소 /fds/
PARENT_DIR = os.path.dirname((CUR_DIR))
ROOT_DIR = os.path.dirname((PARENT_DIR))


def word2vec_load(path):
    tri_model = None
    if os.path.isfile(path):
        tri_model = KeyedVectors.load_word2vec_format(path)
    else:
        print('w2v model is not founded. make model start')
        dataset = datas.load_data('{}/data/dataset/dataset.csv'.format(PARENT_DIR))
        dataset = remove_spectial_character(dataset=dataset)
        dataset['tokenized'] = dataset['text(clean)'].apply(tokenizer)

        bigrams = Phrases(sentences=dataset.tokenized)
        trigrams = Phrases(sentences=bigrams[dataset.tokenized])
        print(dataset.tokenized)
        EMBEDDING_SIZE = 256
        tri_model = Word2Vec(sentences=trigrams[bigrams[dataset.tokenized]], vector_size=EMBEDDING_SIZE, window=10, min_count=5, workers=4, sg=1)
        tri_model.wv.save_word2vec_format(path)
        tri_model = KeyedVectors.load_word2vec_format(path)
    print('w2v load complete')
    return tri_model


if __name__ == '__main__':
    tri_model = word2vec_load('{}/trained/w2v_model'.format(CUR_DIR))
    tri_model.save_word2vec_format('{}/trained/w2v_model'.format(CUR_DIR))
