# coding:utf-8
# 因为poster下载链接有失效，所以根据有效的posterID（movieId）重新筛选合理的ID
jpgdes_dir = './movie_ID_Jpg.txt'
rate_dir = './user_ratedmovies-timestamps.dat'

movieid_list = []
with open(jpgdes_dir, 'rb') as jpgopen:
	lines = jpgopen.readlines()
	for line in lines:
		tempdata = line.strip().split('\t')
		movie_id = tempdata[0]
		movieid_list.append(movie_id)
	print movieid_list

fwrite = open('./valid_user_ratedmovies.txt', 'wb')

with open(rate_dir, 'rb') as rateopen:
	lines = rateopen.readlines()
	for line in lines:
		tempdata = line.strip().split('\t')
		movieId = tempdata[1]
		if movieId in movieid_list:
			print 'valid'
			fwrite.write(str(line))
		else:
			print 'invalid movieID'
			continue