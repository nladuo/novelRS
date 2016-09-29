# coding=utf-8

from model import *
from utils import *
from config import *
from bs4 import BeautifulSoup
import sys


reload(sys)
sys.setdefaultencoding('utf8')


class NovelCrawler:

    def __init__(self):
        self.client = init_client()
        self.db = self.client[config['db_name']]
        self.collection = self.db.novels

    def run(self):
        for i in range(1, 647):
            print ".....................正在爬取第", i, "页....................."
            url = "http://www.23wx.com/quanben/" + str(i)
            html = get_body(url)
            if html == '':
                add_failed_url(self.db, url)
            novels = self.__parse(html)
            self.__add_novels(novels)
        self.__close()

    def __parse(self, html):
        novels = []
        bs_obj = BeautifulSoup(html)
        trs = bs_obj.find_all('tr', {'bgcolor': '#FFFFFF'})
        for tr in trs:
            tds = tr.find_all("td")
            name = tds[0].text
            html2 = get_body(tds[0].a.attrs['href'])
            bs_obj2 = BeautifulSoup(html2)
            url = bs_obj2.find('a', {'class': 'read'}).attrs['href']
            word_num = bs_obj2.find_all('td')[0].text
            category = bs_obj2.find_all('td')[4].text
            author = tds[2].text
            novels.append(Novel(name, author, category, word_num, url, False, True))
            print name, author, category,  word_num, url
        return novels

    def __add_novels(self, novels):
        for novel in novels:
            if self.collection.find({'url': novel.url}).count() == 0:
                self.collection.insert(novel.dict())

    def __close(self):
        self.client.close()


crawler = NovelCrawler()
crawler.run()
