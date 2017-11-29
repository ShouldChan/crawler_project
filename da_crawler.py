# coding:utf-8
import urllib2
import sqlite3
import re
import string
import time
import Queue
import threading
from bs4 import BeautifulSoup


# 扩充个人主页列表的线程，输入为已备份主页队列qSaved，输出为已扩充主页队列qExtended和待处理
class ExtendProfileThread(threading.Thread):
    # 初始化
    def __init__(self, thread_name, qsaved, qextended, qprofile, repeat=1000):
        threading.Thread.__init__(self, name=thread_name)
        self.input = qsaved
        self.output = qextended
        self.recycle = qprofile
        self.indexUrl = ''
        self.remaincount = repeat
        self.isRunning = 0

    # 读取首页（仅在首页地址传入时执行）
    def readIndex(self):
        url_legal_pattern = re.compile('https://.*')  # 用于检查url合法性的正则表达式模式
        strip_tag_pattern = re.compile('</?\w+[^>]*>')  # 用于去除html标签的正则表达式模式
        # 检查URL合法性
        match = url_legal_pattern.search(indexUrl)
        if not match:
            print 'Illegal Index URL:', indexUrl
            return -1
            # 读取页面
        try:
            site = urllib2.urlopen(indexUrl, timeout=10)
            content = site.read()
        except:
            print 'Time out for index:', indexUrl
            return -1
        # 分析HTML结构
        soup = BeautifulSoup(content, 'html5lib')
        pagetitle = re.sub(strip_tag_pattern, '', soup.html.head.title.__str__())
        print '>>Index Page: ' + pagetitle + '<<'
        # 提取title和url信息
        articles = soup.findAll('a', attrs={'href': True, 'title': True, 'class': 'thumb'})
        for item in articles:
            url = item['href']
            self.recycle.put(url[:url.find('art/')])
            self.remaincount = self.remaincount - 1
        site.close()
        return 0

    # 扩充qProfile
    def extendProfile(self):
        # 满足给定扩展次数则线程结束
        if self.remaincount <= 0:
            print 'Extend repeat finish'
            isRunning = 0
            return -1
        try:
            url = self.input.get(block=False)
        except Queue.Empty:
            return 1  # 用于记录qSaved为空重试的次数
        self.output.put(url)  # 将取出的url直接放入qExtended
        time.sleep(0.5)  # 未必需要，防止访问太频繁被服务器打回
        retry = 6  # 超时重试5次+初始1次
        while retry:
            try:
                page = urllib2.urlopen(url, timeout=10)
                content = page.read()
                page.close()
            except:
                if retry > 1:
                    print 'Time out for watchers:', url
                    print 'Retry', 7 - retry
                retry = retry - 1
                if not retry:
                    print 'Cannot connect to url:', url
                    return 0
                continue
            retry = 0
        print 'Searching for watchers:', url
        # 分析页面，使用html5lib，因为lxml有额外空格的bug，严重影响分析
        soup = BeautifulSoup(content, 'html5lib')
        # 去掉包含id="groups-list-xxxx"的p字段，因为这是group列表而非watcher列表
        groupsp = soup.findAll('p', attrs={'id': re.compile('groups-list-.*')})
        for item in groupsp:
            item.extract()
            # 提取watcher列表
        watchers1 = soup.findAll('a', attrs={'class': 'u', 'href': True})
        watchers2 = soup.findAll('a', attrs={'target': '_self', 'href': True})
        watchers = watchers1 + watchers2
        for watcher in watchers:
            if not watcher['href'] == url:
                try:
                    self.recycle.put(watcher['href'], timeout=30)  # 将watcher的url放入待处理队列等待备份
                except Queue.Full:
                    print 'qProfile Full for 30s'
                self.remaincount = self.remaincount - 1
        return 0

    # 扩充qProfile
    def extendProfile(self):
        # 满足给定扩展次数则线程结束
        if self.remaincount <= 0:
            print 'Extend repeat finish'
            isRunning = 0
            return -1
        try:
            url = self.input.get(block=False)
        except Queue.Empty:
            return 1  # 用于记录qSaved为空重试的次数
        self.output.put(url)  # 将取出的url直接放入qExtended
        time.sleep(0.5)  # 未必需要，防止访问太频繁被服务器打回
        retry = 6  # 超时重试5次+初始1次
        while retry:
            try:
                page = urllib2.urlopen(url, timeout=10)
                content = page.read()
                page.close()
            except:
                if retry > 1:
                    print 'Time out for watchers:', url
                    print 'Retry', 7 - retry
                retry = retry - 1
                if not retry:
                    print 'Cannot connect to url:', url
                    return 0
                continue
            retry = 0
        print 'Searching for watchers:', url
        # 分析页面，使用html5lib，因为lxml有额外空格的bug，严重影响分析
        soup = BeautifulSoup(content, 'html5lib')
        # 去掉包含id="groups-list-xxxx"的p字段，因为这是group列表而非watcher列表
        groupsp = soup.findAll('p', attrs={'id': re.compile('groups-list-.*')})
        for item in groupsp:
            item.extract()
            # 提取watcher列表
        watchers1 = soup.findAll('a', attrs={'class': 'u', 'href': True})
        watchers2 = soup.findAll('a', attrs={'target': '_self', 'href': True})
        watchers = watchers1 + watchers2
        for watcher in watchers:
            if not watcher['href'] == url:
                try:
                    self.recycle.put(watcher['href'], timeout=30)  # 将watcher的url放入待处理队列等待备份
                except Queue.Full:
                    print 'qProfile Full for 30s'
                self.remaincount = self.remaincount - 1
        return 0

    # 线程运行
    def run(self):
        self.isRunning = 1
        global threadStatus
        threadStatus += 10000
        ret = 0
        retry = 0
        print 'Extender waiting...\n'
        while not self.indexUrl:
            continue  # 等待主线程传入启动指令
        if not self.indexUrl == '/recover/':
            self.readIndex()
        while self.isRunning:
            ret = self.extendProfile()
            if ret == -1:
                self.isRunning = 0
                break
            elif ret == 1:
                retry = retry + ret
                time.sleep(3)  # 等待3s再尝试从qSaved读入数据
            else:
                retry = 0
            if retry >= 3:  # 连续三次无法从qSaved读入数据，则结束运行
                self.isRunning = 0
                break
        threadStatus -= 10000
        print '!!Thread exit: extend, status:', threadStatus


