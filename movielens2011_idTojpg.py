# coding:utf-8

pic_dir='./movielens2011_posters/'
describe_dir='./movielens2011/movie_ID_Jpg.txt'
import os

# describe the movie by Id to Jpg.

def describe_idTojpg():
    fwrite=open(describe_dir,'wb')
    for x in range(1,65134,1):
        fpath=pic_dir+str(x)+'.jpg'
        if os.path.exists(fpath):
            fwrite.write(str(x)+'\t'+str(x)+'.jpg\n')
            print str(x)+'\t'+str(x)+'.jpg\n'

describe_idTojpg()