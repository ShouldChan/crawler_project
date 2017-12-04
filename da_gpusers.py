# coding:utf-8
import time
import urllib2
from contextlib import nested

from bs4 import BeautifulSoup

# 错误代码的设置 在访问
# httplib.HTTPConnection._http_vsn = 10
# httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'

save_path = "./gpusers.txt"
group_path = "./groups_filter_20171202.txt"
group_save_path = "./groups_filter_nums_20171203.txt"
group_timeout_path = "./group_timeout_list_20171203.txt"
user_timeout_path = "./group_timeout_list_20171203.txt"
# 遇到中途出现异常错误而停止的问题 直接保存group name 并且 保存已爬下的group name
have_crawled_group_path="./have_crawled_group_20171203.txt"


# group_set = set()


def askURL(url, host_name):
    # 解决HTTP Error 403: Forbidden
    # 伪装成浏览器
    # host_name = str(host_name).lower()
    headers = {
        'Host': host_name + '.deviantart.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/62.0.3202.75 Chrome/62.0.3202.75 Safari/537.36'
    }
    # 发送请求
    html = ""
    request = urllib2.Request(url, headers=headers)
    # request = urllib2.Request(url)
    try:
        # 取得响应
        response = urllib2.urlopen(request)
        # 获得网页的内容
        html = response.read()
        # print(html)
    except urllib2.URLError, e:
        # print(e)

        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
        return None
    return html


def read_groupname():
    group_set=set()
    with open(group_path, 'r') as fr:
        lines = fr.readlines()
        for line in lines:
            group = line.strip()
            # print(group)
            group_set.add(group.lower())
    return group_set

def read_crawled_groupname():
    group_crawled_set=set()
    with open(have_crawled_group_path,'r') as fr:
        lines =fr.readlines()
        for line in lines:
            group=line.strip()
            group_crawled_set.add(group)
    return group_crawled_set

def downloadGpusers():
    t = time.time()
    group_set=read_groupname()
    # 读取已爬取的groupname 得到未爬取的组
    group_crawled_set=read_crawled_groupname()
    group_not_crawed_set= group_set-group_crawled_set

    print("Total groups: %d"%len(group_set))
    print("Have crawled groups: %d"%len(group_crawled_set))
    print("Need to crawl groups: %d"%len(group_not_crawed_set))

    # fw_group_timeout = open(group_timeout_path, 'a+')
    # fw_user_timeout=open(user_timeout_path, 'a+')
    # fw_group = open(group_save_path, 'a+')
    # fw_crawled=open(have_crawled_group_path, 'a+')

    with nested(open(save_path, 'a+'),open(group_timeout_path, 'a+'),open(user_timeout_path, 'a+'),open(group_save_path, 'a+'),open(have_crawled_group_path, 'a+')) as (fw,fw_group_timeout,fw_user_timeout,fw_group,fw_crawled):
        for group in group_not_crawed_set:
            print("---------Group Name: %s----------" % group)

            '''
            因为用户列表分页的原因，首先获取group用户的个数  <span class="tighttt"><strong>299 </strong> Members<br></span>
            每一页存有100个用户，不满一百的就是单独一页
            三个strong分别对应：members, pageviews, watchers
            '''
            group_url = "https://" + str(group).lower() + ".deviantart.com"
            print(group_url)
            # try:
            #     rq = requests.get(group_url, timeout=60)
            # except requests.exceptions.ConnectionError:
            #     print("======MD!TIME OUT!======")
            #     fw_timeout.write(str(group) + '\n')
            #     continue

            group_html = askURL(group_url, group)
            if not group_html:
                fw_group_timeout.write(str(group)+'\t'+str(group_url)+'\n')
                continue
            group_soup = BeautifulSoup(group_html, "lxml")

            try:
                item_list = group_soup.find_all("span", class_="tighttt")
                item_contents = item_list[0].contents[0].contents
            except:
                fw_group_timeout.write("GROUP!!!Catch Error\t"+str(group)+'\n')
                continue
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
                print(users_url)
                # try:
                #     rq = requests.get(users_url, timeout=60)
                # except requests.exceptions.ConnectionError:
                #     print("======MD!TIME OUT!======")
                #     fw_timeout.write(str(group) + '\t' + str(offset) + '\n')
                #     continue

                users_html = askURL(users_url, group)
                if not users_html:
                    fw_user_timeout.write(str(group)+'\t'+str(offset)+'\t'+str(users_url)+'\n')
                    continue

                soup = BeautifulSoup(users_html, "lxml")

                print("----------------------Page. %d-------------------------" % (offset / 100 + 1))
                count = 0

                try:
                    # 爬取核心用户
                    premium_items = soup.find_all('a', class_="u premium username")
                    if premium_items:
                        for item in soup.find_all('a', class_="u regular username"):
                            item_contents = item.contents
                        item_str = str(item_contents)
                        # [u'groupname']
                        item_str = item_str[3:-2]
                        print(item_str)
                        fw.write(str(item_str) + '\t' + str(group) + '\n')

                    for item in soup.find_all('a', class_="u regular username"):
                        item_contents = item.contents
                        item_str = str(item_contents)
                        # [u'groupname']
                        item_str = item_str[3:-2]
                        fw.write(str(item_str) + '\t' + str(group) + '\n')
                        # print item_str, count
                        count += 1
                except:
                    fw_user_timeout.write("USER!!!Catch Error\t"+str(group)+'\t'+str(offset)+'\n')
                    continue
                print time.time() - t
            fw_crawled.write(str(group)+'\n')
    # fw_group.close()
    # fw_group_timeout.close()
    # fw_user_timeout.close()
    # fw_crawled.close()


def test_download():
    group_set=read_groupname()
    for group in group_set:
        print("group name:%s"%group)
        group_url = "https://" + str(group).lower() + ".deviantart.com"
        print(group_url)
        group_html = askURL(group_url, group)
        group_soup = BeautifulSoup(group_html, "lxml")
        item_list = group_soup.find_all("span", class_="tighttt")
        item_contents = item_list[0].contents[0].contents
        item_str = str(item_contents)
        item_str = item_str[3:-3]
        if ',' in item_str:
            item_str = item_str.replace(',', '')

        n_gpusers = int(item_str)
        print("nums of user: %d" % n_gpusers)
        print("all the pages: %d" % (int(n_gpusers / 100) + 1))

# test_download()
# downloadGpusers()
downloadGpusers()
