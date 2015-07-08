from util import * 
import re,urllib,urllib2 
import MySQLdb
from bs4 import BeautifulSoup

#dou=douban() 
#username='373382617@qq.com' 
#password='123654' 
#domain='http://www.douban.com/' 
#origURL='http://www.douban.com/login' 
#dou.setinfo(username,password,domain,origURL) 
#dou.signin() 


#cj = cookielib.LWPCookieJar() 
#try: 
#	cj.revert('douban.cookie') 
#except: 
#	None 
#opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj)) 
#urllib2.install_opener(opener) 
#collectPage = urllib2.urlopen("http://movie.douban.com/people/crankysophia/collect?start=0&sort=time&rating=all&filter=all&mode=list-view").read().decode("utf-8")
#soup = BeautifulSoup(collectPage, 'html.parser')
#
#print soup.title.name
## u'title'
#
#print soup.title.string
## u'The Dormouse's story'
#
##print len(dir_book) 
##print soup.prettify()
#
#for grid in soup.findAll("div", { "class" : "grid-view" }) :
#	#print grid
#	subSoup = BeautifulSoup(str(grid), 'html.parser')
#	for item in subSoup.findAll("div", { "class" : "item" }) :
#		print BeautifulSoup(str(item)).prettify().encode('utf-8')
#		#print BeautifulSoup(str(item)).find("li", { "class" : "title" }).encode('gbk')


conn = MySQLdb.connect(host='localhost',user='root',passwd='root')
curs = conn.cursor()
conn.select_db('mysql')
curs.execute('select sysdate() from dual')
result = curs.fetchone()
print result;