#coding:utf-8
import  sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests
from lxml.etree import tostring
from lxml import  html
from userAgents import pcAgents
import random
import hashlib
import MySQLdb
import time
from proxies import hkProxy

class getIntelligence(object):
	def __init__(self):
		self.con = MySQLdb.Connect(host='127.0.0.1', user='root', passwd='silence123456', db='intelligence', charset='utf8')
		self.curson = self.con.cursor()

	def check(self,articleID):
		sql = "select * from informations where article_id='%s'" %(articleID)
		self.curson.execute(sql)
		num = len(self.curson.fetchall())
		if num==0:
			return True
		else:
			return False

	def certGetArticles(self):
		header = {
			'User-Agent':random.choice(pcAgents)
		}
		startUrl = "https://ics-cert.us-cert.gov/announcements"
		try:
			request = requests.get(url=startUrl, headers=header,proxies=hkProxy,timeout=20)
			formatHtml = html.fromstring(request.text)
			articles = formatHtml.xpath("//li[contains(@class,'views-row')]")
			if len(articles)!=0:
				for article in articles:
					title = article.xpath("div/strong/a/text()")[0].strip()
					url = "https://ics-cert.us-cert.gov" + article.xpath("div/strong/a/@href")[0]
					title = '<a href="%s">%s</a>' % (url, title)
					publish_time = article.xpath("div/em[@class='field-content']/text()")[0]
					author = ""
					abstract = article.xpath("div/div[@class='field-content']")[0]
					abstract = tostring(abstract).strip()
					md5encode = hashlib.md5(url)
					articleid = str(md5encode.hexdigest())
					collection_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
					flag = self.check(articleid)
					if flag:
						sql = "INSERT INTO informations(`author`,`article_id`,`website`,`title`,`abstract`,`publish_time`,`collection_time`,`category`) VALUES ('%s','%s','ics-cert.us-cert.gov','%s','%s','%s','%s','Threat Research')" %(author,articleid,MySQLdb.escape_string(title),MySQLdb.escape_string(abstract),publish_time,collection_time)
						self.curson.execute(sql)
						sql ="INSERT INTO informations_id(`article_id`) VALUES ('%s')" %(articleid)
						self.curson.execute(sql)
						self.con.commit()
		except:
			pass

	def insightsGetAiticles(self):
		urls = {
			'DevOps':'https://insights.sei.cmu.edu/cgi-bin/mt/mt-search.cgi?IncludeBlogs=18&template_id=1344&limit=8&archive_type=Index&page=',
			'CERT/CC':'https://insights.sei.cmu.edu/cgi-bin/mt/mt-search.cgi?IncludeBlogs=14&template_id=839&limit=8&archive_type=Index&page=',
			'Insider Threat':'https://insights.sei.cmu.edu/cgi-bin/mt/mt-search.cgi?IncludeBlogs=17&template_id=1308&limit=8&archive_type=Index&page=',
			'SATURN':'https://insights.sei.cmu.edu/cgi-bin/mt/mt-search.cgi?IncludeBlogs=15&template_id=1165&limit=8&archive_type=Index&page=',
			'SEI':'https://insights.sei.cmu.edu/cgi-bin/mt/mt-search.cgi?IncludeBlogs=9&template_id=1234&limit=8&archive_type=Index&page='
		}
		for key,value in urls.items():
			header = {
				'User-Agent': random.choice(pcAgents)
			}
			page = 1
			while True:
				isHas = False
				startUrl = value+str(page)
				try:
					request = requests.get(url=startUrl, headers=header,proxies=hkProxy,timeout=20)
					formatHtml = html.fromstring(request.text)
					articles = formatHtml.xpath("//article")
					if len(articles) != 0:
						for article in articles:
							title = article.xpath("div/h2/a")[0]
							title = tostring(title)
							url = article.xpath("div/h2/a/@href")[0]
							publish_time = article.xpath("div/p[@id='alert']/time/@datetime")[0]
							author = article.xpath("div/p[@id='alert']/span/a")[0]
							author = tostring(author).replace('href="', 'href="https://insights.sei.cmu.edu')
							abstract = article.xpath("div[@itemprop='articleBody']")[0]
							abstract = tostring(abstract).replace('src="', 'href="https://insights.sei.cmu.edu')
							md5encode = hashlib.md5(url)
							articleid = str(md5encode.hexdigest())
							flag = self.check(articleid)
							collection_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
							if flag:
								sql = "INSERT INTO informations(`author`,`article_id`,`website`,`title`,`abstract`,`publish_time`,`collection_time`,`category`) VALUES ('%s','%s','https://insights.sei.cmu.edu/','%s','%s','%s','%s','%s')" % (author,articleid, MySQLdb.escape_string(title), MySQLdb.escape_string(abstract), publish_time,collection_time,key)
								self.curson.execute(sql)
								sql = "INSERT INTO informations_id(`article_id`) VALUES ('%s')" % (articleid)
								self.curson.execute(sql)
								self.con.commit()
							else:
								isHas = True
								pass
					else:
						break
				except:
					break
				if isHas:
					break
				else:
					page += 1

	def krebsonsecurityGetArticles(self):
		page = 1
		header = {
			'User-Agent':random.choice(pcAgents)
		}
		while True:
			startUrl = "https://krebsonsecurity.com/page/" + str(page)
			isHas = False
			try:
				request = requests.get(url=startUrl, headers=header,proxies=hkProxy,timeout=20)
				formatHtml = html.fromstring(request.text)
				articles = formatHtml.xpath("//div[@class='post-smallerfont']")
				if len(articles)!=0:
					for article in articles:
						title = article.xpath("h2[@class='post-title']/a")[0]
						title = tostring(title)
						url = article.xpath("h2[@class='post-title']/a/@href")[0]
						publish_time = url.split("/")[3]+"-"+url.split("/")[4]+"-"+article.xpath("//small/span[@class='date']/text()")[0]
						author = ""
						abstract = article.xpath("div[@class='entry']")[0]
						abstract = tostring(abstract)
						md5encode = hashlib.md5(url)
						articleid = str(md5encode.hexdigest())
						flag = self.check(articleid)
						collection_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
						if flag:
							sql = "INSERT INTO informations(`author`,`article_id`,`website`,`title`,`abstract`,`publish_time`,`collection_time`) VALUES ('%s','%s','https://krebsonsecurity.com/','%s','%s','%s','%s')" %(author,articleid,MySQLdb.escape_string(title),MySQLdb.escape_string(abstract),publish_time,collection_time)
							self.curson.execute(sql)
							sql ="INSERT INTO informations_id(`article_id`) VALUES ('%s')" %(articleid)
							self.curson.execute(sql)
							self.con.commit()
						else:
							isHas = True
							pass
				else:
					break
			except:
				break
			if isHas:
				break
			else:
				page+=1

	def nakedsecurityGetArticles(self):
		page = 1
		header = {
			'User-Agent':random.choice(pcAgents)
		}
		while True:
			startUrl = "https://nakedsecurity.sophos.com/page/" + str(page)
			isHas = False
			try:
				request = requests.get(url=startUrl, headers=header,proxies=hkProxy,timeout=20)
				formatHtml = html.fromstring(request.text)
				articles = formatHtml.xpath("//article[@class='card-article']")
				if len(articles)!=0:
					for article in articles:
						title = article.xpath("div/h3[@class='card-title']/a")[0]
						title = tostring(title)
						url = article.xpath("div/h3[@class='card-title']/a/@href")[0]
						publish_time = url.split("/")[3]+"-"+url.split("/")[4]+"-"+url.split("/")[5]
						author = article.xpath("div/div/div[@class='author-box']/text()")[0].strip()
						abstract = ""
						md5encode = hashlib.md5(url)
						articleid = str(md5encode.hexdigest())
						flag = self.check(articleid)
						collection_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
						if flag:
							sql = "INSERT INTO informations(`author`,`article_id`,`website`,`title`,`abstract`,`publish_time`,`collection_time`) VALUES ('%s','%s','https://nakedsecurity.sophos.com','%s','%s','%s','%s')" %(author,articleid,MySQLdb.escape_string(title),MySQLdb.escape_string(abstract),publish_time,collection_time)
							self.curson.execute(sql)
							sql ="INSERT INTO informations_id(`article_id`) VALUES ('%s')" %(articleid)
							self.curson.execute(sql)
							self.con.commit()
						else:
							isHas = True
							pass
				else:
					break
			except:
				break
			if isHas:
				break
			else:
				page+=1

	def softpediaGetArticles(self):
		page = 1
		header = {
			'User-Agent':random.choice(pcAgents)
		}
		while True:
			startUrl = "http://news.softpedia.com/cat/Security/index-" + str(page)+".shtml"
			isHas = False
			try:
				request = requests.get(url=startUrl, headers=header,proxies=hkProxy,timeout=20)
				formatHtml = html.fromstring(request.text)
				articles = formatHtml.xpath("//div[contains(@class,'dlclassic')]")
				if len(articles)!=0:
					for article in articles:
						title = article.xpath("h3/a")[0]
						title = tostring(title)
						url = article.xpath("h3/a/@href")[0]
						publish_time = article.xpath("div[contains(@class,'info')]/ul/li[last()]/text()")[0]
						author = article.xpath("div[contains(@class,'info')]/ul/li/b/text()")[0]
						try:
							abstract = article.xpath("div/p[@class='ellip']")[0]
							abstract = tostring(abstract)
						except:
							abstract =""
						md5encode = hashlib.md5(url)
						articleid = str(md5encode.hexdigest())
						flag = self.check(articleid)
						collection_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
						if flag:
							sql = "INSERT INTO informations(`author`,`article_id`,`website`,`title`,`abstract`,`publish_time`,`collection_time`) VALUES ('%s','%s','http://news.softpedia.com','%s','%s','%s','%s')" %(author,articleid,MySQLdb.escape_string(title),MySQLdb.escape_string(abstract),publish_time,collection_time)
							self.curson.execute(sql)
							sql ="INSERT INTO informations_id(`article_id`) VALUES ('%s')" %(articleid)
							self.curson.execute(sql)
							self.con.commit()
						else:
							isHas = True
							pass
				else:
					break
			except:
				break
			if isHas:
				break
			else:
				page+=1

	def securityaffairsGetArticles(self):
		page = 1
		header = {
			'User-Agent':random.choice(pcAgents)
		}
		while True:
			startUrl = "http://securityaffairs.co/wordpress/page/" + str(page)
			isHas = False
			try:
				request = requests.get(url=startUrl, headers=header,proxies=hkProxy,timeout=20)
				formatHtml = html.fromstring(request.text)
				articles = formatHtml.xpath("//div[@class='post_inner_wrapper']")
				if len(articles)!=0:
					for article in articles:
						title = article.xpath("div[@class='post_header_wrapper']/div/h3/a")[0]
						title = tostring(title)
						url = article.xpath("div[@class='post_header_wrapper']/div/h3/a/@href")[0]
						publish_time = article.xpath("div[contains(@class,'post_detail')]/a/text()")[0]
						author = article.xpath("div[contains(@class,'post_detail')]/a/text()")[1]
						try:
							abstract = article.xpath("div[@class='post_wrapper_inner']/p")[0]
							abstract = tostring(abstract)
						except:
							abstract =""
						md5encode = hashlib.md5(url)
						articleid = str(md5encode.hexdigest())
						flag = self.check(articleid)
						collection_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
						if flag:
							sql = "INSERT INTO informations(`author`,`article_id`,`website`,`title`,`abstract`,`publish_time`,`collection_time`) VALUES ('%s','%s','http://securityaffairs.co','%s','%s','%s','%s')" %(author,articleid,MySQLdb.escape_string(title),MySQLdb.escape_string(abstract),publish_time,collection_time)
							self.curson.execute(sql)
							sql ="INSERT INTO informations_id(`article_id`) VALUES ('%s')" %(articleid)
							self.curson.execute(sql)
							self.con.commit()
						else:
							isHas = True
							pass
				else:
					break
			except:
				break
			if isHas:
				break
			else:
				page+=1

	def seraGetArticles(self):
		page = 1
		header = {
			'User-Agent':random.choice(pcAgents)
		}
		while True:
			startUrl = "https://sera-brynn.com/sera-brynn-news/page/" + str(page)
			isHas = False
			try:
				request = requests.get(url=startUrl, headers=header,proxies=hkProxy,timeout=20)
				formatHtml = html.fromstring(request.text)
				articles = formatHtml.xpath("//div[contains(@class,'post-item')]")
				if len(articles)!=0:
					for article in articles:
						title = article.xpath("div/div/div[@class='post-title']/h2/a")[0]
						title = tostring(title)
						url = article.xpath("div/div/div[@class='post-title']/h2/a/@href")[0]
						publish_time = article.xpath("div/div/div/div/span[@class='date']/text()")[-1]
						author = article.xpath("div/div/div/div/span[@class='author']/a/text()")[0]
						abstract = article.xpath("div/div/div[@class='post-excerpt']")[0]
						abstract = tostring(abstract)
						md5encode = hashlib.md5(url)
						articleid = str(md5encode.hexdigest())
						flag = self.check(articleid)
						collection_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
						if flag:
							sql = "INSERT INTO informations(`author`,`article_id`,`website`,`title`,`abstract`,`publish_time`,`collection_time`) VALUES ('%s','%s','https://sera-brynn.com','%s','%s','%s','%s')" %(MySQLdb.escape_string(author),articleid,MySQLdb.escape_string(title),MySQLdb.escape_string(abstract),publish_time,collection_time)
							self.curson.execute(sql)
							sql ="INSERT INTO informations_id(`article_id`) VALUES ('%s')" %(articleid)
							self.curson.execute(sql)
							self.con.commit()
						else:
							isHas = True
							pass
				else:
					break
			except:
				break
			if isHas:
				break
			else:
				page+=1

	def hacknewsGetArticles(self):
		header = {
			'User-Agent':random.choice(pcAgents)
		}
		startUrl = "http://thehackernews.com/"
		while True:
			isHas = False
			try:
				request = requests.get(url=startUrl, headers=header,proxies=hkProxy,timeout=20)
				formatHtml = html.fromstring(request.text)
				articles = formatHtml.xpath("//span[@class='main-article-info']")
				if len(articles)!=0:
					for article in articles:
						title = article.xpath("h2/a")[0]
						title = tostring(title)
						url = article.xpath("h2/a/@href")[0]
						publish_time = article.xpath("div/span/span[@class='updated']/text()")[0]
						try:
							author = article.xpath("div/span/span/a[@href='#author-info']/span/text()")[0]
						except:
							author = article.xpath("div/span/a[@href='#author-info']/span/text()")[0]
						abstract = article.xpath("div[contains(@class,'entry-content')]/div/div")[0]
						abstract = tostring(abstract)
						md5encode = hashlib.md5(url)
						articleid = str(md5encode.hexdigest())
						flag = self.check(articleid)
						collection_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
						if flag:
							sql = "INSERT INTO informations(`author`,`article_id`,`website`,`title`,`abstract`,`publish_time`,`collection_time`) VALUES ('%s','%s','http://thehackernews.com/','%s','%s','%s','%s')" %(MySQLdb.escape_string(author),articleid,MySQLdb.escape_string(title),MySQLdb.escape_string(abstract),publish_time,collection_time)
							self.curson.execute(sql)
							sql ="INSERT INTO informations_id(`article_id`) VALUES ('%s')" %(articleid)
							self.curson.execute(sql)
							self.con.commit()
						else:
							isHas = True
							pass
				else:
					break
			except:
				break
			if isHas:
				break
			else:
				nextPage = formatHtml.xpath("//a[@class='blog-pager-older-link-mobile']")
				if len(nextPage)>0:
					startUrl = nextPage[0].xpath('@href')[0]
				else:
					break
	def darkreadingGetArticles(self):
		page = 1
		header = {
			'User-Agent':random.choice(pcAgents)
		}
		while True:
			startUrl = "http://www.darkreading.com/archives.asp?newsandcommentary=yes&piddl_archivepage=" + str(page)
			isHas = False
			try:
				request = requests.get(url=startUrl, headers=header,proxies=hkProxy,timeout=20)
				formatHtml = html.fromstring(request.text)
				articles = formatHtml.xpath("//div[@class='listdocitem']")
				if len(articles)!=0:
					for article in articles:
						title = article.xpath("span[contains(@class,'blue')]/a")[0]
						title = tostring(title)
						url = article.xpath("span[contains(@class,'blue')]/a/@href")[0]
						publish_time = article.xpath("div/div/span[@class='gray smallest']/text()")[0].split('|')[0].strip()
						author = ""
						abstract = article.xpath("span[@class='black smaller']")[0]
						abstract = tostring(abstract)
						md5encode = hashlib.md5(url)
						articleid = str(md5encode.hexdigest())
						flag = self.check(articleid)
						collection_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
						if flag:
							sql = "INSERT INTO informations(`author`,`article_id`,`website`,`title`,`abstract`,`publish_time`,`collection_time`) VALUES ('%s','%s','http://www.darkreading.com','%s','%s','%s','%s')" %(author,articleid,MySQLdb.escape_string(title),MySQLdb.escape_string(abstract),publish_time,collection_time)
							self.curson.execute(sql)
							sql ="INSERT INTO informations_id(`article_id`) VALUES ('%s')" %(articleid)
							self.curson.execute(sql)
							self.con.commit()
						else:
							isHas = True
							pass
				else:
					break
			except:
				break
			if isHas:
				break
			else:
				page+=1

	def flashpointGetArticles(self):
		page = 1
		header = {
			'User-Agent':random.choice(pcAgents)
		}
		while True:
			if page==10:
				break
			startUrl = "https://www.flashpoint-intel.com/blog/page/" + str(page)
			isHas = False
			try:
				request = requests.get(url=startUrl, headers=header,proxies=hkProxy,timeout=20)
				formatHtml = html.fromstring(request.text)
				articles = formatHtml.xpath("//article")
				if len(articles)!=0:
					for article in articles:
						title = article.xpath("header/h1[@class='entry-title']/a")[0]
						title = tostring(title)
						url = article.xpath("header/h1[@class='entry-title']/a/@href")[0]
						publish_time = article.xpath("div[@class='meta']/div[@class='date']/text()")[0].strip()
						author = article.xpath("div[@class='meta']/div[@class='author']")[0]
						author = tostring(author)
						abstract = article.xpath("div[@class='entry-summary']")[0]
						abstract = tostring(abstract)
						md5encode = hashlib.md5(url)
						articleid = str(md5encode.hexdigest())
						flag = self.check(articleid)
						collection_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
						if flag:
							sql = "INSERT INTO informations(`author`,`article_id`,`website`,`title`,`abstract`,`publish_time`,`collection_time`) VALUES ('%s','%s','https://www.flashpoint-intel.com','%s','%s','%s','%s')" %(author,articleid,MySQLdb.escape_string(title),MySQLdb.escape_string(abstract),publish_time,collection_time)
							self.curson.execute(sql)
							sql ="INSERT INTO informations_id(`article_id`) VALUES ('%s')" %(articleid)
							self.curson.execute(sql)
							self.con.commit()
						else:
							isHas = True
							pass
				else:
					break
			except:
				break
			if isHas:
				break
			else:
				page+=1


	def run(self):
		self.certGetArticles()
		self.insightsGetAiticles()
		self.krebsonsecurityGetArticles()
		self.nakedsecurityGetArticles()
		self.softpediaGetArticles()
		self.securityaffairsGetArticles()
		self.seraGetArticles()
		self.hacknewsGetArticles()
		self.darkreadingGetArticles()
		self.flashpointGetArticles()
	def close(self):
		self.con.commit()
		self.curson.close()
		self.con.close()
if __name__=='__main__':
	work = getIntelligence()
	work.run()
	work.close()