# 使用requests爬豆瓣正在上映的电影
from html.parser import HTMLParser
import requests


class MoviesParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.movies = []
        self.img_into_movie = False
        self.a_into_movie = False

    def handle_starttag(self, tag, attrs):
        # 根据属性名称取值
        def _attr(attrs,attr_name):
            for attr in attrs:
                if attr[0] == attr_name:
                    return attr[1]
            return None
        # 取出属性值
        if tag == 'li' and _attr(attrs,'data-title') and _attr(attrs,'data-category') == 'nowplaying':
            movie = {}
            movie['title'] = _attr(attrs,'data-title')
            movie['score'] = _attr(attrs,'data-score')
            movie['star'] = _attr(attrs,'data-star')
            movie['duration'] = _attr(attrs,'data-duration')
            movie['region'] = _attr(attrs,'data-region')
            movie['director'] = _attr(attrs,'data-director')
            movie['actors'] = _attr(attrs,'data-actors')
            self.movies.append(movie)
            self.img_into_movie = True
            self.a_into_movie = True

        #获取海报图片
        if tag == 'img' and self.img_into_movie:
            self.img_into_movie = False
            img_src = _attr(attrs,'src')
            movie = self.movies[len(self.movies) -1]
            movie['poster_url'] = img_src
            donwload_poster_url(img_src)

        if tag == 'a' and self.a_into_movie:
            if _attr(attrs,'data-psource') == 'title':
                self.a_into_movie = False
                movie_url = _attr(attrs,'href')
                movie = self.movies[len(self.movies) -1]
                movie['movie_url'] = movie_url


# 下载图片
def donwload_poster_url(url):
    res = requests.get(url)
    file_name = str.split(url,'/')[-1]
    file_path = 'poster_img/' + file_name
    print('download img file_path = ',file_path)
    with open(file_path,'wb') as f:
        f.write(res.content)


def douban_movies(url):
    #首先构建请求头 ，模拟浏览器请求头
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    # # 打开链接，并得到返回值
    res = requests.get(url,headers=headers)
    # 创建Html解析器
    moviesParser = MoviesParser()
    # 解析Html数据
    moviesParser.feed(res.text)
    return moviesParser.movies

if __name__ == '__main__':
    url_str = 'https://movie.douban.com/cinema/nowplaying/shenzhen/'
    movies_res = douban_movies(url_str)

    import json
    json_str = json.dumps(movies_res,sort_keys=True,indent=4,separators=(',',': '))
    # 打印json数据
    print(json_str)