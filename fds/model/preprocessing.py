from email import header
from konlpy.tag import Okt
import pandas as pd
import datas
import os


def remove_spectial_character(dataset):
    """한글과 공백을 제외한 문자 제거"""
    dataset['text(clean)'] = dataset['text'].str.replace('[^가-힣\s]+', ' ')
    dataset['text(clean)'] = dataset['text(clean)'].str.replace('  ', ' ')

    return dataset


def tokenizer(data, pos=['Noun', 'Verb', 'Adjective', 'Adverb'], stopword=['ㄱ', 'ㄴ,', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ', 'ㅏ', 'ㅑ', 'ㅓ', 'ㅕ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', 'ㅣ', '가', '나', '다', '라', '마', '바', '사', '아', '자', '차', '카', '타', '파', '하', '가가', '듀']):
    """ 문장 토큰화"""
    okt = Okt()
    tokened = okt.pos(data)

    return [word for word, tag in tokened if tag in pos and word not in stopword]


if __name__ == '__main__':
    # 현재 디렉토리 주소 /fds/crawler
    CUR_DIR = os.path.dirname(os.path.abspath(__file__))
    # 부모 디렉토리 주소 /fds/
    PARENT_DIR = os.path.dirname((CUR_DIR))

    dataset = datas.load_data('{}/data/dataset/dataset.csv'.format(PARENT_DIR))
    outlier = datas.get_outlier(dataset)
    print(outlier)
    dataset = datas.remove_some_dataset(dataset=dataset, under=0, over=outlier['fishing'][1])
    dataset = remove_spectial_character(dataset=dataset)
    dataset['tokenized'] = dataset['text(clean)'].apply(tokenizer)
    result = pd.DataFrame(dataset)
    result.to_csv('{}/data/dataset/dataset2.csv'.format(PARENT_DIR), header=None, index=None)
    print('Preprocess complete. Check Your Directory {}/data/dataset/'.format(PARENT_DIR))
