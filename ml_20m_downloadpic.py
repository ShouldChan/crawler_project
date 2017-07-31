# coding:utf-8
pic_dir = './ml_20m_posters/'
mv_dir = './ml_20m/'

import requests
import time
import pandas as pd


# read imdbId to download the pics
def read_imdbId():
    header = ['movieId', 'imdbId', 'tmdbId']
    df = pd.read_csv(mv_dir + 'links.csv', names=header)
    imdbId_series = df['imdbId']
    # print imdbId_series
    print type(imdbId_series)
    # print imdbId_list[0]
    imdb = df.imdbId.unique()
    # print imdb
    # n_imdbId-1 为imdbId的个数，即电影的个数
    n_imdbId = imdb.shape[0]
    # print n_imdbId

    return imdbId_series, n_imdbId


if __name__ == '__main__':
    imdbid_series, n_imdbid = read_imdbId()
    print imdbid_series,n_imdbid
