# coding:utf-8
pic_dir = './movielens2011_frames/'
mv_dir = './movielens2011/'
basis_font = 'http://www.imdb.com/title/tt'
basis_back = '/mediaindex?refine=still_frame&ref_=ttmi_ref_sf'
# http://www.imdb.com/title/tt0373389/mediaindex?refine=still_frame&ref_=ttmi_ref_sf


import pandas as pd
import re
import urllib2
from bs4 import BeautifulSoup
import urllib
import os
import time


# read imdbId to download the pictures
def read_imdbId():
    dic = {}
    with open(mv_dir + 'movies_edit.txt', 'rb') as fopen:
        lines = fopen.readlines()
        for line in lines:
            tempdata = line.strip().split('\t')
            movieid, imdbid = tempdata[0], tempdata[2]
            print movieid, imdbid
            dic[str(movieid)] = str(imdbid)
    # print dic['1']
    return dic


# read_imdbId()
def read_movieId_need():
    ID_list = []
    with open(mv_dir + 'movie_ID_Jpg_8865.txt', 'rb') as fopen:
        lines = fopen.readlines()
        for line in lines:
            temp = line.strip().split('\t')
            id = temp[0]
            ID_list.append(id)
    # print ID_list
    print len(ID_list)
    return ID_list


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


def extract_posters(dic, ID_list):
    findImgSrc = re.compile(r'<img.*src="(.*jpg)"', re.S)  # 找到影片图片
    count = 87154
    for i in ID_list:
        print '-----', i, str(dic[str(i)])
        url = basis_font + str(dic[str(i)]) + basis_back
        html = askURL(url)
        soup = BeautifulSoup(html, 'lxml')
        path = pic_dir + str(dic[str(i)]) + '/'
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
    dic = read_imdbId()
    ID_list = read_movieId_need()
    extract_posters(dic, ID_list)
    print time.time() - t
