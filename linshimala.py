import urllib2
import cookielib
from bs4 import BeautifulSoup

headers1={
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}
cookie1=cookielib.LWPCookieJar()
cookiehandler=urllib2.HTTPCookieProcessor(cookie1)
request1=urllib2.Request(url='http://www.mala.cn/thread-14669372-3-1.html',headers=headers1)
openner=urllib2.build_opener(cookiehandler)
response=openner.open(request1)

responsedata=response.read()
datasoup=BeautifulSoup(responsedata,'lxml')
print datasoup
datasoup.select('#pid68493910 > tbody > tr:nth-of-type(1) > td.plc > div.pi > div > div.authi')