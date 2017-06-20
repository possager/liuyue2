#_*_coding:utf-8_*_
import urllib2
import cookielib
import requests
from bs4 import BeautifulSoup
import MySQLdb
import time
import random
import re
import requests

class JuneSpider:
    def __init__(self):
        # self.connect=MySQLdb.connect(host='127.0.0.1',user='root',passwd='asd123456',db='hackav',charset='utf8')
        # self.cursor=self.connect.cursor()
        self.headers={
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

    def hackbase_index_get(self):
        cookie1 = cookielib.LWPCookieJar()
        # handlers = urllib2.HTTPCookieProcessor(cookie1)
        # openner = urllib2.build_opener(handlers)
        # request1 = urllib2.Request(url='http://bbs.hackav.com/thread-10306-1-45.html', headers=self.headers)
        # response=openner.open(request1)
        # data=response.read()
        # print data
        # response=urllib2.urlopen('http://bbs.hackav.com/thread-10305-1-45.html')
        # print response.read()
        response=requests.get('http://bbs.hackav.com/thread-10305-1-45.html')
        print response.text

if __name__ == '__main__':
    thisclass=JuneSpider()
    thisclass.hackbase_index_get()