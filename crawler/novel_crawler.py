# coding=utf-8
from __future__ import print_function
from bs4 import BeautifulSoup
import sys
sys.path.append("../")
from lib.utils import *
from lib.model import *
from lib.config import *


reload(sys)
sys.setdefaultencoding('utf8')


def get_page_num():
    """ 爬取小说的页数 """
    html = get_body("http://www.23us.com/quanben/1")
    soup = BeautifulSoup(html, "html.parser")
    page_num_str = soup.find("div", {"id": "pagelink"}).find("a", {"class": "last"}).text
    return int(page_num_str)


class NovelCrawler:
    """ 爬取小说基本信息 """
    def __init__(self):
        self.client = init_client()
        self.db = self.client[config['db_name']]
        self.collection = self.db.novels
        self.collection.ensure_index('url', unique=True)

    def run(self):
        for i in range(1, get_page_num()+1):
            print(".....................正在爬取第", i, "页.....................")
            url = "http://www.23us.com/quanben/" + str(i)
            html = get_body(url)
            if html == '':
                add_failed_url(self.db, url)
            novels = self.__parse(html)
            self.__add_novels(novels)
        self.__close()

    def __add_novels(self, novels):
        for novel in novels:
            try:
                self.collection.insert(novel.dict())
            except: pass

    def __close(self):
        """ 关闭数据库 """
        self.client.close()

    @staticmethod
    def __parse(html):
        """ 解析小说 """
        novels = []
        soup = BeautifulSoup(html, "html.parser")
        trs = soup.find_all('tr', {'bgcolor': '#FFFFFF'})
        for tr in trs:
            tds = tr.find_all("td")
            name = tds[0].find_all("a")[1].text
            url = tds[1].a.attrs['href']
            html2 = get_body(tds[0].a.attrs['href'])
            soup2 = BeautifulSoup(html2, "html.parser")
            category = soup2.find_all('td')[0].text.strip()
            word_num = soup2.find_all('td')[4].text
            author = tds[2].text
            novels.append(Novel(name, author, category, word_num, url))
            print(name, author, category, word_num, url)
        return novels


if __name__ == '__main__':
    crawler = NovelCrawler()
    crawler.run()
    print("novel_crawler has been finished.")
