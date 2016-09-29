# -*- coding:utf-8 -*-
import pymongo
import requests
from model import FailedUrl
from config import *


def init_client():
    client = pymongo.MongoClient(config['db_host'], config['db_port'])
    if len(config['db_user']) != 0:
        admin = client['admin']
        admin.authenticate(config['db_user'], config['db_pass'])
    return client


def get_body(url):
    retry_times = 0
    while retry_times < 3:
        try:
            content = requests.get(url, timeout=config['timeout']).content
            return content
        except:
            retry_times += 1
    return ''


def add_failed_url(db, url):
    collection = db.failed_urls
    if collection.find({'url': url}).count() == 0:
        collection.insert(FailedUrl(url).dict())

