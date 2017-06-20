import requests
import cookielib

headers={
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

session1=requests.session()
cookie1=cookielib.LWPCookieJar()
session1.cookies=cookie1
data=session1.request(method='get',url='http://bbs.hackbase.com/forum-1-1.html',headers=headers)
# print data.content

for i in session1.cookies:
    print i.name,'--------',i.value