# 抓取画廊的线程，输入为已扩充主页队列qExtended，输出为已处理主页队列qFinished和待评分图片队列qRanking
class ExtractGalleryThread(threading.Thread):
    # 初始化
    def __init__(self, thread_name, qextended, qranking, qfinished):
        threading.Thread.__init__(self, name=thread_name)
        self.input = qextended
        self.finish = qfinished
        self.output = qranking
        self.isRunning = 0

        # 抓取画廊

    def dragGallery(self):
        try:
            url = self.input.get(timeout=60)
            self.finish.put(url, timeout=60)
        except Queue.Empty:
            print 'qExtended empty for 60s'
            return 1
        except Queue.Full:
            print 'qFinished full for 60s'
            return -1
            # 开始浏览画廊页面，最多1000页（每页通常是24张）
        for page in range(0, 1000):
            galleryurl = url + 'gallery/?catpath=%2F&offset=' + str(page * 24)
            pagetitle, titles, urls = self.getTitleAndUrl(galleryurl)
            if pagetitle == 'empty section':
                break
            elif pagetitle == 'is a group':
                break
            elif pagetitle == 'cannot open':
                break
            works, authors, dates, categories = self.splitTitle(titles)
            if urls and works and authors and dates and categories:
                print '>>Page', page + 1, 'in', pagetitle, 'processed.'
                for i in range(0, len(urls)):
                    # 将信息作为元组存入qRanking
                    combination = (works[i], authors[i], dates[i], categories[i], urls[i])
                    try:
                        self.output.put(combination, timeout=60)
                    except Queue.Full:
                        print 'qRanking full for 60s'
                        return -1
        return 0


        # 提取单个画廊页面中所有作品的标题和url

    def getTitleAndUrl(self, galleryurl):
        url_legal_pattern = re.compile('https://.*')  # 用于检查url合法性的正则表达式模式
        strip_tag_pattern = re.compile('</?\w+[^>]*>')  # 用于去除html标签的正则表达式模式
        pagetitle = ''
        titles = []
        urls = []
        # 检查URL合法性
        match = url_legal_pattern.search(galleryurl)
        if not match:
            print 'Illegal Gallery URL:', self.indexUrl
            return pagetitle, titles, urls
            # 读取页面
        count_try = 6
        while count_try:
            try:
                page = urllib2.urlopen(galleryurl, timeout=10)
                content = page.read()
                page.close()
                break
            except:
                print 'Time out for page:', galleryurl
                count_try -= 1
                if count_try:
                    print 'Retry:', 6 - count_try
                    continue
                else:
                    print 'Cannot open gallery:', galleryurl
                    return 'cannot open', titles, urls
                    # 判断该链接是否是一个小组
        if content.find('Scrapbook') == -1:
            return 'is a group', titles, urls
            # 判断是否空画廊
        if content.find('This section has no deviations yet!') != -1:
            return 'empty section', titles, urls
            # 分析HTML结构
        soup = BeautifulSoup(content, 'html5lib')
        pagetitle = re.sub(strip_tag_pattern, '', soup.html.head.title.__str__())
        # 提取title和url信息
        articles = soup.findAll('a', attrs={'href': True, 'title': True, 'class': 'thumb'})
        for item in articles:
            titles.append(item['title'])
            urls.append(item['href'])
        return pagetitle, titles, urls

        # 进一步将标题分解为详细信息

    def splitTitle(self, titles):
        works = []
        authors = []
        dates = []
        categories = []
        for title in titles:
            tmp1 = title.split(' by ')
            # 有多个by时将除了最后一项之外的各项合并，解决标题中含有' by '的情况
            if len(tmp1) > 2:
                for i in range(1, len(tmp1) - 2):
                    tmp1[0] = tmp1[0] + ' by ' + tmp1[i]
                tmp1[1] = tmp1[len(tmp1) - 1]
            works.append(tmp1[0].strip())
            tmp2 = tmp1[1].split(',', 2)
            authors.append(tmp2[0].strip())
            if not len(tmp2) == 3:
                print 'Coma number error:' + title
                return works, authors, dates, categories
            tmps = tmp2[1] + ',' + tmp2[2]
            tmp4 = tmps.split(' in ')
            if not len(tmp4) == 2:
                for i in range(2, len(tmp4)):
                    tmp4[1] = tmp4[1] + tmp4[i]
            dates.append(tmp4[0].strip())
            categories.append(tmp4[1].split(' > '))
            for item in categories:
                for item2 in item:
                    item2.strip()
        return works, authors, dates, categories

        # 线程运行

    def run(self):
        self.isRunning = 1
        global threadStatus
        threadStatus += 100
        while self.isRunning:
            ret = self.dragGallery()
            # 发现Extender线程已经退出且qExtended序列为空，则退出此线程
            if ret and threadStatus < 10000:
                self.isRunning = 0
                threadStatus -= 100
                print '!!Thread exit: extract, status:', threadStatus
                break


