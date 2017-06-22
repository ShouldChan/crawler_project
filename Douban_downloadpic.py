# coding:utf-8

import requests
import time
import sys
import urllib2
import urllib
import re
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf8')

pic_dir = './posters/'

base_img_url = 'https://img3.doubanio.com/view/photo/raw/public/p'
base_pid_suffix = 'photos?type=R'

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


# 获取poster的ID 这个ID是用来加在高清海报图片后面下载链接的
def getPID(hg_list, pid_list):
    find_pid = re.compile(r'<li data-id="(.*?)">')  # get posterID
    for hg_url in hg_list:
        url = hg_url + base_pid_suffix
        r = requests.get(url)
        content = r.content.decode('utf8')
        soup = BeautifulSoup(content, 'lxml')
        for item in soup.find_all('div', class_='article'):
            item = str(item)
            pid = re.findall(find_pid, item)[0]
            pid_list.append(pid)
            # print pid
    print pid_list


# def savePosterDownloadUrl_txt()


def downloadPic():
    # piccontent = urllib2.urlopen('https://img3.doubanio.com/view/photo/raw/public/p480747492.jpg').read()
    urllib.urlretrieve('https://movie.douban.com/photos/photo/480747492/', './1.jpg')
    # fwrite_pic = open(pic_dir + '1.jpg', 'wb')
    # fwrite_pic.write(piccontent)
    # fwrite_pic.close()

    # fwrite_timeout = open(pic_dir + 'timeout_list.txt', 'ab')
    # try:
    #     rq = requests.get('https://img3.doubanio.com/view/photo/raw/public/p480747492.jpg', timeout=120)
    # except requests.exceptions.ConnectionError:
    #     print 'md!download time out!Mark this and try again...'
    #     fwrite_timeout.write(str(1) + '\n')
    #     print '----------------------------------------------------'
    # finally:
    #     filePath_pic = pic_dir + '1.jpg'
    #
    #     fwrite_pic = open(filePath_pic, 'wb')
    #     fwrite_pic.write(rq.content)
    #     fwrite_pic.close()
    # fwrite_timeout.close()
    # x = 0
    # fwrite_timeout = open(pic_dir + 'timeout_list.txt', 'ab')
    # for pic_url in pic_list:
    #     x += 1
    #     print x
    #     filePath_txt = pic_dir + '%s.txt' % x
    #     print pic_url
    #     try:
    #         rq = requests.get(pic_url, timeout=120)
    #     except requests.exceptions.ConnectionError:
    #         print 'md!download time out!Mark this and try again...'
    #         fwrite_timeout.write(str(x) + '\t' + str(pic_url) + '\n')
    #         print '----------------------------------------------------'
    #         continue
    #     filePath_pic = pic_dir + '%s.jpg' % x
    #
    #     fwrite_pic = open(filePath_pic, 'wb')
    #     fwrite_pic.write(rq.content)
    #     print time.time() - t
    #     print '==========================='


# 读取下载数据集里面的第二列poster缩略图的下载链接（已经不用缩略图了 不够清晰）
def readPicUrl(pic_list):
    with open('./douban_Top250.txt', 'rb') as fread:
        lines = fread.readlines()
        for line in lines:
            tempData = line.strip().split('\t')
            # print tempData
            pic_url = tempData[1]
            print pic_url
            pic_list.append(pic_url)

# 模拟登陆豆瓣
# def modelLogin():


def main():
    t = time.time()
    pic_list = []  # 图片下载链接
    hg_list = []  # 每部电影主页的链接
    pid_list = []  # 获取poster的ID 加在base_img_url后面用于下载图片

    readHomepage(hg_list)
    print '-------readHomepageUrl over-------\t' + str(time.time() - t)

    getPID(hg_list,pid_list)
    print '-------getPID over-------\t' + str(time.time() - t)

    downloadPic()
    print '-------downloadPic over------\t' + str(time.time() - t)




main()
