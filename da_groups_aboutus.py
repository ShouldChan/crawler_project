# coding:utf-8
import requests
import time
import urllib
import urllib2
from bs4 import BeautifulSoup
import re

groupInfo_path = "./2018_01_14/groups_info_20180114.txt"
founders_save_path = "./2018_01_14/group_founders_20180116.txt"
not_founders_save_path = "./2018_01_14/group_not_founders_20180116.txt"


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


# 读取组名
def getGroupName():
    groupName_list = []
    with open(groupInfo_path, 'r') as fr:
        lines = fr.readlines()
        for line in lines:
            temp = line.strip().split('\t')
            groupName = temp[0]
            groupName_list.append(groupName)
    return groupName_list


# 爬取[GROUPNAME].deviantart.com中aboutus中的组创建人founder
def getFounder():
    groupName_list = getGroupName()
    print("=======read GroupName over...======")
    fw = open(founders_save_path, 'w')
    fw_not = open(not_founders_save_path, 'w')
    for eachGroupName, count in zip(groupName_list, range(0, len(groupName_list))):
        groupAboutusUrl = "https://" + str(eachGroupName) + ".deviantart.com/aboutus/"

        html = askURL(groupAboutusUrl)
        if not html:
            continue
        soup = BeautifulSoup(html, "lxml")
        # print(type(soup))
        print("-------------%d-----------" % count)

        member_list = []
        for item in soup.find_all('div', class_="pppp c"):
            # print(type(item))
            # print(item)
            item = item.find_all("img")

            for subitem in item:
                admin = subitem.get("title")
                # print(subitem.get("title"))
                member_list.append(admin)
        if len(member_list) == 0:
            fw.write(str(eachGroupName)+"\n")
            fw_not.write(str(eachGroupName)+"\n")
            fw.flush()
            fw_not.flush()
            print("nothing")
        else:
            # print(member_list)
            # print("-----")
            # print(len(member_list))
            fw.write(str(eachGroupName)+"\t")
            for i in range(0, len(member_list)):
                if i == len(member_list) - 1:
                    fw.write(str(member_list[i])+"\n")
                    fw.flush()
                    print(member_list[i])
                else:
                    fw.write(str(member_list[i])+"\t")
                    fw.flush()
                    print(member_list[i])
    fw.close()
    fw_not.close()

    print("===========get Founder Over=========")


if __name__ == '__main__':
    # 1.爬取founder
    getFounder()
