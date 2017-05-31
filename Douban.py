# coding:utf-8
# 使用requests爬豆瓣正在上映的电影
# import HTMLParser
# import requests
#
#
# class MoviesParser(HTMLParser.HTMLParser):
#     def __init__(self):
#         HTMLParser.HTMLParser.__init__(self)
#         self.movies = []
#         self.img_into_movie = False
#         self.a_into_movie = False
#
#     def handle_starttag(self, tag, attrs):
#         # 根据属性名称取值
#         def _attr(attrs,attr_name):
#             for attr in attrs:
#                 if attr[0] == attr_name:
#                     return attr[1]
#             return None
#         # 取出属性值
#         if tag == 'li' and _attr(attrs,'data-title') and _attr(attrs,'data-category') == 'nowplaying':
#             movie = {}
#             movie['title'] = _attr(attrs,'data-title')
#             movie['score'] = _attr(attrs,'data-score')
#             movie['star'] = _attr(attrs,'data-star')
#             movie['duration'] = _attr(attrs,'data-duration')
#             movie['region'] = _attr(attrs,'data-region')
#             movie['director'] = _attr(attrs,'data-director')
#             movie['actors'] = _attr(attrs,'data-actors')
#             self.movies.append(movie)
#             self.img_into_movie = True
#             self.a_into_movie = True
#
#         #获取海报图片
#         if tag == 'img' and self.img_into_movie:
#             self.img_into_movie = False
#             img_src = _attr(attrs,'src')
#             movie = self.movies[len(self.movies) -1]
#             movie['poster_url'] = img_src
#             donwload_poster_url(img_src)
#
#         if tag == 'a' and self.a_into_movie:
#             if _attr(attrs,'data-psource') == 'title':
#                 self.a_into_movie = False
#                 movie_url = _attr(attrs,'href')
#                 movie = self.movies[len(self.movies) -1]
#                 movie['movie_url'] = movie_url
#
#
# # 下载图片
# def donwload_poster_url(url):
#     res = requests.get(url)
#     file_name = str.split(url,'/')[-1]
#     file_path = 'poster_img/' + file_name
#     print('download img file_path = ',file_path)
#     with open(file_path,'wb') as f:
#         f.write(res.content)
#
#
# def douban_movies(url):
#     #首先构建请求头 ，模拟浏览器请求头
#     headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
#     # # 打开链接，并得到返回值
#     res = requests.get(url,headers=headers)
#     # 创建Html解析器
#     moviesParser = MoviesParser()
#     # 解析Html数据
#     moviesParser.feed(res.text)
#     return moviesParser.movies
#
# if __name__ == '__main__':
#     url_str = 'https://movie.douban.com/cinema/nowplaying/shenzhen/'
#     movies_res = douban_movies(url_str)
#
#     import json
#     json_str = json.dumps(movies_res,sort_keys=True,indent=4,separators=(',',': '))
#     # 打印json数据
#     print(json_str)

import sys
reload(sys)
sys.setdefaultencoding('utf8')
from bs4 import BeautifulSoup
import re
import urllib2
import xlwt

#得到页面全部内容
def askURL(url):
    request = urllib2.Request(url)#发送请求
    try:
        response = urllib2.urlopen(request)#取得响应
        html= response.read()#获取网页内容
        #print html
    except urllib2.URLError, e:
        if hasattr(e,"code"):
            print e.code
        if hasattr(e,"reason"):
            print e.reason
    return html

#获取相关内容
def getData(baseurl):
    findLink=re.compile(r'<a href="(.*?)">')#找到影片详情链接
    findImgSrc=re.compile(r'<img.*src="(.*jpg)"',re.S)#找到影片图片
    findTitle=re.compile(r'<span class="title">(.*)</span>')#找到片名
    #找到评分
    findRating=re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
    #找到评价人数
    findJudge=re.compile(r'<span>(\d*)人评价</span>')
    #找到概况
    findInq=re.compile(r'<span class="inq">(.*)</span>')
    #找到影片相关内容：导演，主演，年份，地区，类别
    findBd=re.compile(r'<p class="">(.*?)</p>',re.S)
    #去掉无关内容
    remove=re.compile(r'                            |\n|</br>|\.*')
    datalist=[]
    for i in range(0,10):
        url=baseurl+str(i*25)
        html=askURL(url)
        soup = BeautifulSoup(html,'lxml')
        for item in soup.find_all('div',class_='item'):#找到每一个影片项
            data=[]
            item=str(item)#转换成字符串
            #print item
            link=re.findall(findLink,item)[0]
            data.append(link)#添加详情链接
            imgSrc=re.findall(findImgSrc,item)[0]
            data.append(imgSrc)#添加图片链接
            titles=re.findall(findTitle,item)
            #片名可能只有一个中文名，没有外国名
            if(len(titles)==2):
                ctitle=titles[0]
                data.append(ctitle)#添加中文片名
                otitle=titles[1].replace(" / ","")#去掉无关符号
                data.append(otitle)#添加外国片名
            else:
                data.append(titles[0])#添加中文片名
                data.append(' ')#留空
            rating=re.findall(findRating,item)[0]
            data.append(rating)#添加评分
            judgeNum=re.findall(findJudge,item)[0]
            data.append(judgeNum)#添加评论人数
            inq=re.findall(findInq,item)
            #可能没有概况
            if len(inq)!=0:
                inq=inq[0].replace("。","")#去掉句号
                data.append(inq)#添加概况
            else:
                data.append(' ')#留空
            bd=re.findall(findBd,item)[0]
            bd=re.sub(remove,"",bd)
            bd=re.sub('<br>'," ",bd)#去掉<br>
            bd=re.sub('/'," ",bd)#替换/
            #data.append(bd)
            words=bd.split(" ")
            for s in words:
                if len(s)!=0 and s!=' ':#去掉空白内容
                     data.append(s)
            #主演有可能因为导演内容太长而没有
            if(len(data)!=12):
                data.insert(8,' ')#留空
            datalist.append(data)
    return datalist

#将相关数据写入excel中
def saveData(datalist,savepath):
    book=xlwt.Workbook(encoding='utf-8',style_compression=0)
    sheet=book.add_sheet('豆瓣电影Top250',cell_overwrite_ok=True)
    col=('电影详情链接','图片链接','影片中文名','影片外国名',
                '评分','评价数','概况','导演','主演','年份','地区','类别')
    for i in range(0,12):
        sheet.write(0,i,col[i])#列名
    for i in range(0,250):
        data=datalist[i]
        for j in range(0,12):
            sheet.write(i+1,j,data[j])#数据
    book.save(savepath)#保存

def main():
    baseurl='https://movie.douban.com/top250?start='
    datalist=getData(baseurl)
    savapath=u'douban_Top250.xlsx'
    saveData(datalist,savapath)

main()