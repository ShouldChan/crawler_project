# coding:utf-8

import requests
import time
import sys

reload(sys)
sys.setdefaultencoding('utf8')
pic_dir = './posters/'

t = time.time()


# download the posters from the dataset
# crawl the movie homepage from the crawled dataset
def readHomepage():
    with open('./douban_Top250.txt','rb') as fread_hg:
        lines =fread_hg.readlines()
        for line in lines:
            tempData=line.strip().split('\t')
def downloadPic(pic_list):
    x = 0
    fwrite_timeout = open(pic_dir + 'timeout_list.txt', 'ab')
    for pic_url in pic_list:
        x += 1
        print x
        filePath_txt = pic_dir + '%s.txt' % x
        print pic_url
        try:
            rq = requests.get(pic_url, timeout=120)
        except requests.exceptions.ConnectionError:
            print 'md!download time out!Mark this and try again...'
            fwrite_timeout.write(str(x) + '\t' + str(pic_url) + '\n')
            print '----------------------------------------------------'
            continue
        filePath_pic = pic_dir + '%s.jpg' % x

        fwrite_pic = open(filePath_pic, 'wb')
        fwrite_pic.write(rq.content)
        print time.time() - t
        print '==========================='


def readPicUrl(pic_list):
    with open('./douban_Top250.txt', 'rb') as fread:
        lines = fread.readlines()
        for line in lines:
            tempData = line.strip().split('\t')
            # print tempData
            pic_url = tempData[1]
            print pic_url
            pic_list.append(pic_url)


def main():
    pic_list = []
    readPicUrl(pic_list)
    print '-------readUrl over-------'
    downloadPic(pic_list)
    print '-------downloadPic over------'


main()