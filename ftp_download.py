# coding:utf-8
import os
import urllib
import logging
import sys

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    stream=sys.stdout)
save_path = 'e:/250/'


def read_ftpurl():
    ftpurl_list = []
    with open('./600.txt', 'rb') as fopen:
        lines = fopen.readlines()
        for line in lines:
            # print line
            ftpurl_list.append(line)
    # print ftpurl_list
    return ftpurl_list


def download(ftpurl_list):
    for each_url in ftpurl_list:
        try:
            urllib.urlretrieve(each_url, save_path)
        except:
            print 'wrong'


if __name__ == '__main__':
    ftpurl_list = read_ftpurl()
    download(ftpurl_list)
