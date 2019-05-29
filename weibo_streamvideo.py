
# coding: utf-8

# In[18]:


import requests
from contextlib import closing
import os


# In[24]:

def download_file(url, path):
    with closing(requests.get(url, stream=True)) as r:
        chunk_size=1024
        content_size=int(r.headers['content-length'])
        print "Download begin..."
        with open(path,"wb") as f:
            n=1
            for chunk in r.iter_content(chunk_size=chunk_size):
                loaded = n*1024.0/content_size
                f.write(chunk)
                print '已下载{0:%}'.format(loaded)
                n+=1
                


# In[30]:

url="https://f.us.sinaimg.cn/000S3Y78lx07ue4wxEZG010412003tRV0E010.mp4?label=mp4_hd&template=480x270.28.0&Expires=1559104721&ssig=FAG%2BsDStX2&KID=unistore,video"
path="f://1.mp4"
download_file(url,path)


# In[ ]:



