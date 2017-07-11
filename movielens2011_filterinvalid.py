# coding:utf-8

pic_dir = './movielens2011_posters/'

import os

# remove the 0kb jpg (invalid one)
def get_FileSize():
    for x in range(1, 65134, 1):
        fpath = pic_dir + str(x) + '.jpg'
        if os.path.exists(fpath):
            filePath = unicode(fpath, 'utf-8')
            fsize = os.path.getsize(filePath)
            if fsize == 0:
                os.remove(filePath)
                print 'remove already...'
            else:
                fsize = fsize / float(1024)
                print x, '\tfile size:\t', fsize
                # return round(fsize, 2)
        else:
            print 'pic does not exist...'
            continue
    print 'operation over..'

get_FileSize()

# def test():
#     filepath = unicode(pic_dir + '9.jpg', 'utf-8')
#     os.remove(filepath)
# test()
