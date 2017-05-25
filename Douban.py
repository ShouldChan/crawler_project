# coding:utf-8
# 使用requests爬豆瓣正在上映的电影
# import HTMLParser
# import requests
#
#
# class MoviesParser(HTMLParser.HTMLParser):
#     def __init__(self):
#         HTMLParser.HTMLParser.__init__(self)
#         self.movies = []
#         self.img_into_movie = False
#         self.a_into_movie = False
#
#     def handle_starttag(self, tag, attrs):
#         # 根据属性名称取值
#         def _attr(attrs,attr_name):
#             for attr in attrs:
#                 if attr[0] == attr_name:
#                     return attr[1]
#             return None
#         # 取出属性值
#         if tag == 'li' and _attr(attrs,'data-title') and _attr(attrs,'data-category') == 'nowplaying':
#             movie = {}
#             movie['title'] = _attr(attrs,'data-title')
#             movie['score'] = _attr(attrs,'data-score')
#             movie['star'] = _attr(attrs,'data-star')
#             movie['duration'] = _attr(attrs,'data-duration')
#             movie['region'] = _attr(attrs,'data-region')
#             movie['director'] = _attr(attrs,'data-director')
#             movie['actors'] = _attr(attrs,'data-actors')
#             self.movies.append(movie)
#             self.img_into_movie = True
#             self.a_into_movie = True
#
#         #获取海报图片
#         if tag == 'img' and self.img_into_movie:
#             self.img_into_movie = False
#             img_src = _attr(attrs,'src')
#             movie = self.movies[len(self.movies) -1]
#             movie['poster_url'] = img_src
#             donwload_poster_url(img_src)
#
#         if tag == 'a' and self.a_into_movie:
#             if _attr(attrs,'data-psource') == 'title':
#                 self.a_into_movie = False
#                 movie_url = _attr(attrs,'href')
#                 movie = self.movies[len(self.movies) -1]
#                 movie['movie_url'] = movie_url
#
#
# # 下载图片
# def donwload_poster_url(url):
#     res = requests.get(url)
#     file_name = str.split(url,'/')[-1]
#     file_path = 'poster_img/' + file_name
#     print('download img file_path = ',file_path)
#     with open(file_path,'wb') as f:
#         f.write(res.content)
#
#
# def douban_movies(url):
#     #首先构建请求头 ，模拟浏览器请求头
#     headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
#     # # 打开链接，并得到返回值
#     res = requests.get(url,headers=headers)
#     # 创建Html解析器
#     moviesParser = MoviesParser()
#     # 解析Html数据
#     moviesParser.feed(res.text)
#     return moviesParser.movies
#
# if __name__ == '__main__':
#     url_str = 'https://movie.douban.com/cinema/nowplaying/shenzhen/'
#     movies_res = douban_movies(url_str)
#
#     import json
#     json_str = json.dumps(movies_res,sort_keys=True,indent=4,separators=(',',': '))
#     # 打印json数据
#     print(json_str)

# !/usr/bin/env python
import urllib.request
from bs4 import BeautifulSoup

mylist = []
print(u'豆瓣电影TOP250:\n 序号 \t 影片名\t 评分\t 评价人数\t 评价')


def crawl(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    req = urllib.request.Request(url, headers=headers)
    page = urllib.request.urlopen(req, timeout=60)
    contents = page.read()
    soup = BeautifulSoup(contents)
    for tag in soup.find_all('div', class_='item'):
        try:
            m_order = int(tag.find('em', class_='').get_text())
            m_name = tag.span.get_text()
            m_rating_score = float(tag.find('div', class_='star').em.get_text())
            m_rating_num = tag.find('div', class_='star').span.next_sibling.next_sibling.get_text()
            m_comments = tag.find("span", class_="inq").get_text()
        except AttributeError:
            print("%s %s %s %s %s" % (m_order, m_name, m_rating_score, m_rating_num, "NO COMMENTS"))
            mylist.append((m_order, m_name, m_rating_score, m_rating_num, "NO COMMENTS"))
        else:
            print("%s %s %s %s %s" % (m_order, m_name, m_rating_score, m_rating_num, m_comments))
            mylist.append((m_order, m_name, m_rating_score, m_rating_num, m_comments))


pagenumber = []
for i in range(10):
    page_number = 25 * i
    pagenumber.append(page_number)
pagelist = list(map(str, pagenumber))

BASE_URL = 'http://movie.douban.com/top250?start='
LAST_URL = '&filter=&type='
for url in [BASE_URL + MID_URL + LAST_URL for MID_URL in pagelist]:
    crawl(url)

import tablib

headers = ('m_order', 'm_name', 'm_rating_score', 'm_rating_num', 'm_comments')
mylist = tablib.Dataset(*mylist, headers=headers)
print(mylist.csv)
with open('./out/doubanmovielist.xlsx', 'wb') as f:
    f.write(mylist.xlsx)