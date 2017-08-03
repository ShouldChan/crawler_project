# coding:utf-8
import os
import os.path

folderpath = './'
# identify: is empty
empty = False

count = 1
for count in range(1, 4):
	if os.path.exists(folderpath+str(count))==False:
		count += 1
		print 'not exist'
	else:
		for root, dirs, files in os.walk(folderpath+str(count)):
			print type(root)
			print root
			print type(dirs)
			print dirs
			print type(files)
			print files
			if len(files) == 0:
				empty = True
				print 'wei kong'
		count += 1