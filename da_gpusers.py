# coding:utf-8
import requests
import time
import urllib
import urllib2
from bs4 import BeautifulSoup
import re
import httplib

httplib.HTTPConnection._http_vsn = 10
httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'

save_path = "./gpusers.txt"
group_path = "./groups_full.txt"
group_save_path = "./groups_nums.txt"
timeout_path = "./timeout_list.txt"

group_set = set()


def askURL(url):
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
        print(e)

        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
        return None
    return html


def read_groupname():
    with open(group_path, 'r') as fr:
        lines = fr.readlines()
        for line in lines:
            group = line.strip()
            # print(group)
            group_set.add(group)


# read_groupname()
# print(len(group_set))

def downloadGpusers():
    t = time.time()

    # group = "coldmirror-FanClub"
    fw_timeout = open(timeout_path, 'w')
    fw_group = open(group_save_path, 'w')
    with open(save_path, 'w') as fw:
        for group in group_set:
            print("---------Group Name: %s----------" % group.lower())

            '''
            因为用户列表分页的原因，首先获取group用户的个数  <span class="tighttt"><strong>299 </strong> Members<br></span>
            每一页存有100个用户，不满一百的就是单独一页
            三个strong分别对应：members, pageviews, watchers
            '''
            group_url = "https://" + str(group).lower() + ".deviantart.com/"
            try:
                rq = requests.get(group_url, timeout=60)
            except requests.exceptions.ConnectionError:
                print("======MD!TIME OUT!======")
                fw_timeout.write(str(group) + '\n')
                continue

            group_html = askURL(group_url)
            if not group_html:
                continue
            group_soup = BeautifulSoup(group_html, "lxml")

            item_list = group_soup.find_all("span", class_="tighttt")
            item_contents = item_list[0].contents[0].contents
            item_str = str(item_contents)
            item_str = item_str[3:-3]
            if ',' in item_str:
                item_str = item_str.replace(',', '')

            n_gpusers = int(item_str)
            fw_group.write(str(group) + '\t' + str(n_gpusers) + '\n')
            print("nums of user: %d" % n_gpusers)
            print("all the pages: %d" % (int(n_gpusers / 100) + 1))

            for offset in range(0, n_gpusers, 100):
                print offset

                users_url = "https://" + str(group).lower() + ".deviantart.com/modals/memberlist/?offset=" + str(offset)
                try:
                    rq = requests.get(users_url, timeout=90)
                except requests.exceptions.ConnectionError:
                    print("======MD!TIME OUT!======")
                    fw_timeout.write(str(group) + '\t' + str(offset) + '\n')
                    continue

                users_html = askURL(users_url)
                if not users_html:
                    continue

                soup = BeautifulSoup(users_html, "lxml")

                print("----------------------Page. %d-------------------------" % (offset / 100 + 1))
                count = 0
                for item in soup.find_all('a', class_="u regular username"):
                    item_contents = item.contents
                    # inside_contents=item_contents.contents
                    item_str = str(item_contents)
                    # [u'groupname']
                    item_str = item_str[3:-2]
                    fw.write(str(item_str) + '\t' + str(group) + '\n')
                    # print item_str, count
                    count += 1
                print time.time() - t
    fw_group.close()
    fw_timeout.close()


read_groupname()
print(len(group_set))
downloadGpusers()
