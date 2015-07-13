# encoding=utf8
from util import *
import re, urllib, urllib2
import MySQLdb
from bs4 import BeautifulSoup
import sys
import datetime
import time


def __unicode__(non_uni_val):
    if non_uni_val is None:
        return u''


# dou=douban()
# username='373382617@qq.com'
# password='123654'
# domain='http://www.douban.com/'
# origURL='http://www.douban.com/login'
# dou.setinfo(username,password,domain,origURL)
# dou.signin()
def crawl_one_user(user_id, start_from):
    print user_id, start_from;
    reload(sys)
    sys.setdefaultencoding('utf-8')

    cj = cookielib.LWPCookieJar()
    try:
        cj.revert('douban.cookie')
    except:
        None
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    collectPage = urllib2.urlopen("http://movie.douban.com/people/" + user_id + "/collect?start=" + str(
        start_from) + "&sort=time&rating=all&filter=all&mode=list-view", timeout=20).read().encode('utf-8')
    soup = BeautifulSoup(collectPage, 'html.parser')

    # f1 = open(str(startFrom)+'.txt','w')
    # f1.write(collectPage)
    # print soup.title.name
    # u'title'

    # print soup.title.string
    # u'The Dormouse's story'

    # print len(dir_book)
    # print soup.prettify()

    # initializing db connection
    conn = MySQLdb.connect(host='localhost', user='root', passwd='root', charset='utf8')
    conn.select_db('pydb')

    curs = conn.cursor()

    try:
        sql_str = 'insert into users(user_id) values (\'' + user_id + '\')'
        # print sqlStr
        curs.execute(sql_str)
    except:
        None

    for grid in soup.findAll("div", {"class": "grid-view"}):
        # print grid
        sub_soup = BeautifulSoup(str(grid), 'html.parser')
        for item in sub_soup.findAll("div", {"class": "item"}):
            item_soup = BeautifulSoup(str(item), 'html.parser');

            # Fetch all rating related attributes
            subject = u''
            href = u''
            movie_id = u''
            try:
                subject = item_soup.em.get_text()
                href = item_soup.a['href']
                movie_id = re.findall(r'\d+', href)[0]
            except:
                continue

            imgSrc = u''
            try:
                imgSrc = item_soup.img['src']
            except:
                u''

            intro = u''
            try:
                intro = item_soup.find('li', {'class': 'intro'}).get_text()
            except:
                u''

            rating = u''
            try:
                rating = item_soup.find('span', {'class': re.compile('rating')})['class'][0]
            except:
                u''

            date = u''
            try:
                date = item_soup.find('span', {'class': re.compile('date')}).get_text()
            except:
                continue

            tags = u''
            try:
                tags = item_soup.find('span', {'class': re.compile('tags')}).get_text()
            except:
                u''

            comment = u''
            try:
                comment = item_soup.find('span', {'class': re.compile('comment')}).get_text()
            except:
                u''

            print movie_id;
            # movie_id = __unicode__(movie_id)
            # subject = __unicode__(subject)
            # href = __unicode__(href)
            # imgSrc = __unicode__(imgSrc)
            # intro = __unicode__(intro)
            # rating = __unicode__(rating)
            # date = __unicode__(date)
            # tags = __unicode__(tags)
            # comment = __unicode__(comment)
            try:
                # sqlStr = 'insert into db_movies(movie_id, subject, href, imgsrc, intro)
                # values (\'' + movie_id.encode('utf-8') + '\', \''+ subject.encode('utf-8')
                # + '\', \''+ href.encode('utf-8') + '\', \''+ imgSrc.encode('utf-8') + '\', \''
                # + intro.encode('utf-8') + '\')'
                # sqlStr = 'insert into db_movies(movie_id, subject, href, imgsrc, intro)
                # values (\'' + movie_id.decode('utf-8') + '\', \''+ subject.decode('utf-8')
                # + '\', \''+ href.decode('utf-8') + '\', \''+ imgSrc.decode('utf-8') + '\', \''
                # + intro.decode('utf-8') + '\')'
                sql_str = 'insert into db_movies(movie_id, subject, href, imgsrc, intro) values (\'' + movie_id + \
                          '\', \'' + subject + '\', \'' + href + '\', \'' + imgSrc + '\', \'' + intro + '\')'
                # print sqlStr
                curs.execute(sql_str)
            except:
                None

            date_time = datetime.datetime.strptime(date, '%Y-%m-%d')
            sql_str = ('INSERT INTO `pydb`.`ratings`(`user_id`,`movie_id`,`rating`,`date`,`comment`)'
                       'VALUES (%s, %s, %s, %s, %s)')
            rating_rec = [user_id, movie_id, rating, date_time, comment]
            curs.execute(sql_str, rating_rec)
            rating_id = curs.lastrowid
            # print rating_id
            if tags != u'':
                curs.executemany(
                    'INSERT INTO `pydb`.`rating_tags`(`rating_id`,`tag`)VALUES(' + str(rating_id) + ', %s)',
                    tags.split(' ', 1)[1].split(' '))

    try:
        tag_li_val = []
        for tagLi in soup.findAll("li", {"class": "clearfix"}):
            tag_li_soup = BeautifulSoup(str(tagLi), 'html.parser')
            tag_li_val.append([user_id, tag_li_soup.a['title'], tag_li_soup.span.get_text()])
        print tag_li_val
        curs.executemany("insert into user_movie_tags (`user_id`,`tag`,`time`) values (%s, %s, %s)", tag_li_val)
    except:
        None
    # curs.execute('select * from db_movies')
    # result = curs.fetchone()
    # print result
    conn.commit()
    curs.close()
    conn.close()

    user_movie_num = int(re.findall(r'\d+', re.findall(r'看过的电影\(\d+\)', collectPage)[0])[0])
    if start_from + 30 < user_movie_num:
        time.sleep(2)
        crawl_one_user(user_id, start_from + 30)


crawl_one_user('mizeer', 0)
