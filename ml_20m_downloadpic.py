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
    imdbId_list = df['imdbId']
    print imdbId_list
    print type(imdbId_list)
    # print imdbId_list[0]
    imdb = df.imdbId.unique()
    print imdb
    n_imdbId = imdb.shape[0]
    print n_imdbId


read_imdbId()
