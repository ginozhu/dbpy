# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import re

source = ''
source += '        <div class="item" >'
source += '            <div class="pic">'
source += '                <a title="无心法师" href="http://movie.douban.com/subject/26298756/" class="nbg">'
source += '                    <img alt="无心法师" src="http://img3.douban.com/view/movie_poster_cover/ipst/public/p2248745554.jpg" class="">'
source += '                </a>'
source += '            </div>'
source += '            <div class="info">'
source += '                <ul>'
source += '                    <li class="title">'
source += '                        <a href="http://movie.douban.com/subject/26298756/" class="">'
source += '                            <em>无心法师</em>'
source += '                            '
source += '                        </a>'
source += '                    </li>'
source += '                        <li class="intro">2015-07-06(中国大陆) / 韩东君 / 金晨 / 陈瑶 / 张若昀 / 孔连顺 / 隋咏良 / 王彦霖 / 麦克 / 中国大陆 / 李国立 / 剧情 / 悬疑 / 徐子沅 / 方羌羌 / 肖志瑶 / 李楠 / 汉语普通话</li>'
source += '                    <li>'
source += '                         <span class="rating4-t"></span>'
source += '                        <span class="date">2015-07-08</span>'
source += '                        '
source += '                            <span class="tags">标签: 无心法师 网剧</span>'
source += '                    </li>'
source += '                    <li>'
source += '                        <span class="comment">不想追了。1.预见到女二会引发腥风血雨；2.男主第二集就因为想多赚点钱害死人了，我精神洁癖，受不了这种男主。拜拜。</span>'
source += '                        '
source += '                    </li>'
source += '                </ul>'
source += '            </div>'
source += '        </div>'


soup = BeautifulSoup(source, "html.parser")

subject = None
href = None
try :
    subject = soup.a['title']
    href = soup.a['href']
except :
    None


imgSrc = None
try :
    imgSrc = soup.img['src']
except :
    None

intro = None
try :
    intro = soup.find('li', { 'class' : 'intro' }).get_text()
except :
    None


rating = None
try :
    rating = soup.find('span', { 'class' : re.compile('rating') })['class'][0]
except :
    None
date = None
try :
    date = soup.find('span', { 'class' : re.compile('date') }).get_text()
except :
    None
tags = None
try :
    tags = soup.find('span', { 'class' : re.compile('tags') }).get_text()
except :
    None
comment = None
try :
    comment = soup.find('span', { 'class' : re.compile('comment') }).get_text()
except :
    None

print subject
print href
print imgSrc
print intro
print rating
print date
print tags
print comment