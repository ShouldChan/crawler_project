# coding:utf-8

pic_dir = './movielens2011_frames/'
mv_dir = './movielens2011/'

import os


# 本文件的作用：过滤掉没有key frame的电影文件夹 并写成一个描述文件
# read imdbId 用字典存储  dic[movieid]：imdbid
def read_imdbId():
    dic = {}
    with open(mv_dir + 'movies_edit.txt', 'rb') as fopen:
        lines = fopen.readlines()
        for line in lines:
            tempdata = line.strip().split('\t')
            movieid, imdbid = tempdata[0], tempdata[2]
            # print movieid, imdbid
            dic[str(movieid)] = str(imdbid)
    # print dic['1']
    return dic


# read_imdbId()
# 读取有poster但并一定有frame的movieid
def read_movieId_need():
    ID_list = []
    with open(mv_dir + 'movie_ID_Jpg.txt', 'rb') as fopen:
        lines = fopen.readlines()
        for line in lines:
            temp = line.strip().split('\t')
            id = temp[0]
            ID_list.append(id)
    # print ID_list
    print 'lengths of the movies need to use:', len(ID_list)
    return ID_list


def traverse_folder(dic, Id_list):
    fwrite = open(mv_dir + 'valid_movieid_imdbid.txt', 'wb')
    for i in Id_list:
        path = pic_dir + str(dic[str(i)]) + '/'
        if os.path.exists(path) == False:
            print 'not exist this folder.........'
        else:
            for root, dirs, files in os.walk(path):  # 获取目录下文件的个数 如果该文件夹为空就删除并记录写入一个描述文件
                if len(files) == 0:
                    print '--------------this folder is empty--------------'
                else:
                    fwrite.write(str(i) + '\t' + str(dic[str(i)]) + '\n')
                    # 将这个文件夹下无效的图片剔除
                    for j in files:
                        jpg_path = path + str(j)
                        fsize = os.path.getsize(jpg_path)
                        if fsize == 0:
                            os.remove(jpg_path)
                            print 'remove already...'
                    print files
        print i, dic[str(i)]
    print 'traverse over...'


if __name__ == '__main__':
    dic = read_imdbId()
    Id_list = read_movieId_need()
    traverse_folder(dic, Id_list)
