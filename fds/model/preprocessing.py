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
