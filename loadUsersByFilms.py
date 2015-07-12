#encoding=utf8
from util import * 
import re,urllib,urllib2 
import MySQLdb
from bs4 import BeautifulSoup
import sys
import datetime
import time









def findMovieReviewers(movie_id, subUrl) :	
	print movie_id
	print subUrl
	reload(sys)
	sys.setdefaultencoding('utf-8')
	
	cj = cookielib.LWPCookieJar() 
	try: 
		cj.revert('douban.cookie') 
	except: 
		try :
			dou=douban() 
			username='373382617@qq.com' 
			password='123654' 
			domain='http://www.douban.com/' 
			origURL='http://www.douban.com/login' 
			dou.setinfo(username,password,domain,origURL) 
			dou.signin()  
		except : 
			return
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj)) 
	urllib2.install_opener(opener) 
	collectPage = urllib2.urlopen("http://movie.douban.com/subject/" + movie_id + "/reviews" + subUrl, timeout=20).read().encode('utf-8')
	soup = BeautifulSoup(collectPage, 'html.parser')

	#init db connection
	conn = MySQLdb.connect(host='localhost',user='root',passwd='root')
	curs = conn.cursor()
	conn.select_db('pydb')

	reviewsOfThisPage = soup.findAll("a", { "class" : "review-hd-avatar" })

	countReviews = len(reviewsOfThisPage)
	print countReviews

	for review in reviewsOfThisPage :
		reviewSoup = BeautifulSoup(str(review), 'html.parser')
		userId = reviewSoup.a["href"].split("/")[4]
		try :
			#insert data into db rowbyrow
			curs.execute('INSERT INTO users (user_id) VALUES (%s)', userId)
			print "rows affected " + str(curs.rowcount)
		except :
			print "error inserting, probably duplicate for userid : " + userId
			None

	try :
		foundSubUrl = soup.find("a", { "class" : "next" })['href']
	except :
		foundSubUrl = ""

	print foundSubUrl

	conn.commit()
	curs.close()
	conn.close()	

	if "" != foundSubUrl  and countReviews > 0 :
		time.sleep( 2 )
		findMovieReviewers(movie_id, foundSubUrl)

findMovieReviewers("26277313", "")