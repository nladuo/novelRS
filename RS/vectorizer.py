# coding=utf-8
from __future__ import print_function
from sklearn.feature_extraction.text import TfidfVectorizer
import sys
import cPickle as pickle
import random
import json
import os
from bson.objectid import ObjectId
sys.path.append("../")
from lib.model import *
from lib.utils import *
from lib.config import *
from lib.stop_words import *

reload(sys)
sys.setdefaultencoding('utf8')


class Vectorizer:
    """ 章节内容向量化 """
    def __init__(self):
        self.client = init_client()
        self.db = self.client[config['db_name']]
        self.collection = self.db.novels
        self.collection.ensure_index('url', unique=True)
        self.novels = self.collection.find({
            'success': True,
            'is_segment': True
        })

    def run(self):
        novels = []
        # 先把数据都读到内存里
        for novel in self.novels:
            novels.append(novel)

        contents = [self.__read_file(novel['_id'])
                        for novel in novels]
        vectorizer = TfidfVectorizer(stop_words=stop_words, min_df=10, max_df=1000)
        print("start vectorizing...")
        X = vectorizer.fit_transform(contents).toarray()
        print('vocabulary num:', len(vectorizer.vocabulary_))
        # 开始保存
        for (i, novel) in enumerate(novels):
            print("saving", novel['name'])
            vector = json.dumps(X[i].tolist())
            self.__save_file(novel['_id'], vector)
            self.__update_novel(novel['_id'])
        # 关闭数据库
        self.__close()
        print("finished. all documents has been vectorized.")

    def __update_novel(self, novel_id):
        """ 更新novel的is_vectorize """
        self.collection.update({'_id': ObjectId(novel_id)}, {
            '$set': {
                'is_vectorize': True
            },
        })

    def __close(self):
        """ 关闭数据库 """
        self.client.close()

    @staticmethod
    def __read_file(_id):
        """ 读取corpus """
        filename = './seg_corpus/' + str(_id) + '.txt'
        if os.path.exists(filename):
            f = open(filename, "rb")
            text = f.read()
            f.close()
            return text
        else:
            raise Exception('文件：' + filename + " 不存在")

    @staticmethod
    def __save_file(_id, text):
        """ 保存到vectors """
        filename = 'vectors/' + str(_id) + '.dat'
        f = open(filename, "wb")
        f.write(text)
        f.close()


if __name__ == '__main__':
    vectorizer = Vectorizer()
    vectorizer.run()
