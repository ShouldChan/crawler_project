# coding:utf-8
import requests
import time
import urllib
import urllib2
from bs4 import BeautifulSoup
import re

save_path = "./groups.txt"


def askURL(url):
    # 发送请求
    request = urllib2.Request(url)
    try:
        # 取得响应
        response = urllib2.urlopen(request)
        # 获得网页的内容
        html = response.read()
        # print(html)
    except urllib2.URLError, e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


def downloadGroups():
    t = time.time()
    base_url = "https://groups.deviantart.com/?offset="

    # 找到groupname
    # <a class="u regular username" href="https://communism.deviantart.com/">communism</a>
    # findGroupname = re.compile(r'<a class="u regular username">(.*)</a>')

    with open(save_path, 'w') as fw:
        count = 0

        # 翻页后的groupname
        for offset in range(0, 4001):   # offset最多到4000
            url = base_url + str(offset)
            html = askURL(url)
            soup = BeautifulSoup(html, "lxml")

            print '-----------------------%d---------------------'%offset

            for item in soup.find_all('a', class_="u regular username"):
                item_contents = item.contents
                item_str = str(item_contents)
                # [u'groupname']
                item_str = item_str[3:-2]
                fw.write(str(item_str) + '\n')
                print item_str, count
                count += 1


downloadGroups()