# 评分线程，输入为待评分队列qRanking，输出为已评分队列qRanked
class RankPictureThread(threading.Thread):
    # 初始化
    def __init__(self, thread_name, qranking, qranked):
        threading.Thread.__init__(self, name=thread_name)
        self.input = qranking
        self.output = qranked
        self.isRunning = 0


    # 获得图片收藏数作为评分
    def getPicFavs(self):
        try:
            combination = self.input.get(timeout=60)
            work = combination[0]
            author = combination[1]
            date = combination[2]
            category = combination[3]
            url = combination[4]
        except Queue.Empty:
            print 'qRanking empty for 60s'
            return 1
            # 开始提取收藏数
        num_begin = 0
        count_try = 0
        # 有时会出现奇怪的问题，HTML文件没有完整载入，此时重新读取
        while num_begin < 10000:
            count_try = count_try + 1
            try:
                img = urllib2.urlopen(url, timeout=10)
                content = img.read()
                img.close()
            except:
                if count_try > 10:
                    break
                print 'Time out for favs:', url
                print 'Retry:', count_try
                continue
            num_begin = content.find('</span>Favourites:</span>') + len('</span>Favourites:</span>')
            # 重复10次仍然得不到评分的图片记为-1分
        if count_try > 10:
            score = -1
        else:
            number = '0'
            for i in range(num_begin, num_begin + 20):
                if content[i] == '[' or content[i] == '<':
                    break;
                number = number + content[i]
            try:
                number = number.replace(',', '')
                number = number.replace(' ', '')
                score = string.atoi(number)
            except:
                print 'Cannot get score:', number
                print 'The url is:', url
                score = -1  # 某张图片无法读取收藏数是bug，但报告后继续运行
            # 交给下一函数提取打分者列表
            ret = self.WhoFavedThis(work, author, date, score, category, url)
            return ret

    # 进一步获得打分者列表
    def WhoFavedThis(self, work, author, date, score, category, url):
        # score为0或-1
        if score < 1:
            follower = 'NULL'
            tupleout = (work, author, date, score, category, url, follower)
            try:
                self.output.put(tupleout, timeout=60)
            except Queue.Full:
                print 'qRanked full for 60s'
                return -1
            return 0
        # 找到作品ID
        seg = url.split('-')
        picid = seg[-1]
        for page in range(0, 100):
            favurl = 'https://www.deviantart.com/deviation/' + picid + '/favourites?offset=' + str(page * 100)
            for count_try in range(1, 7):
                try:
                    favpage = urllib2.urlopen(favurl, timeout=10)
                    content = favpage.read()
                    favpage.close()
                    break
                except:
                    if count_try < 6:
                        print 'Timeout for favlist:', picid
                        print 'Retry', count_try
                    else:
                        print 'Cannot get favlist:', picid
                        return -1
                        # 提取列表
            soup = BeautifulSoup(content, 'html5lib')
            favlist = soup.findAll('a', attrs={'class': 'whoUserLink'})
            if len(favlist) == 0:
                return 0
            for item in favlist:
                try:
                    follower = item['href']
                except:
                    print 'Error for favlist:', item
                    continue
                tupleout = (work, author, date, score, category, url, follower)
                try:
                    self.output.put(tupleout, timeout=60)
                except Queue.Full:
                    print 'qRanked full for 60s'
                    return -1

    # 线程运行
    def run(self):
        self.isRunning = 1
        global threadStatus
        threadStatus += 1
        while self.isRunning:
            ret = self.getPicFavs()
            # 发现qRanking为空且所有Dragger线程已经退出，则结束线程
            if ret and threadStatus < 100:
                self.isRunning = 0
                threadStatus -= 1
                print '!!Thread exit: rank, status:', threadStatus
                break


