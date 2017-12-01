# coding:utf-8
import requests
import time
import urllib
import urllib2
from bs4 import BeautifulSoup
import re

save_path = "./gpusers.txt"
group_path = "./groups_full.txt"

group_set = set()


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


def read_groupname():
    with open(group_path, 'r') as fr:
        lines = fr.readlines()
        for line in lines:
            group = line.strip()
            print(group)
            group_set.add(group)


# read_groupname()
# print(len(group_set))

def downloadGpusers():
    t = time.time()
    count = 0
    group="coldmirror-FanClub"
    print(group.lower())

    # 获取group用户的个数  <span class="tighttt"><strong>299 </strong> Members<br></span>
    url = "https://" + str(group).lower() + ".deviantart.com/modals/memberlist/"
    html = askURL(url)
    soup = BeautifulSoup(html, "lxml")
    print("----------------------No. %d-------------------------" % count)
    # count += 1
    for item in soup.find_all('a', class_="u regular username"):
        item_contents = item.contents
        item_str = str(item_contents)
        # [u'groupname']
        item_str = item_str[3:-2]
        print item_str, count
        count += 1
    # with open(save_path, 'w') as fw:
    #     for group in group_set:
    #         url = "https://" + str(group).lower() + ".deviantart.com"
    #         html = askURL(url)
    #         soup = BeautifulSoup(html, "lxml")
    #         print("----------------------No. %d-------------------------" % count)
    #         count += 1
    #         for item in soup.find_all('a', class_="u regular username"):
    #             item_contents = item.contents
    #             item_str = str(item_contents)
    #             # [u'groupname']
    #             item_str = item_str[3:-2]
    #             fw.write(str(item_str) + '\n')
    #             print item_str, count
    #             count += 1
    #
downloadGpusers()