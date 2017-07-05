# coding:utf-8
pic_dir = './imdb_posters/'
imdb_dir = './imdb/'

import csv
import requests
import re
import sys
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf8')


# Step1
def read_save_imdb():
    jpg_describ_txt = open(pic_dir + 'jpg_description.txt', 'wb+')
    count = 0
    with open(imdb_dir + 'movie_metadata.csv', 'rb') as csvfile:
        # reader = csv.DictReader(csvfile)
        # title = [row['movie_title'] for row in reader]
        # link_url = [row['movie_imdb_link'] for row in reader]
        # print title
        # print link_url
        reader = csv.reader(csvfile)
        for line in reader:
            movie_title, link_url = line[11], line[17]
            jpg_describ_txt.write(str(count) + '\t' + str(movie_title) + '\t' + str(link_url) + '\n')
            count += 1
            print movie_title + '\t' + link_url


# read_save_imdb()

# Step2
def get_picurl():
    x = 0
    picurl_list = []
    find_url = re.compile(r'<img src="(.*?)">')  # get picurl
    with open(pic_dir + 'jpg_description.txt', 'rb') as readfile:
        lines = readfile.readlines()
        for line in lines:
            link_url = line.strip().split('\t')[0]
            print link_url
            r = requests.get(link_url)
            content = r.content.decode('utf8')
            soup = BeautifulSoup(content, 'lxml')
            x += 1
            print link_url

            for item in soup.find_all('div', class_='poster'):
                item = str(item)
                print item
                picurl = re.findall(find_url, item)
                picurl_list.append(picurl)
                print str(picurl) + '\t' + str(x)


get_picurl()