# 备份个人主页列表的线程，输入为待处理主页队列qProfile和已处理主页队列qFinished，输出为已备份主页队列qSaved
class BackupProfileThread(threading.Thread):
    # 初始化
    def __init__(self, thread_name, qprofile, qsaved, qfinished, qextended, dbname, pextender, noextend):
        threading.Thread.__init__(self, name=thread_name)
        self.input = qprofile
        self.remove = qfinished
        self.output = qsaved
        self.extend = qextended
        self.dbName = dbname
        self.isRunning = 0
        self.extender = pextender
        self.nomoreextend = noextend

        # 连接到数据库文件

    def linkDatabase(self):
        self.db = sqlite3.connect('./' + self.dbName)
        self.cur = self.db.cursor()
        self.cur.execute('CREATE TABLE IF NOT EXISTS Profile(' + \
                         'ID integer PRIMARY KEY AUTOINCREMENT, ' + \
                         'Url varchar(200), ' + \
                         'Processed integer)')

        # 从中断恢复数据库恢复队列到qExtended或qSaved，依用户指令而定

    def recoverProfile(self):
        try:
            self.cur.execute('SELECT Url FROM Profile WHERE Processed = 0')
            lst = self.cur.fetchall()
            if lst:
                print len(lst), 'profile(s) recovered.'
                for item in lst:
                    if self.nomoreextend:
                        self.extend.put(item[0], block=False)
                    else:
                        self.output.put(item[0], block=False)  # 恢复时qSaved一般不应该填满
                return 1
            else:
                return 0
        except Queue.Full:
            if self.noextend:
                print 'qExtended full while recovering'
            else:
                print 'qSaved full while recovering'
            return 1
        except:
            return 0

            # 将url备份到中断恢复数据库并输出到qSaved

    def saveProfile(self):
        try:
            url = self.input.get(block=False)
        except Queue.Empty:
            return 1
            # 跳过某些只有'#'的url
        if url == '#':
            return 0
        url_legal_pattern = re.compile('https://.*')  # 用于检查url合法性的正则表达式模式
        # 检查url合法性
        match = url_legal_pattern.search(url)
        if not match:
            print 'Illegal Profile URL:', url
            return 1
            # 检查数据库中是否已存在此url
        self.cur.execute('SELECT ID FROM Profile WHERE Url = "' + url + '"''"')
        tmp = self.cur.fetchall()
        if tmp:
            return 0
        # 保存此url
        try:
            cmd = 'INSERT INTO Profile (Url, Processed) ' + \
                  'VALUES("' + url + '", 0)'
            self.cur.execute(cmd)
            self.db.commit()
            self.output.put(url, timeout=60)
        except Queue.Full:
            print 'qSaved full for 60s'
            return 1
        except sqlite3.Error:
            print 'Backup profile database error, command:', cmd
        return 0

    # 标记中断恢复数据库中处理完毕的url
    def updateProfile(self):
        try:
            url = self.remove.get(block=False)
            cmd = 'UPDATE Profile SET Processed = 1 WHERE Url = "' + url + '"'
            self.cur.execute(cmd)
            self.db.commit()
        except Queue.Empty:
            return 1
        except sqlite3.Error:
            print 'Update profile database error, command:', cmd
        return 0

        # 线程运行

    def run(self):
        self.linkDatabase()
        ret = self.recoverProfile()
        if ret:
            extender.indexUrl = '/recover/'
            print 'Recovered from database'
            if self.nomoreextend:
                extender.isRunning = 0
        else:
            extender.indexUrl = indexUrl
        self.isRunning = 1
        while self.isRunning:
            ret1 = self.saveProfile()
            ret2 = self.updateProfile()
        self.db.close()
        print '!!Thread exit: savior'


