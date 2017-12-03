# coding:utf-8
import requests
import time
import urllib
import urllib2
from bs4 import BeautifulSoup
import re
import config

save_path = "./groups_full_20171202.txt"
timeout_path = "./timeout_groupoffset_list.txt"
filter_save_path = "./groups_filter_20171202.txt"


# user_agents = [
#     'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
#     'Opera/9.25 (Windows NT 5.1; U; en)',
#     'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
#     'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
#     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
#     'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
#     "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
#     "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
#
# ]

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


def downloadGroups():
    fw_timeout = open(timeout_path, 'w')
    t = time.time()
    base_url = "https://groups.deviantart.com/?offset="

    # 找到groupname
    # <a class="u regular username" href="https://communism.deviantart.com/">communism</a>
    # findGroupname = re.compile(r'<a class="u regular username">(.*)</a>')

    with open(save_path, 'w') as fw:
        count = 0
        print("start")
        # 翻页后的groupname
        for offset in range(0, 4991, 10):  # offset最多到4000
            print("in")
            url = base_url + str(offset)
            # try:
            #     rq = requests.get(url, timeout=60)
            # except requests.exceptions.ConnectionError:
            #     print("======MD!TIME OUT!======")
            #     fw_timeout.write("https://groups.deviantart.com/?offset="+str(offset) + '\n')
            #     continue

            html = askURL(url)
            if not html:
                continue
            soup = BeautifulSoup(html, "lxml")

            print '-----------------------%d---------------------' % offset

            for item in soup.find_all('a', class_="u regular username"):
                item_contents = item.contents
                item_str = str(item_contents)
                # [u'groupname']
                item_str = item_str[3:-2]
                fw.write(str(item_str) + '\n')
                print item_str, count
                count += 1


# 因为在爬取过程中混有非groupName的字符串 需要过滤掉
# 通过groups.deviantart.com查询过滤
def filterGroups():
    fw = open(filter_save_path, 'w')
    group_set = set()
    with open(save_path, 'r') as fr:
        lines = fr.readlines()
        for line in lines:
            group = line.strip()
            # print(group)
            group_set.add(group)
    print(len(group_set))

    base_url = "https://groups.deviantart.com/?qh=&q="
    # <div class="search-stats"><h1>Xandriia1</h1> <span>No results</span></div>
    # url = base_url + str("Cuphead-FC")
    # url_2 = base_url + str("Xandriia1")
    # html = askURL(url)
    # html_2 = askURL(url_2)
    # soup_2 = BeautifulSoup(html_2, "lxml")
    # soup = BeautifulSoup(html, "lxml")
    # for item in soup_2.find_all('div', class_="search-stats"):
    #     item_contents = item.contents
    #     item_str = str(item_contents)
    #     print item_str
    #     if "No results" in item_str:
    #         print "shit"
    #         break

    for group in group_set:
        url = base_url + str(group)
        html = askURL(url)
        soup = BeautifulSoup(html, "lxml")
        for item in soup.find_all('div', class_="search-stats"):
            item_contents = item.contents
            item_str = str(item_contents)
            # print item_str
            if "No results" in item_str:
                print("--------%s---------This is not a GroupName!!!"%group)
                break
            print("Yes, they are....%s"%group)
            fw.write(str(group)+'\n')

    fw.close()


if __name__ == '__main__':
    # step 1
    # downloadGroups()
    # step 2
    filterGroups()
