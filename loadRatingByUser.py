#encoding=utf8
from util import * 
import re,urllib,urllib2 
import MySQLdb
from bs4 import BeautifulSoup
import sys
import datetime
import time


def __unicode__(nonUniVal):
	if(nonUniVal == None) :
	   return u''
#dou=douban() 
#username='373382617@qq.com' 
#password='123654' 
#domain='http://www.douban.com/' 
#origURL='http://www.douban.com/login' 
#dou.setinfo(username,password,domain,origURL) 
#dou.signin() 
def crawlOneUser(userId, startFrom) :
	print userId, startFrom;
	reload(sys)
	sys.setdefaultencoding('utf-8')
	
	cj = cookielib.LWPCookieJar() 
	try: 
		cj.revert('douban.cookie') 
	except: 
		None 
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj)) 
	urllib2.install_opener(opener) 
	collectPage = urllib2.urlopen("http://movie.douban.com/people/" + userId + "/collect?start=" + str(startFrom) + "&sort=time&rating=all&filter=all&mode=list-view", timeout=20).read().encode('utf-8')
	soup = BeautifulSoup(collectPage, 'html.parser')
	
	#f1 = open(str(startFrom)+'.txt','w')
	#f1.write(collectPage)
	#print soup.title.name
	# u'title'
	
	#print soup.title.string
	# u'The Dormouse's story'
	
	#print len(dir_book) 
	#print soup.prettify()
	
	
	#initializing db connection
	conn = MySQLdb.connect(host='localhost',user='root',passwd='root',charset='utf8')
	conn.select_db('pydb')

	curs = conn.cursor()

	try :	
		sqlStr = 'update users set last_update_date = sysdate() where user_id = %s'
		#print sqlStr
		curs.execute(sqlStr, userId)
	except :
		print 'error updating ' + userId
		return

	for grid in soup.findAll("div", { "class" : "grid-view" }) :
		#print grid
		subSoup = BeautifulSoup(str(grid), 'html.parser')
		for item in subSoup.findAll("div", { "class" : "item" }) :
			itemSoup = BeautifulSoup(str(item), 'html.parser');
	
			#Fetch all rating related attributes
			subject = u''
			href = u''
			movie_id = u''
			try :
			    subject = itemSoup.em.get_text()
			    href = itemSoup.a['href']
			    movie_id = re.findall(r'\d+', href)[0]
			except :
			    continue
	
			imgSrc = u''
			try :
			    imgSrc = itemSoup.img['src']
			except :
			    u''
			
			intro = u''
			try :
			    intro = itemSoup.find('li', { 'class' : 'intro' }).get_text()
			except :
			    u''
			
			rating = u''
			try :
			    rating = itemSoup.find('span', { 'class' : re.compile('rating') })['class'][0]
			except :
			    u''
	
			date = u''
			try :
			    date = itemSoup.find('span', { 'class' : re.compile('date') }).get_text()
			except :
			    continue
	
			tags = u''
			try :
			    tags = itemSoup.find('span', { 'class' : re.compile('tags') }).get_text()
			except :
			    u''
	
			comment = u''
			try :
			    comment = itemSoup.find('span', { 'class' : re.compile('comment') }).get_text()
			except :
			    u''
			
			print movie_id;
			#movie_id = __unicode__(movie_id)
			#subject = __unicode__(subject)
			#href = __unicode__(href)
			#imgSrc = __unicode__(imgSrc)
			#intro = __unicode__(intro)
			#rating = __unicode__(rating)
			#date = __unicode__(date)
			#tags = __unicode__(tags)
			#comment = __unicode__(comment)
			try :
				#sqlStr = 'insert into db_movies(movie_id, subject, href, imgsrc, intro) values (\'' + movie_id.encode('utf-8') + '\', \''+ subject.encode('utf-8') + '\', \''+ href.encode('utf-8') + '\', \''+ imgSrc.encode('utf-8') + '\', \''+ intro.encode('utf-8') + '\')'
				#sqlStr = 'insert into db_movies(movie_id, subject, href, imgsrc, intro) values (\'' + movie_id.decode('utf-8') + '\', \''+ subject.decode('utf-8') + '\', \''+ href.decode('utf-8') + '\', \''+ imgSrc.decode('utf-8') + '\', \''+ intro.decode('utf-8') + '\')'
				sqlStr = 'insert into db_movies(movie_id, subject, href, imgsrc, intro) values (\'' + movie_id + '\', \''+ subject + '\', \''+ href + '\', \''+ imgSrc + '\', \''+ intro + '\')'
				#print sqlStr
				curs.execute(sqlStr)
			except :
				None

			date_time = datetime.datetime.strptime(date,'%Y-%m-%d')
			sqlStr = 'INSERT INTO `pydb`.`ratings`(`user_id`,`movie_id`,`rating`,`date`,`comment`)VALUES (%s, %s, %s, %s, %s)'
			ratingRec = [userId, movie_id, rating, date_time, comment]
			curs.execute(sqlStr, ratingRec)
			rating_id = curs.lastrowid
			#print rating_id
			if tags != u'' :
				curs.executemany('INSERT INTO `pydb`.`rating_tags`(`rating_id`,`tag`)VALUES(' + str(rating_id) + ', %s)', tags.split(' ', 1)[1].split(' '))
	
	try :		
		tagLiVal = []
		for tagLi in soup.findAll("li", { "class" : "clearfix" }) :
			tagLiSoup = BeautifulSoup(str(tagLi), 'html.parser')
			tagLiVal.append([userId, tagLiSoup.a['title'], tagLiSoup.span.get_text()])
		print tagLiVal
		curs.executemany("insert into user_movie_tags (`user_id`,`tag`,`time`) values (%s, %s, %s)", tagLiVal)
	except :
		None
	#curs.execute('select * from db_movies')
	#result = curs.fetchone()
	#print result
	conn.commit()
	curs.close()
	conn.close()	

	userMovieNum = int(re.findall(r'\d+', re.findall(r'看过的电影\(\d+\)', collectPage)[0])[0])
	if startFrom + 30 < userMovieNum :
		time.sleep( 2 )
		crawlOneUser(userId, startFrom + 30)


crawlOneUser('2925766', 150)