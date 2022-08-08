from keras_preprocessing.sequence import pad_sequences


def vectorize_data(data, vocab: dict) -> list:
    print('Vectorize sentences...', end='\r')
    keys = list(vocab.keys())
    def filter_unknown(word): return vocab.get(word, None) is not None
    def encode(review): return list(map(keys.index, filter(filter_unknown, review)))
    vectorized = list(map(encode, data))
    print('Vectorie sentence.. (done)')
    return vectorized


def integer_indexing(data, maxlen, tri_model, padding='post'):
    x = pad_sequences(
        sequences=vectorize_data(data, vocab=tri_model.key_to_index),
        maxlen=maxlen,
        padding=padding
    )

    return x