# 维护主数据库的线程，输入为已评分队列qRanked，没有输出队列
class mainDatabaseHandlerThread(threading.Thread):
    # 初始化
    def __init__(self, thread_name, qranked, dbname):
        threading.Thread.__init__(self, name=thread_name)
        self.input = qranked
        self.dbName = dbname
        self.isRunning = 0

        # 连接到数据库

    def linkDatabase(self):
        self.db = sqlite3.connect('./' + self.dbName)
        self.cur = self.db.cursor()
        self.cur.execute('CREATE TABLE IF NOT EXISTS Art(' + \
                         'ID integer PRIMARY KEY AUTOINCREMENT, ' + \
                         'Title varchar(100), ' + \
                         'Author varchar(50), ' + \
                         'Date varchar(50), ' + \
                         'Score integer, ' + \
                         'Url varchar(200), ' + \
                         'Category_1 varchar(50), ' + \
                         'Category_2 varchar(50), ' + \
                         'Category_3 varchar(50), ' + \
                         'Category_4 varchar(50), ' + \
                         'Category_5 varchar(50), ' + \
                         'Category_6 varchar(50), ' + \
                         'Follower varchar(200))')

        # 保存到数据库

    def saveToDB(self):
        try:
            tuplein = self.input.get(timeout=60)
        except Queue.Empty:
            print 'qRanked empty for 60s'
            return 1
        work = tuplein[0]
        author = tuplein[1]
        date = tuplein[2]
        score = tuplein[3]
        category = tuplein[4]
        url = tuplein[5]
        follower = tuplein[6]
        # 查询数据库，判断是否重复
        self.cur.execute('SELECT ID FROM Art WHERE Url = "' + url + '" AND Follower = "' + follower + '"''"')
        lst = self.cur.fetchone()
        if lst:
            return 0
        # 将类别项拆分成小类别再组合为SQL语句
        category_str = '"'
        for item in category:
            category_str = category_str + ', "' + item + '"''"'
        for j in range(len(category) + 1, 7):
            category_str = category_str + ' ,NULL'
        # 写入数据库
        cmd = 'INSERT INTO Art VALUES(NULL, ' + \
              '"' + work + '", ' + \
              '"''"' + author + '", ' + \
              '"' + date + '", ' + \
              str(score) + ', ' + \
              '"''"' + url + \
              category_str + ', ' + \
              '"' + follower + '")'
        try:
            self.cur.execute(cmd)
        except sqlite3.Error, e:
            print 'Main database error, command:', cmd
            print e
        self.db.commit()
        return 0

        # 线程运行

    def run(self):
        self.linkDatabase()
        self.isRunning = 1
        while self.isRunning:
            ret = self.saveToDB()
        self.db.close()
        print '!!Thread exit: keeper'

        # -------------------------------------------------------------------------#


