# coding:utf-8

import requests
import time
import sys
import urllib2
import re

reload(sys)
sys.setdefaultencoding('utf8')
pic_dir = './posters/'

t = time.time()


# download the posters from the dataset
# crawl the movie homepage from the crawled dataset
def readHomepage(hg_list):
    with open('./douban_Top250.txt', 'rb') as fread_hg:
        lines = fread_hg.readlines()
        for line in lines:
            tempData = line.strip().split('\t')
            hg_url = tempData[0]
            hg_list.append(hg_url)
    print hg_list


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


def getPosterId(base_url):
    find_pId = re.compile(r'<li data-id="(.*?)">')  # get posterID
    print find_pId


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
    base_img = 'https://img3.doubanio.com/view/photo/raw/public/p'
    pic_list = []
    hg_list = []
    test_hg = 'https://movie.douban.com/subject/1292262/'
    getPosterId(test_hg)
    # readHomepage(hg_list)
    print '-------readHomepageUrl over-------'
    # readPicUrl(pic_list)
    print '-------readPicUrl over-------'
    # downloadPic(pic_list)
    print '-------downloadPic over------'


main()
