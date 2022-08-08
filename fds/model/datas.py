# 데이터 전처리
import pandas as pd
import numpy as np


def load_data(path):
    """전처리 되지 않은 데이터 load"""
    dataset = pd.read_csv(path, names=['text', 'fishing'])
    dataset['length'] = dataset['text'].apply(lambda x: len(x))

    return dataset


def load_predict_data(path):
    """예측을 위한 데이터 load"""
    data = pd.read_csv(path, names=['text'])
    data['length'] = data['text'].apply(lambda x: len(x))
    return data


def remove_some_dataset(dataset, under=0, over=None):
    if under > 0:
        dataset = dataset.drop(dataset[dataset['length'] < under].index)
    if over is not None:
        dataset = dataset.drop(dataset[dataset['length'] > over].index)
    return dataset


def get_outlier(dataset):
    fishing = dataset[dataset['fishing'] == 1]
    normal = dataset[dataset['fishing'] == 0]
    outlier = dict()
    outlier['all'] = (np.percentile(dataset['length'], 5), np.percentile(dataset['length'], 95))
    outlier['fishing'] = (np.percentile(fishing['length'], 5), np.percentile(fishing['length'], 95))
    outlier['normal'] = (np.percentile(normal['length'], 5), np.percentile(normal['length'], 95))
    return outlier
