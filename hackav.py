#_*_coding:utf-8_*_
import urllib2
import cookielib
import requests
from bs4 import BeautifulSoup
import MySQLdb
import time
import random



class JuneSpider:
    def __init__(self):
        # self.connect=MySQLdb.connect(host='127.0.0.1',user='root',passwd='asd123456',db='hackav',charset='utf8')
        # self.cursor=self.connect.cursor()
        self.headers={
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

    def hackav_all_post_index_get(self,url1=None):
        cookie = cookielib.LWPCookieJar()
        cookiehandler = urllib2.HTTPCookieProcessor(cookie)
        openner = urllib2.build_opener(cookiehandler)

        request = urllib2.Request(url=url1, headers=self.headers)
        response = openner.open(request)
        responsesoup = BeautifulSoup(response.read(), 'lxml')
        data = responsesoup.select('#threadlisttableid > tbody')
        for i in data:
            if i.select('tr > th > a.s.xst'):
                title = i.select('tr > th > a.s.xst')[0].text  # 帖子标题
                print title
                href = i.select('tr > th > a.s.xst')[0].get('href')
                print href
                publisher = i.select('tr > td > cite > a')[0].text  # 发帖人
                print publisher
                publishtime = i.select('tr > td > em > span')[0].text
                print publishtime
                reply = i.select('tr > td.num > a')[0].text  # huifushu
                print reply
                viewnumber = i.select('tr > td.num > em')[0].text  # 查看数
                print viewnumber
                lastviewer = i.select('tr > td:nth-of-type(4) > cite')[0].text  # 最后发稿人
                print lastviewer
                lastviewtime = i.select('tr > td:nth-of-type(4) > em > a')[0].text
                print lastviewtime

                if i.select('tr > th > img[alt="agree"]'):
                    print 'been agree'
                    beenagree = 1
                else:
                    print 'not been agree'
                    beenagree = 0
                if i.select('tr > th > img[alt="digest"]'):
                    print '精华'
                    isdigest = 1
                else:
                    print '非精华'
                    isdigest = 0
                if i.select('tr > th > img[alt="heatlevel"]'):
                    print i.select('tr > th > img[alt="heatlevel"]')[0].get('title')
                    hotvalue = 1
                else:
                    print '热度0'
                    hotvalue = 0
                if i.select('tr > th > img[alt="attach_img"]'):
                    print '有图片附件'
                    pictureattachment = 1
                else:
                    print '没有图片附件'
                    pictureattachment = 0
                if i.select('tr > th > img[alt="absmiddle"]'):
                    print '恩，有附件'
                    mallattachment = 1
                else:
                    print '额,木有附件'
                    mallattachment = 0
                connect = MySQLdb.connect(host='127.0.0.1', user='root', passwd='asd123456', db='hackav',
                                          charset='utf8')
                cursor = connect.cursor()
                sql1 = 'INSERT INTO all_post_index(title,href,isdigest,beenagree,hotvalue,mallattachment,pictureattachment,pusher,publishtime,lastestviewtime,reply,viewnumber,lastestviewer) VALUE ("%s","%s","%d","%d"' \
                       ',"%d","%d","%d","%s","%s","%s","%d","%d","%s")' % (
                       title, href, int(isdigest), int(beenagree), int(hotvalue), int(mallattachment),
                       int(pictureattachment), publisher, publishtime, lastviewtime, int(reply), int(viewnumber),
                       lastviewer)
                try:
                    cursor.execute(sql1)
                    connect.commit()
                except Exception as e:
                    print e
                    print '重复了'
                print '\n'

        # urlsplit= response.url.split('forum-11-')
        nextdata = responsesoup.select('#pgt > blockquote > p > span > div > a.nxt')
        print nextdata
        if nextdata:
            nexturl = nextdata[0].get('href')
            time.sleep(random.randint(2, 5))
            print nexturl
            self.hackav_all_post_index_get(url1=nexturl)
    def hackav_all_post_index_get_lunch(self):
        urls=['http://bbs.hackav.com/forum-11-1.html',
              'http://bbs.hackav.com/forum-29-1.html',
              'http://bbs.hackav.com/forum-19-1.html',
              'http://bbs.hackav.com/forum-6-1.html',
              'http://bbs.hackav.com/forum-26-1.html',
              'http://bbs.hackav.com/forum-27-1.html',
              'http://bbs.hackav.com/forum-46-1.html',
              'http://bbs.hackav.com/forum-89-1.html',
              'http://bbs.hackav.com/forum-62-1.html',
              'http://bbs.hackav.com/forum-28-1.html',
              'http://bbs.hackav.com/forum-4-1.html',
              'http://bbs.hackav.com/forum-32-1.html',
              'http://bbs.hackav.com/forum-35-1.html',
              'http://bbs.hackav.com/forum-76-1.html'
              ]
        for i in urls:
            self.hackav_all_post_index_get(url1=i)  # 启动对应的页面信息抓取
    def hackav_all_post_detail_get(self,url1=None,retry=2):#后来发现有些网站需要特定cookie，在这个模式下，只需访问两次即可。
        connect = MySQLdb.connect(host='127.0.0.1', user='root', passwd='asd123456', db='hackav',
                                  charset='utf8')
        cursor = connect.cursor()
        cookie1 = cookielib.LWPCookieJar()
        handlers = urllib2.HTTPCookieProcessor(cookie1)
        openner = urllib2.build_opener(handlers)
        print url1
        if url1:
            request1 = urllib2.Request(url=url1, headers=self.headers)
        else:
            return
        response = openner.open(request1)

        while len(response.read())<2000:#开始处理蛋疼的函数
            data1=response.read()

            response=openner.open(request1)
            print 1
            time.sleep(3)
        datasoup = BeautifulSoup(response.read(), 'lxml')
        print datasoup
        for j in datasoup.select('#postlist > div'):
            # print j.text
            print ' in for '
            try:
                floor = j.select('td.plc > div.pi > strong > a')[0].text.replace('\n', '')  # 发帖楼层
                print floor
                one = j.select('td.plc > div.pi > div.pti > div.authi')
                if one:
                    publishtime = one[0].text.replace('\n', '').split('|')[0].split(u'发表于 ')[1]  # 发帖时间
                    print publishtime
                content = j.select('td.plc > div.pct > div.pcb > div > table')[0].text.replace("'", "\\'").replace('"',
                                                                                                                   '\\"')  # 帖子内容
                print content
                pusher = j.select(' div.pi > div')[0].text  # 发帖人
                print pusher
                pusherhref = j.select('div.pi > div.authi > a')[0].get('href')
                print pusherhref
                ownner = url1
                print ownner

                sql21 = 'INSERT INTO all_post_detail (floor,ownerhref,pusherhref,pusher,content,publishtime) VALUE ("%s","%s","%s","%s","%s","%s")' % (
                    floor, ownner, pusherhref, pusher, content, publishtime)
                cursor.execute(sql21)
                connect.commit()
            except Exception as e:
                print e, 'maybe has no replay'
        time.sleep(random.randint(2, 5))

        nextdata = datasoup.select('#pgt > div > div > a.nxt')
        if nextdata:
            nexturl = nextdata[0].get('href')
            time.sleep(random.randint(2, 5))
            print nexturl
            self.hackav_all_post_detail_get(url1=nexturl)
    def hackav_all_post_detail_get_lunch(self):
        connect = MySQLdb.connect(host='127.0.0.1', user='root', passwd='asd123456', db='hackav',
                                  charset='utf8')
        cursor = connect.cursor()
        sql2 = 'SELECT href FROM all_post_index WHERE dealed=0'
        cursor.execute(sql2)
        data = cursor.fetchall()

        for i in data:
            self.hackav_all_post_detail_get(url1=i[0])  # 启动对应的页面信息抓取
            sql21='UPDATE hackav.all_post_index SET dealed=1 WHERE href ="%s"'%i[0]
            cursor.execute(sql21)
            connect.commit()



    # def hackbase_bbs_index_get(self):




if __name__ == '__main__':
    thisclass=JuneSpider()
    # thisclass.hackav_original_post_index()
    # thisclass.hackav_original_post_detail_get_lunch()
    # thisclass.hackav_all_post_detail_get_lunch()