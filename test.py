#_*_coding:utf-8_*_
import requests
import cookielib
import requests
from bs4 import BeautifulSoup
import chardet
import MySQLdb
import time
import random
import re
import datetime

class JuneSpider:
    def __init__(self):
        self.connect=MySQLdb.connect(host='127.0.0.1',user='root',passwd='asd123456',db='JuneSpider',charset='utf8')
        self.cursor=self.connect.cursor()
        self.headers={
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

    def hackbase_index_get(self):

        def getindex(url1):
            print url1
            response=session1.request(method='GET',url=url1,headers=self.headers)
            data=response.text
            datasoup = BeautifulSoup(data, 'lxml')
            for i in datasoup.select('#threadlisttableid > tbody'):
                try:
                    title = i.select('tr > th > a.s.xst')
                    titletext= title[0].text#帖子标题
                    titlehref= title[0].get('href')#帖子链接

                    auther = i.select('tr > td.by > cite > a')
                    time1 = i.select('tr > td.by > em > span')
                    autherhref= auther[0].get('href')#作者链接
                    authertext= auther[0].text#作者名字
                    authertime= time1[0].text#发帖时间

                    time2 = i.select('tr > td > em > a')

                    lastviewername= auther[1].text#最后一个浏览人的名称
                    lastviewerhref= auther[1].get('href')#最后一个浏览人的链接
                    lastviewertime= time2[0].text#最后一个浏览人的浏览时间
                    if u'昨天' in lastviewertime:
                        time1=datetime.date.today()
                        time2=time1-datetime.timedelta(days=1)
                        lastviewertime=lastviewertime.replace(u'昨天',str(time2))
                    if u'今天' in lastviewertime:
                        lastviewertime=lastviewertime.replace(u'今天',str(datetime.date.today()))

                    if u'昨天' in authertime:
                        time1=datetime.date.today()
                        time2=time1-datetime.timedelta(days=1)
                        authertime=authertime.replace(u'昨天',str(time2))
                    if u'今天' in authertime:
                        authertime=authertime.replace(u'今天',str(datetime.date.today()))

                    print authertime
                    print lastviewertime

                    sqlhackbase='INSERT INTO JuneSpider.index_all_website (href,title,publisher,publishtime,publisherhref,lastviewer,lastviewtime,lastviewerhref,ownerwebsite) VALUE ("%s","%s","%s","%s","%s","%s","%s","%s","bbs.hackbase.com")'\
                        %(titlehref,titletext,authertext,authertime,autherhref,lastviewername,lastviewertime,lastviewerhref)
                    self.cursor.execute(sqlhackbase)
                    self.connect.commit()
                except Exception as e:
                    print e
            nextpage = datasoup.select('#fd_page_top > div.pg > a.nxt')
            if nextpage:
                print response.url
                print nextpage
                nexturl = nextpage[0].get('href')
                print nexturl,'-----!'
                time.sleep(random.randint(2, 5))
                getindex(url1=nexturl)
            else:
                return


        cookie1 = cookielib.LWPCookieJar()
        session1 = requests.session()
        session1.cookies = cookie1
        # handlers = urllib2.HTTPCookieProcessor(cookie1)
        # openner = urllib2.build_opener(handlers)

        urllists=['http://bbs.hackbase.com/forum-1-1.html',
                  'http://bbs.hackbase.com/forum-12-1.html',
                  'http://bbs.hackbase.com/forum-333-1.html',
                  'http://bbs.hackbase.com/forum-269-1.html',
                  'http://bbs.hackbase.com/forum-130-1.html',
                  'http://bbs.hackbase.com/forum-317-1.html',
                  'http://bbs.hackbase.com/forum-276-1.html',
                  'http://bbs.hackbase.com/forum-445-1.html',
                  'http://bbs.hackbase.com/forum-479-1.html',
                  'http://bbs.hackbase.com/forum-454-1.html',
                  'http://bbs.hackbase.com/forum-453-1.html',
                  'http://bbs.hackbase.com/forum-443-1.html',
                  'http://bbs.hackbase.com/forum-444-1.html',
                  ]

        for i in urllists:
            getindex(i)

    def all_detail_get(self):
        session1=requests.session()
        session1.headers=self.headers
        cookie_detail=cookielib.LWPCookieJar()
        session1.cookies=cookie_detail

        def datailget(urldetail):
            response=session1.request(method='GET',url=urldetail)
            data=response.text
            datasoup=BeautifulSoup(data,'lxml')
            for ii in datasoup.select('#postlist > div'):
                try:
                    publishername=None
                    publisherhref=None
                    try:
                        publishername= ii.select(' td.pls > div > div.pi > div > a')[0].text
                        publisherhref= ii.select('td.pls > div > div.pi > div > a')[0].get('href')
                    except Exception as e:
                        publishername='匿名'
                        publisherhref=None
                    content= ii.select('tr > td.plc > div.pct > div.pcb > div > table > tr > td > div')[0].text# tr:nth-child(1) > td.plc > div.pct > div > div.t_fsz > table > tbody > tr
                    publishtime=ii.select(' tr > td.plc > div.pi > div > div.authi > em')[0].text.replace(u'发表于 ','')
                    floor= ii.select('tr > td.plc > div.pi > strong > a > em')[0].text
                    print publishtime

                    sqlsvaedetail='INSERT INTO JuneSpider.detail_post (floor,ownerhref,publisher,publisherhref,content,publishtime) VALUE ("%s","%s","%s","%s","%s","%s")'%(floor,i[0],publishername,publisherhref,content,publishtime)
                    # print sqlsvaedetail
                    self.cursor.execute(sqlsvaedetail)
                    self.connect.commit()
                except Exception as e:
                    print e
            nextpage=datasoup.select('#ct > div.pgs.mtm.mbm.cl > div > a.nxt')
            if nextpage:
                nexturl=nextpage[0].get('href')
                print nexturl
                time.sleep(2)
                datailget(nexturl)
            else:
                return



        sqlselecthref = 'SELECT href FROM index_all_website WHERE dealed is NULL AND ownerwebsite="bbs.hackbase.com"'
        self.cursor.execute(sqlselecthref)
        urllist_need_visti=self.cursor.fetchall()
        for i in urllist_need_visti:
            datailget(i[0])
            sqlsetdealed='UPDATE index_all_website set dealed=1 WHERE href="%s"'%(i[0])
            self.cursor.execute(sqlsetdealed)
            self.connect.commit()

    def heishou_get_index(self):
        urls=['http://www.heishou.com.cn/index.php?page=156']
        cookie1=cookielib.LWPCookieJar()
        session=requests.session()
        session.cookies=cookie1



        def indexget(url1):
            response=session.request(method='GET',url=url1,headers=self.headers)
            datasoup=BeautifulSoup(response.text,'lxml')
            for i in datasoup.select('#J_posts_list > tr'):
                try:
                    title= i.select(' td.subject > p.title')[0].text#title
                    publishername= i.select(' td.subject > p.info > a.J_user_card_show')[0].text#用户
                    publishtime= i.select(' td.subject > p.info > span')[0].text#发帖时间

                    lastreplayername= i.select(' td.subject > p.info > a.J_user_card_show')[1].text#最后回帖人
                    lastreplaytime= i.select(' td.subject > p.info > span')[1].text#回帖时间
                    if len(lastreplaytime)<14:
                        lastreplaytime=publishtime.split('-')[0]+'-'+lastreplaytime
                    replaynum= i.select(' td.num > span > em')[0].text#回复
                    viewnum=i.select(' td.num > span > em')[1].text#浏览

                    titlehref= i.select(' td.subject > p.title > a')[0].get('href')#href
                    publisherhref= i.select(' td.subject > p.info > a.J_user_card_show')[0].get('href')#publisherhref
                    replayerhref= i.select(' td.subject > p.info > a.J_user_card_show')[1].get('href')#viewerhref

                    sqlheishouindex='INSERT INTO JuneSpider.index_all_website (href,title,publishtime,publisher,lastviewtime,lastviewer,ownerwebsite,publisherhref,lastviewerhref,viewernum,replayernum) VALUE ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%d","%d")'%\
                                    (titlehref,title,publishtime,publishername,lastreplaytime,lastreplayername,'www.heishou.com',publisherhref,replayerhref,int(viewnum),int(replaynum))
                    #这里的vireerhref就是replayhref,不同的网站使用不一样.

                    self.cursor.execute(sqlheishouindex)
                    self.connect.commit()
                except Exception as e:
                    print e


            nextpage = datasoup.select('body > div > div.main_wrap > div.main.cc > div.main_body > div > div.J_page_wrap.cc > div > a.pages_next.J_pages_next')
            if nextpage:
                nexturl=nextpage[0].get('href')
                time.sleep(random.randint(2,5))
                try:
                    indexget(nexturl)
                except Exception as e:
                    print e











        for i in urls:
            indexget(i)


    def heishou_get_detail(self):
        session1=requests.session()
        cookie1=cookielib.LWPCookieJar()
        session1.cookies=cookie1
        session1.headers=self.headers

        def heishoudetail(url1):
            respone=session1.request(method='GET',url=url1)

            datasoup=BeautifulSoup(respone.text,'lxml')
            for ii in datasoup.select('#J_posts_list > div'):
                try:
                    publishername= ii.select(' tr > td.floor_left > div > div.name > a')[0].text#用户昵称
                    content= ii.select('#J_read_main > div.editor_content')[0].text#发帖内容
                    publishtime= ii.select('tr > td.box_wrap.floor_right > div.floor_top_tips.cc > span')[0].text.replace(u'发布于：','').rstrip(' ').replace('\t','')+':00'#发帖时间
                    floor= ii.select('tr > td.box_wrap.floor_right > div.floor_top_tips.cc > div > span')[0].text.replace(u'楼','').replace(u'#','')#发帖楼层
                    publisherhref= ii.select(' tr > td.floor_left > div > div.name > a')[0].get('href')


                    sqlheishoudetailinsert='INSERT INTO JuneSpider.detail_post (floor,ownerhref,publisherhref,content,publishtime,publisher) VALUE ("%d","%s","%s","%s","%s","%s")'%(int(floor),i[0],publisherhref,content,publishtime,publishername)
                    print sqlheishoudetailinsert

                    self.cursor.execute(sqlheishoudetailinsert)
                    self.connect.commit()

                except Exception as e:
                    print e

            nextpage=datasoup.select('#floor_reply > div > div > a.pages_next.J_pages_next')
            if nextpage:
                nexturl=nextpage[0].get('href')
                print nexturl
                time.sleep(random.randint(2,5))
                heishoudetail(nexturl)
            else:
                return

        sqlheishoudetailget='SELECT href FROM JuneSpider.index_all_website WHERE ownerwebsite="www.heishou.com"'
        self.cursor.execute(sqlheishoudetailget)
        urls=self.cursor.fetchall()

        for i in urls:
            print i[0]
            heishoudetail(i[0])


    def myhack58_index_get(self):
        session1=requests.session()
        session1.headers=self.headers
        cookie1=cookielib.LWPCookieJar()
        session1.cookies=cookie1


        urls=['http://bbs.myhack58.com/thread.php?fid-39-page-1.html',
              'http://bbs.myhack58.com/thread.php?fid-144-page-1.html',
              'http://bbs.myhack58.com/thread.php?fid-69-page-1.html',
              'http://bbs.myhack58.com/thread.php?fid-179-page-1.html',
              'http://bbs.myhack58.com/thread.php?fid-152-page-1.html',
              'http://bbs.myhack58.com/thread.php?fid-88-page-1.html',
              'http://bbs.myhack58.com/thread.php?fid-160-page-1.html',
              'http://bbs.myhack58.com/thread.php?fid-160-page-1.html',
              ]

        def myhack58indexget(url1):
            response=session1.request(method='GET',url=url1)
            response.encoding='gbk'
            datasoup=BeautifulSoup(response.text,'lxml')
            for ii in datasoup.select('#ajaxtable > tbody > tr.tr3.t_one'):
                print '\n\n'
                try:
                    content= ii.select(' td > h3 > a')[0].text
                    href='http://bbs.myhack58.com/'+ii.select('td > h3 > a')[0].get('href')
                    publishername=ii.select('td.tal.y-style > a.bl')[0].text
                    publishertime=ii.select('td.tal.y-style > div.f10.gray2')[0].text
                    publisherhref='http://bbs.myhack58.com/'+ii.select('td.tal.y-style > a.bl')[0].get('href')
                    replaynum=ii.select(' td.tal.y-style.f10')[0].text
                    lastpublishtime=ii.select('td.tal.y-style > a.f10')[0].text.lstrip(' ').rstrip(' ')
                    lastpublisher=ii.select('td.tal.y-style > span.gray2')[0].text.replace('by: ','')

                    viewernum=replaynum.split('/')[1].replace(' ','')
                    replayernum=replaynum.split('/')[0].replace(' ','')





                    # type1=chardet.detect(content)
                    print content
                    print href
                    print publishername
                    print publisherhref
                    print replaynum
                    print lastpublisher
                    print lastpublishtime
                    print publishertime.replace('\n','')

                    sqlmyhackinsert='INSERT INTO JuneSpider.index_all_website (href,title,publishtime,publisher,lastviewtime,lastviewer,ownerwebsite,publisherhref,dealed,viewernum,replayernum)' \
                                    'VALUE ("%s","%s","%s","%s","%s","%s","bbs.myhack58.com","%s",NULL ,"%d","%d")'%(href,content,publishertime,publishername,lastpublishtime,lastpublisher,publisherhref,int(viewernum),int(replayernum))

                    print sqlmyhackinsert
                    self.cursor.execute(sqlmyhackinsert)
                    self.connect.commit()




                    # print type1
                except Exception as e:
                    print e
            nextpageneed=datasoup.select('#main > div > span.fl > div.pages.cc > span')
            if nextpageneed:
                try:
                    needvisitText=nextpageneed[0].text
                    nextpageneedlist= needvisitText.replace('Pages: ','').split(' ')[0].split('/')
                    print nextpageneedlist
                    nextpagenum=response.url.split('-')[-1].split('.')[0]
                    nextpagenum2= int(nextpagenum)+1
                    print nextpagenum2
                    time.sleep(random.randint(2,5))
                    if nextpagenum2<1000 and nextpagenum2<nextpageneedlist[1]:
                        nexturl=response.url.split('page-')[0]+'page-'+str(nextpagenum2)+'.html'
                        print nexturl
                        # myhack58indexget(nexturl)
                    else:
                        return

                except Exception as e:
                    print e



        for i in urls[:1]:
            myhack58indexget(i)


    def myhack58_detail_get(self):
        session1=requests.session()
        session1.headers=self.headers
        cookie1=cookielib.LWPCookieJar()
        session1.cookies=cookie1

        def myhackdetailget(url1):
            print url1
            response=session1.request(method='GET',url=url1)
            response.encoding='gbk'
            datasoup=BeautifulSoup(response.text,'lxml')
            for ii in datasoup.select('#main > form > div.t5'):
                publishername= ii.select(' tr > th.r_two > div > b > a')[0].text
                publisherhref= 'http://bbs.myhack58.com/'+ii.select(' tr > th.r_two > div > b > a')[0].get('href')
                content= ii.select(' tr > th > div.tpc_content > div.f14')[0].text.replace('"','-')
                publishtime=ii.select(' tr > th > div.tiptop > span.fl.gray')[0].text.replace(u'发表于: ','')
                floor= ii.select(' tr > th > div.tiptop > span.fl > a.s3.b')[0].text.replace('\n','')
                # print '\n\n'

                try:
                    sqlmyhackinsert='INSERT INTO JuneSpider.detail_post (floor,ownerhref,publisher,publisherhref,content,publishtime)VALUE ("%s","%s","%s","%s","%s","%s")'%(floor,i[0],publishername,publisherhref,content,publishtime)
                    print sqlmyhackinsert
                    self.cursor.execute(sqlmyhackinsert)
                    self.connect.commit()
                except Exception as e:
                    print e

            nextpageneedtovisit=datasoup.select('#main > div > span.fl > div.pages.cc > span')
            if nextpageneedtovisit:
                nextpagetext=nextpageneedtovisit[0].text
                nextpagetextlist= nextpagetext.replace('Pages: ','').split(' ')[0].split('/')
                if int(nextpagetextlist[0])<int(nextpagetextlist[1]):
                    nexturl1=None
                    if '-page' in response.url:#太蛋疼
                        thispagenumber=int(response.url.split('-page')[1].replace('-','').split('.')[0])
                        nexturl1=response.url.split('-page')[0]+'-page-'+str(thispagenumber+1)+'.html'
                    else:
                        nexturl1=response.url.replace('.html','-page-1.html')#http://bbs.myhack58.com/read.php?tid-946246-fpage-3.html
                    print nexturl1
                    time.sleep(random.randint(2,5))
                    myhackdetailget(nexturl1)
                else:
                    return
            else:
                return




        sqlmyhackselect='SELECT href FROM JuneSpider.index_all_website WHERE (ownerwebsite="bbs.myhack58.com")'
        self.cursor.execute(sqlmyhackselect)
        self.connect.commit()
        urlsneedtovisit=self.cursor.fetchall()
        for i in urlsneedtovisit[:1]:
            myhackdetailget(i[0])


    def pediy_get_index(self):
        session1=requests.session()
        session1.headers=session1.headers
        # cookie1=cookielib.LWPCookieJar()

        def pediy(url1):
            print url1
            response=session1.request(method='GET',url=url1)
            datasoup=BeautifulSoup(response.text,'lxml')
            for ii in datasoup.select('#threadbits_forum_161 > tr'):
                try:
                    title= ii.select('td > div > a')[0].text
                    href= 'http://m.pediy.com/'+ii.select('td > div > a')[0].get('href')
                    publisherhref='http://m.pediy.com/'+ii.select('td.alt2 > div.smallfont > span')[0].get('onclick').split("'")[1]
                    publisher= ii.select('td.alt2 > div')[0].text.replace('\n','')
                    publishtime= ii.select('td.alt2 > font')[0].text

                    replayandview= ii.select('td.alt2')[2].get('title')
                    replayernum=replayandview.split(u'，',1)[0].replace(u'回复:','').strip()
                    viewernum=replayandview.split(u'，',1)[1].replace(u'查看次数:','').replace(',','').strip()

                    print replayernum
                    print viewernum
                    lastviewer=ii.select('td.alt2 > div > a')[0].text
                    lastviewerhref='http://m.pediy.com/'+ii.select('td.alt2 > div > a')[0].get('href')
                    lastviewtime= ii.select('td.alt2 > div.smallfont')[2].text.replace('\n','').lstrip().replace(',','')

                    sqlpediy='INSERT INTO JuneSpider.index_all_website (href,title,publishtime,lastviewtime,lastviewer,lastviewerhref,publisher,publisherhref,ownerwebsite) VALUE ("%s","%s","%s","%s","%s","%s","%s","%s","http://m.pediy.com")'%(
                        href,title,publishtime,lastviewtime,lastviewer,lastviewerhref,publisher,publisherhref
                    )
                    print sqlpediy
                    self.cursor.execute(sqlpediy)
                    self.connect.commit()


                except Exception as e:
                    print e

            nextpage=datasoup.select('#inlinemodform > table:nth-of-type(4) > tr > td:nth-of-type(2) > div > table > tr > td > a[rel=next]')##inlinemodform > table:nth-child(8) > tbody > tr > td:nth-child(2) > div > table > tbody > tr > td:nth-child(16) > a
            # for i in nextpage:
            #     print i
            #     print '\n'
            if nextpage:
                nexturl=nextpage[0].get('href')
                nexturl='http://m.pediy.com/'+nexturl
                pediy(nexturl)
                return


        pediyurllist=['http://m.pediy.com/forumdisplay.php?f=128',
                      'http://m.pediy.com/forumdisplay.php?f=161',
                      'http://m.pediy.com/forumdisplay.php?f=166',
                      'http://m.pediy.com/forumdisplay.php?f=4',
                      'http://m.pediy.com/forumdisplay.php?f=151',
                      'http://m.pediy.com/forumdisplay.php?f=162',
                      'http://m.pediy.com/forumdisplay.php?f=20',]


        for i in pediyurllist:
            pediy(i)

    def pediy_get_detail(self):
        def pediydetail(url2):
            session1=requests.session()
            session1.headers=self.headers
            response1=session1.request(method='GET',url=url2)
            datasoup=BeautifulSoup(response1.text,'lxml')
            for ii in datasoup.select('#posts > div > div'):
                try:
                    content= ii.select(' div > div > table  > tr > td > div > div > div')[0].text.replace('\t','').replace('\n','').replace('"','').replace("'",'')#content
                    floorAnddate= ii.select('#table1 > tr > td > div')[0].text.replace('\t','').lstrip('\n').rstrip('\n').split('\n')
                    floor=floorAnddate[0]
                    date=floorAnddate[2]
                    print floor
                    print date
                    publisher= ii.select('div > div > table > tr > td > div[id] > a')[0].text
                    publisherhref= 'http://m.pediy.com/'+ii.select(' div > div > table > tr > td > div[id] > a')[0].get('href')

                    sqlpediydetail='INSERT INTO JuneSpider.detail_post (floor,ownerhref,publisher,publisherhref,content,publishtime) VALUE ("%s","%s","%s","%s","%s","%s")'%(floor,url2,publisher,publisherhref,content,date)
                    self.cursor.execute(sqlpediydetail)
                    self.connect.commit()
                except Exception as e:
                    print e

            nextpage=datasoup.select('body > div[align=center] > div.page > div[align=left] > table > tr > td[align=right] > div.pagenav > table > tr > td.alt1 > a[rel=next]')
            if nextpage:
                nexturl='http://m.pediy.com/'+nextpage[0].get('href')
                time.sleep(0.5)
                pediydetail(nexturl)

        sqlpediygetindex='SELECT href FROM JuneSpider.index_all_website WHERE ownerwebsite = "http://m.pediy.com"'
        self.cursor.execute(sqlpediygetindex)
        self.connect.commit()

        urlindexlist=self.cursor.fetchall()
        for i in urlindexlist:
            pediydetail(i)










if __name__ == '__main__':
    thisclass=JuneSpider()
    thisclass.pediy_get_detail()