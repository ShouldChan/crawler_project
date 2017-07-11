# coding:utf-8
pic_dir = './movielens2011_posters/'
mv_dir = './movielens2011/'

import requests
import time


def downloadPic():
    t = time.time()
    with open(mv_dir + 'movies.dat', 'rb') as fopen:
        lines = fopen.readlines()
        for line in lines:

            tempdata = line.strip().split('\t')
            mvId, url = tempdata[0], tempdata[4]
            print mvId, url, len(url)
            if len(url) != 0:
                try:
                    rq = requests.get(url, timeout=120)
                except requests.exceptions.ConnectionError:
                    print '杰哥这串下载链接超时了！'
                    filepath_txt = pic_dir + str(mvId) + '.txt'
                    fwrite = open(filepath_txt, 'wb')
                    print '------------------------------------------'
                filepath_pic = pic_dir + str(mvId) + '.jpg'

                with open(filepath_pic, 'wb') as picwrite:
                    picwrite.write(rq.content)
                print time.time() - t
                print '====================杰哥海报下好了=================='

downloadPic()
