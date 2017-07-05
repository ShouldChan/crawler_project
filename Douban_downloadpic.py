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
            hg_url, movie_name = tempData[0], tempData[2]
            hg_list.append([movie_name, hg_url])
    print hg_list
    print len(hg_list)


# 获取poster的ID 这个ID是用来加在高清海报图片后面下载链接的
def getPID(hg_list, pid_list):
    x = 0
    count = 1
    # fwrite = open('./LOGs.txt', 'wb')
    find_pid = re.compile(r'<li data-id="(.*?)">')  # get posterID
    for hg_line in hg_list:
        movie_name = hg_line[0]
        url = hg_line[1] + base_pid_suffix
        r = requests.get(url)
        content = r.content.decode('utf8')
        soup = BeautifulSoup(content, 'lxml')
        # print str(count)
        # count += 1
        print '------------------' + str(movie_name) + '-----------------------'
        print str(url)
        # fwrite.write(str(x + 1))
        # fwrite.write('------------------' + str(movie_name) + '-----------------------')
        for item in soup.find_all('div', class_='article'):
            item = str(item)
            pid = re.findall(find_pid, item)[0]
            pid_list.append(pid)
            x += 1
            print str(pid) + '\t' + str(x)
            # fwrite.write(str(pid) + '\t' + str(x))
        print '------------------' + str(movie_name) + '-----------------------'
        # fwrite.write('------------------' + str(movie_name) + '-----------------------')
    print pid_list


def downloadPic(pid_list):
    x = 0
    print 'walk into the loop...'
    for each_pid in pid_list:
        x += 1
        print x
        down_url = 'https://img3.doubanio.com/view/photo/photo/public/p' + str(each_pid) + '.webp'
        save_pic = './posters/' + str(x) + '.jpg'
        urllib.urlretrieve(down_url, save_pic)
    print 'walk out of the loop...'
    # fwrite_pic = open(pic_dir + '1.webp', 'wb')
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

    getPID(hg_list, pid_list)
    print '-------getPID over-------\t' + str(time.time() - t)
    #
    # downloadPic(pid_list)
    # print '-------downloadPic over------\t' + str(time.time() - t)


main()
