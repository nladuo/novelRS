# -*- coding:utf-8 -*-
import pymongo
import requests
from .model import FailedUrl
from .config import *


def init_client():
    """ 初始化mongo客户端 """
    client = pymongo.MongoClient(config['db_host'], config['db_port'])
    if len(config['db_user']) != 0:
        admin = client['admin']
        admin.authenticate(config['db_user'], config['db_pass'])
    return client


def get_body(url):
    """ 发送http请求 """
    retry_times = 0
    while retry_times < 3:
        try:
            content = requests.get(url, timeout=config['timeout']).content
            return content
        except KeyboardInterrupt:
            print("KeyboardInterrupt, now_url:", url)
            raise
        except:
            retry_times += 1
    return ''


def add_failed_url(db, url):
    """ 把失败的url添加到数据库 """
    collection = db.failed_urls
    if collection.find({'url': url}).count() == 0:
        collection.insert(FailedUrl(url).dict())

def read_novel(path):
    with open(path, "r") as f:
        return f.read().decode("gb2312", 'ignore')
