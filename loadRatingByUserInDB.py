#encoding=utf8
from util import * 
import re,urllib,urllib2 
import MySQLdb
from bs4 import BeautifulSoup
from loadRatingByUser import *
import sys
import datetime
import time


def loadLimitUsers(limitNumber) :	
	conn = MySQLdb.connect(host='localhost',user='root',passwd='root')
	curs = conn.cursor()
	conn.select_db('pydb')
	curs.execute('select user_id from users where last_update_date is null limit %s', limitNumber)
	results = curs.fetchall()
	i = 1;
	for user in results :
		print str(i) + "----------------------------------------------------------------------------"
		i += 1
		print user[0]
		crawlOneUser(user[0], 0)
		time.sleep( 2 )
	curs.close()
	conn.close()

loadLimitUsers(200)