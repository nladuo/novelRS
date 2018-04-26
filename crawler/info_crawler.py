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


def get_page_num(html):
    soup = BeautifulSoup(html, "html.parser")
    a = soup.find("div", {"class": "tspage"}).find_all("a")[1]
    page_str = a.attrs["href"].split("/")[-1].replace("index_", "").replace( ".html", "")
    return int(page_str)


class InfoCrawler:
    """ 爬取小说基本信息 """
    def __init__(self):
        self.client = init_client()
        self.db = self.client[config['db_name']]
        self.collection = self.db.novels
        self.collection.ensure_index('url', unique=True)

    def run(self):
        # 只爬取武侠仙侠和玄幻奇幻两个部分
        start_urls = [
            "https://www.qisuu.la/soft/sort01/",
            "https://www.qisuu.la/soft/sort02/"
        ]

        # For中断重新爬取
        start_index = {
            "https://www.qisuu.la/soft/sort01/": 1,
            "https://www.qisuu.la/soft/sort02/": 1
        }

        # 开始爬取
        for start_url in start_urls:
            html = get_body(start_url)
            if html == "":
                raise Exception("Error download init url: %s" % start_url )
            page_num = get_page_num(html)
            print(start_url, "page_num:", page_num)
            for page in range(start_index[start_url], page_num + 1):
                url = start_url + "index_%d.html" % page
                if page == 1:
                    url = start_url
                print("正在爬取:", url)
                html = get_body(url)
                if html == "":
                    add_failed_url(self.db, url);continue
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
        # print(html)
        novels = []
        soup = BeautifulSoup(html, "html.parser")
        lis = soup.find("div", {"class": "listBox"}).find_all("li")
        for li in lis:
            for i, child in enumerate(li.children):
                if i == 3:
                    url = "https://www.qisuu.la" + child.attrs["href"]
                    # 下载详情页面
                    html2 = get_body(url)
                    soup2 = BeautifulSoup(html2, "html.parser")
                    abstract = soup2.find("div", {"class": "showInfo"}).get_text()
                    author = soup2.find("div", {"class": "detail_right"}).find_all("li")[5].\
                        get_text().replace("书籍作者：", "")

                    name = soup2.find("div", {"class": "showDown"}).script.get_text().split("'")[5]

                    txt_url = soup2.find("div", {"class": "showDown"}).script.get_text().split("','")[1]

                    category = soup2.find("div", {"class": "wrap position"}).span.find_all("a")[-2].get_text()
                    print("《"+name+"》", "作者:", author, "类别:", category, txt_url)
                    novels.append(Novel(name, url, author, category, abstract, txt_url))
        return novels


if __name__ == '__main__':
    crawler = InfoCrawler()
    crawler.run()
    print("info_crawler has been finished.")
