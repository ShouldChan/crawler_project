# coding:utf-8
import requests
import time
import urllib
import urllib2
from bs4 import BeautifulSoup
import re
import config

save_path = "./2018_01_14/groups_info_20180114.txt"
group_path = "./2018_01_14/have_crawled_group_20171203.txt"
# group_path = "./2018_01_14/test.txt"


def askURL(url):
    # 解决HTTP Error 403: Forbidden
    # 伪装成浏览器
    # headers = {
    #     # 'Host': 'groups.deviantart.com',
    #     'User-Agent': 'MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'
    # }
    # 发送请求
    html = ""
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
        return None
    return html


def getGroupName():
    group_list = []
    with open(group_path, 'r') as fr:
        lines = fr.readlines()
        for line in lines:
            groupName = line.strip()
            # print(groupName)
            group_list.append(groupName)
        print("METHOD: getGroupName\t%d" % len(group_list))
    return group_list

# TEST
# strin = "[[[[dfssaf<strong>890 </strong>,sdafasdfsdaf<strong>221</strong> u' Watchers' <strong>fuck</strong>"
# datapre = re.compile(r'<strong>(.*?)</strong>')
# res = datapre.findall(strin)
# print res


def getGroupInfo():
    groupInfo_list = []
    group_list = getGroupName()
    for eachGroupName, count in zip(group_list, range(0, len(group_list))):
        groupHomepageUrl = "https://" + str(eachGroupName) + ".deviantart.com"

        html = askURL(groupHomepageUrl)
        if not html:
            continue
        soup = BeautifulSoup(html, "lxml")
        print("-------------%d-----------" % count)

        # [u'\n', <span class="tighttt"><strong>310 </strong> Members<br/></span>, <span class="tighttt"><strong>77,216 </strong> Pageviews</span>, <span class="tighttt"><strong>890 </strong> Watchers</span>, u' ']

        for item in soup.find_all('span', class_="tight"):
            item_contents = item.contents
            item_str = str(item_contents)
            data = re.compile(r'<strong>(.*?)</strong>')
            # print(item_str)
            res = data.findall(item_str)
            groupInfo_list.append([eachGroupName, res])
            print(res)
    return groupInfo_list


def writeGroupInfo():
    groupInfo_list = getGroupInfo()
    with open(save_path, 'w') as fw:
        for name, mem_page_wat in groupInfo_list:
            mem, page, wat = mem_page_wat

            fw.write(str(name) + '\t' + str(mem).strip() + '\t' + str(page).strip() + '\t' + str(wat).strip() + '\n')
    print("=============over==============")


writeGroupInfo()
