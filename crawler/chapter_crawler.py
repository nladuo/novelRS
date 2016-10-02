# coding=utf-8

from model import *
from utils import *
from config import *
from bs4 import BeautifulSoup
import sys


reload(sys)
sys.setdefaultencoding('utf8')


class ChapterCrawler:

    def __init__(self):
        pass

    def __parse(self):
        pass

url = "http://www.23wx.com/html/0/829/"

html = get_body(url)
bs_obj = BeautifulSoup(html)
tds = bs_obj.find_all('td', {'class', 'L'})
i = 1
for td in tds:
    print i, td.text
    i += 1


