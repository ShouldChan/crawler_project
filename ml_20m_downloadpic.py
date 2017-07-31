# coding:utf-8
pic_dir = './ml_20m_posters/'
mv_dir = './ml_20m/'
basis_font = 'http://www.imdb.com/title/tt'
basis_back = '/mediaindex?refine=poster&ref_=ttmi_ref_pos'

import requests
import time
import pandas as pd


# read imdbId to download the pics
def read_imdbId():
    header = ['movieId', 'imdbId', 'tmdbId']
    df = pd.read_csv(mv_dir + 'links.csv', names=header)
    movieId_series = df['movieId']
    imdbId_series = df['imdbId']
    # print imdbId_series
    print movieId_series
    # print type(imdbId_series)
    # print type(movieId_series)
    # print movieId_series[0]
    # print imdbId_series[0]
    imdb = df.imdbId.unique()
    movie = df.movieId.unique()
    # print imdb
    # n_imdbId-1 为imdbId的个数，即电影的个数
    n_imdbId = imdb.shape[0]
    n_movieId = movie.shape[0]
    if n_imdbId == n_movieId:
        n_imdbId = n_imdbId - 1
        print 'the number of movie id:\t', str(n_imdbId)
    # print n_imdbId

    return imdbId_series, n_imdbId


def extract_posters(imdbid_series, n_imdbid):
    print 'asdasd'


if __name__ == '__main__':
    imdbid_series, n_imdbid = read_imdbId()
    print imdbid_series, n_imdbid
