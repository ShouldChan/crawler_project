# coding:utf-8

# 读取我们需要的movieid（即有海报和关键帧的）
movieid_need = []
with open('./movielens2011/valid_movieid_imdbid.txt', 'rb') as fread:
    lines = fread.readlines()
    for line in lines:
        temp = line.strip().split('\t')
        movieid_need.append(temp[0])

print movieid_need

count = 0
fwrite = open('v2_filter_user_ratedmovies.txt', 'wb')
with open('./movielens2011/copy_user_ratedmovies.dat', 'rb') as fread:
    lines = fread.readlines()
    for line in lines:
        count += 1
        print count
        temp = line.strip().split('\t')
        userid, movieid, rate, timestamp = temp[0], temp[1], temp[2], temp[3]
        if movieid in movieid_need:
            print 'in:\t', movieid
            fwrite.write(str(line))
