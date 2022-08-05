def vectorize_data(data, vocab: dict) -> list:
    print('Vectorize sentences...', end='\r')
    keys = list(vocab.keys())
    def filter_unknown(word): return vocab.get(word, None) is not None
    def encode(review): return list(map(keys.index, filter(filter_unknown, review)))
    vectorized = list(map(encode, data))
    print('Vectorie sentence.. (done)')
    return vectorized
