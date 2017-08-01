# coding:utf-8
pic_dir = './ml_20m_posters/'
mv_dir = './ml_20m/'
basis_font = 'http://www.imdb.com/title/tt'
basis_back = '/mediaindex?refine=poster&ref_=ttmi_ref_pos'

import requests
import time
import pandas as pd
import re
import urllib2
from bs4 import BeautifulSoup
import urllib
import os


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

    return imdbId_series, movieId_series, n_imdbId


# 得到页面全部内容
def askURL(url):
    request = urllib2.Request(url)  # 发送请求
    try:
        response = urllib2.urlopen(request)  # 取得响应
        html = response.read()  # 获取网页内容
        # print html
    except urllib2.URLError, e:
        if hasattr(e, "code"):
            print e.code
        if hasattr(e, "reason"):
            print e.reason
    return html


# 1、os.path.exists(path) 判断一个目录是否存在
# 2、os.makedirs(path) 多层创建目录
# 3、os.mkdir(path) 创建目录
def extract_posters(imdbid_series, movieid_series, n_imdbid):
    # findLink = re.compile(r'<a href="(.*?)">')  # 找到影片详情链接
    findImgSrc = re.compile(r'<img.*src="(.*jpg)"', re.S)  # 找到影片图片
    # findTitle = re.compile(r'<span class="title">(.*)</span>')  # 找到片名
    # 去掉无关内容
    # remove = re.compile(r'                            |\n|</br>|\.*')
    count = 0
    for i in range(1, n_imdbid + 1):
        print imdbid_series[i], movieid_series[i]
        url = basis_font + str(imdbid_series[i]) + basis_back
        html = askURL(url)
        soup = BeautifulSoup(html, 'lxml')
        # for item in soup.find_all('div', class_='media_index_thumb_list'):
        path = pic_dir + str(imdbid_series[i]) + '/'
        if os.path.exists(path) != True:
            os.mkdir(path)
        for item in soup.find_all('img', height='100'):
            item = str(item)
            # print item
            # img_list = soup.select('.media_index_thumb_list')
            # print img_list
            imgSrc = re.findall(findImgSrc, item)[0]
            print imgSrc
            print type(imgSrc)
            count += 1
            save_pic = path + str(count) + '.jpg'
            urllib.urlretrieve(imgSrc, save_pic)
    print 'asdasd'


if __name__ == '__main__':
    imdbid_series, movieid_series, n_imdbid = read_imdbId()
    # print imdbid_series, n_imdbid
    extract_posters(imdbid_series, movieid_series, n_imdbid)
