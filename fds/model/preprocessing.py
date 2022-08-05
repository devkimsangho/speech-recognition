from konlpy.tag import Okt


# 구두점과 특수문자 제거
def remove_spectial_character(dataset):
    dataset['text(clean)'] = dataset['text'].str.replace('[\\WX]', ' ')

    return dataset


# 문장 토큰화
def tokenizer(data, pos=['Noun', 'Verb', 'Adjective', 'Adverb'], stopword=['ㄱ', 'ㄴ,', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ', 'ㅏ', 'ㅑ', 'ㅓ', 'ㅕ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', 'ㅣ', '가', '나', '다', '라', '마', '바', '사', '아', '자', '차', '카', '타', '파', '하', '가가', '듀']
              ):
    okt = Okt()
    tokened = okt.pos(data)

    return [word for word, tag in tokened if tag in pos and word not in stopword]

# .str.replace(' ', '')
