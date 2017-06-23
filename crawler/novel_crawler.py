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


def get_types():
    """ 爬取小说的类型 """
    html = get_body("http://www.suimeng.la/")
    soup = BeautifulSoup(html, "html.parser")
    lis = soup.find("ul", {"class": "fl"}).find_all("li")
    types = []
    index = 1
    for li in lis:
        name = li.text
        url = li.a.attrs['href']
        if "sort" in url:
            types.append({"name": name, "url": url, "index": index})
            index += 1
            print(name, url)
    return types


def get_page_num(url):
    html = get_body(url)
    soup = BeautifulSoup(html, "html.parser")

    return int(soup.find("div", {"id": "pagelink"}).find("a", {"class": "last"}).text)


class NovelCrawler:
    """ 爬取小说基本信息 """
    def __init__(self):
        self.client = init_client()
        self.db = self.client[config['db_name']]
        self.collection = self.db.novels
        self.collection.ensure_index('url', unique=True)

    def run(self):
        _types = get_types()
        for t in _types:
            for i in range(1, get_page_num(t["url"])+1):
                print("................正在爬取[%s]的第%d页................" % (t["name"], i))
                url = "http://www.suimeng.la/sort/%d-%d.html" % (t["index"], i)
                print(url)
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
        lis = soup.find("ul", {"class": "ultwo"}).find_all("li")
        for li in lis:
            name = li.find("a", {"class": "aname"}).text
            url = li.find("a", {"class": "aname"}).attrs['href']
            status = li.find("span", {"class": "aflag"}).text
            info = li.find("p", {"class": "gray"}).text
            author = info.split("\n")[0].split("：")[1].strip()
            category = info.split("\n")[1].split("：")[1].strip()
            novels.append(Novel(name, author, category, status, url))
            print(name, author, category, status, url)
        return novels


if __name__ == '__main__':
    crawler = NovelCrawler()
    crawler.run()
    print("novel_crawler has been finished.")
