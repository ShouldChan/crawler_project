# coding:utf-8
pic_dir = './ml_20m_frames/'
mv_dir = './ml_20m/'
basis_font = 'http://www.imdb.com/title/tt'
basis_back = '/mediaindex?refine=still_frame&ref_=ttmi_ref_sf'

import pandas as pd
import re
import urllib2
from bs4 import BeautifulSoup
import urllib
import os
import time


# read imdbId to download the pictures
def read_imdbId():
    header = ['movieId', 'imdbId', 'tmdbId']
    df = pd.read_csv(mv_dir + 'links.csv', names=header)
    movieId_series = df['movieId']
    imdbId_series = df['imdbId']
    print movieId_series
    imdb = df.imdbId.unique()
    movie = df.movieId.unique()
    # n_imdbId-1 为imdbId的个数，即电影的个数
    n_imdbId = imdb.shape[0]
    n_movieId = movie.shape[0]
    if n_imdbId == n_movieId:
        n_imdbId = n_imdbId - 1
        print 'the number of movie id:\t', str(n_imdbId)

    return imdbId_series, movieId_series, n_imdbId


# 得到全部的页面内容
def askURL(url):
    request = urllib2.Request(url)  # request
    try:
        response = urllib2.urlopen(request)  # response
        html = response.read()  # get the content of html
        # print html
    except urllib2.URLError, e:
        if hasattr(e, 'code'):
            print e.code
        if hasattr(e, 'reason'):
            print e.reason
    return html


# 1、os.path.exists(path) 判断一个目录是否存在
# 2、os.makedirs(path) 多层创建目录
# 3、os.mkdir(path) 创建目录

def extract_posters(imdbId_series, movieId_series, n_imdbId):
    findImgSrc = re.compile(r'<img.*src="(.*jpg)"', re.S)  # 找到影片图片
    count = 0
    for i in range(1, n_imdbId + 1):
        print imdbId_series[i], movieId_series[i]
        url = basis_font + str(imdbId_series[i]) + basis_back
        html = askURL(url)
        soup = BeautifulSoup(html, 'lxml')
        # for item in soup.find_all('div', class_='media_index_thumb_list'):
        path = pic_dir + str(imdbId_series[i]) + '/'
        if os.path.exists(path) != True:
            os.mkdir(path)
        for item in soup.find_all('img', height='100'):
            item = str(item)
            # print item
            # img_list = soup.select('.media_index_thumb_list')
            # print img_list
            imgSrc = re.findall(findImgSrc, item)[0]
            # print imgSrc
            # print type(imgSrc)
            count += 1
            print count
            save_pic = path + str(count) + '.jpg'
            urllib.urlretrieve(imgSrc, save_pic)
    print 'Download still frames ok...'


if __name__ == '__main__':
    t = time.time()
    imdbId_series, movieId_series, n_imdbId = read_imdbId()
    extract_posters(imdbId_series, movieId_series, n_imdbId)
    print time.time() - t
