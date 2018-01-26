# coding=utf-8
# @Time : 2018/1/23 10:24
# @Author : 李飞
import re, requests
from bs4 import BeautifulSoup
import MySQLdb
import random


def insert(tittle, content):
    conn = MySQLdb.connect(host="116.196.96.140", user="root", passwd="901211feifei", db="restblog", charset="utf8")
    sql = 'insert into blog_blog (tittle,content,author_id,click_num,fav_num,add_time,isintroduce) VALUES (%s,%s,%s,%s,%s,%s,%s)'
    cursor = conn.cursor()
    import datetime
    params = (tittle, content, random.randint(1, 6), 0, 0, datetime.datetime.now(),False)
    n = cursor.execute(sql, params, )
    conn.commit()
    conn.close()
    print(n)


def getdata():
    for i in range(10):
        url = 'http://python.jobbole.com/all-posts/page/{}/'.format(i)
        result = requests.get(url=url, )
        result = BeautifulSoup(result.content, 'lxml')
        hrefs = result.select('div.post-meta p a.archive-title')
        for i in hrefs:
            detail_url = i.attrs['href']
            result = requests.get(url=detail_url, )
            result = BeautifulSoup(result.content, 'lxml')
            tittle = result.select('div.entry-header')[0].text
            content = result.select('div.entry')[0].text
            insert(tittle, content)


if __name__ == '__main__':
    getdata()
