# coding:utf-8

pic_dir = './movielens2011_frames/'
mv_dir = './movielens2011/'

import os

# read imdbId to filter the pictures
def read_imdbId():
    dic = {}
    with open(mv_dir + 'movies_edit.txt', 'rb') as fopen:
        lines = fopen.readlines()
        for line in lines:
            tempdata = line.strip().split('\t')
            movieid, imdbid = tempdata[0], tempdata[2]
            print movieid, imdbid
            dic[str(movieid)] = str(imdbid)
    # print dic['1']
    return dic

# read_imdbId()
def read_movieId_need():
    ID_list = []
    with open(mv_dir + 'movie_ID_Jpg.txt', 'rb') as fopen:
        lines = fopen.readlines()
        for line in lines:
            temp = line.strip().split('\t')
            id = temp[0]
            ID_list.append(id)
    # print ID_list
    print len(ID_list)
    return ID_list