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

# 3.
group_founders_523_path = "./2018_01_14/group_founders_523_20180118.txt"
gpuser_path = "./2018_01_14/gpusers_20171205.txt"
user_group_path = "./2018_01_14/user_group_20180118.txt"


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
            fw.write(str(eachGroupName) + "\n")
            fw_not.write(str(eachGroupName) + "\n")
            fw.flush()
            fw_not.flush()
            print("nothing")
        else:
            # print(member_list)
            # print("-----")
            # print(len(member_list))
            fw.write(str(eachGroupName) + "\t")
            for i in range(0, len(member_list)):
                if i == len(member_list) - 1:
                    fw.write(str(member_list[i]) + "\n")
                    fw.flush()
                    print(member_list[i])
                else:
                    fw.write(str(member_list[i]) + "\t")
                    fw.flush()
                    print(member_list[i])
    fw.close()
    fw_not.close()

    print("===========get Founder Over=========")


def filterGroups():
    not_crawled_list = []
    fw = open("./2018_01_14/group_founders_filter_20180117.txt", 'w')
    with open(not_founders_save_path, 'r') as fr1:
        lines = fr1.readlines()
        for line in lines:
            temp = line.strip().split('\t')
            name = temp[0]
            not_crawled_list.append(name)
    print(len(not_crawled_list))

    count = 1
    with open(founders_save_path, 'r') as fr2:
        lines = fr2.readlines()
        for i in range(0, len(lines)):
            temp = lines[i].strip().split('\t')
            name = temp[0]
            if name in not_crawled_list:
                print count
                count += 1
            else:
                fw.write(lines[i])
                fw.flush()
                print("--------")

    fw.close()


def extractUser():
    groupname_list = []
    fw = open(user_group_path, 'w')
    with open(group_founders_523_path, 'r') as fr1:
        lines = fr1.readlines()
        for line in lines:
            temp = line.strip().split('\t')
            name = temp[0]
            groupname_list.append(name)

    print(len(groupname_list))
    count = 1

    with open(gpuser_path, 'r') as fr2:
        lines = fr2.readlines()
        for line in lines:
            temp = line.strip().split('\t')
            username, groupname = temp[0], temp[1]
            print(line)
            if groupname in groupname_list:
                print(count)
                count += 1
                fw.write(line)
                fw.flush()
    fw.close()


if __name__ == '__main__':
    # 1.爬取founder
    # getFounder()
    # 2.filter not founders
    # filterGroups()

    # 3.小部分组数据抽取所需用户和组关系
    extractUser()