# 主入口
if __name__ == '__main__':
    noextend = 1

    indexUrl = 'https://www.deviantart.com/'
    qProfile = Queue.Queue(1000)
    qSaved = Queue.Queue(1000)
    qExtended = Queue.Queue(1000)
    qFinished = Queue.Queue(1000)
    qRanking = Queue.Queue(1000)
    qRanked = Queue.Queue(1000)

    # 线程状态标志，供后续线程判断前驱线程是否退出
    # 这是一个五位数，各数位表示还在运行的该类线程的个数
    # 万位表示Extender线程，千、百位表示Dragger线程，十、个位表示Ranker线程
    threadStatus = 0

    # 各线程
    extender = ExtendProfileThread('Extender', qSaved, qExtended, qProfile, repeat=2000)
    savior = BackupProfileThread('Savior', qProfile, qSaved, qFinished, qExtended, 'deviantArtProfile.db', extender,
                                 noextend)
    keeper = mainDatabaseHandlerThread('Keeper', qRanked, 'deviantArtThreaded.db')
    dragger = []
    ranker = []
    for i in range(1, 2):
        dragger.append(ExtractGalleryThread('Dragger' + str(i), qExtended, qRanking, qFinished))
    for i in range(1, 3):
        ranker.append(RankPictureThread('Ranker' + str(i), qRanking, qRanked))
    enumThread = [savior, keeper, extender]
    for item in dragger:
        enumThread.append(item)
    for item in ranker:
        enumThread.append(item)
    for thread in enumThread:
        thread.setDaemon(True)
        thread.start()
        time.sleep(0.1)
    print '------All thread start. Status:', threadStatus, '------'

    # 不等待两个数据库维护线程，它们必须一直运行到其他线程全部结束为止
    for thread in enumThread[2:]:
        thread.join()

    # 结束两个数据库维护线程
    savior.isRunning = 0
    keeper.isRunning = 0
    time.sleep(5)
    print '------All thread end. Status:', threadStatus, '------'
