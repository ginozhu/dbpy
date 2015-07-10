#encoding=utf-8
from util import * 
import re,urllib,urllib2 
import MySQLdb
from bs4 import BeautifulSoup
import re

conn = MySQLdb.connect(host='localhost',user='root',passwd='root')
curs = conn.cursor()
conn.select_db('pydb')
curs.execute('INSERT INTO ratings (user_id) VALUES (1)')
curs.execute('delete from ratings')
print curs.lastrowid
print conn.insert_id()
curs.execute('select * from db_movies where movie_id = 1422063')
result = curs.fetchone()
print result

a = u'你好'
print a.encode('utf-8').decode('utf-8')
print a.encode('utf-8')
print a

print re.findall(r'\d+', re.findall(r'看过的电影\(\d+\)', '    TheForce看过的电影(1089)')[0])








cj = cookielib.LWPCookieJar() 
try: 
	cj.revert('douban.cookie') 
except: 
	None 
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj)) 
urllib2.install_opener(opener) 
collectPage = urllib2.urlopen("http://movie.douban.com/people/crankysophia/collect?start=120&sort=time&rating=all&filter=all&mode=list-view").read()
soup = BeautifulSoup(collectPage, 'html.parser')
print soup