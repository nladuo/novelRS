# coding=utf-8
from __future__ import print_function
import sys
import cPickle as pickle
import os
from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.pipeline import make_pipeline
from time import time
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
            'is_crawled': True,
            'is_segment': True
        })

    def run(self):
        novels = []
        # 先把数据都读到内存里
        for novel in self.novels:
            novels.append(novel)

        contents = [self.__read_file(novel['_id'])
                        for novel in novels]
        vectorizer = CountVectorizer(input="file",min_df=10, max_df=1000,
                                   stop_words=stop_words)

        print("start vectorizing...")
        t0 = time()
        # 转化向量
        X = vectorizer.fit_transform(contents)
        print("done in %0.3fs" % (time() - t0))
        with open("dataset.pickle", "w") as f:
            print("saving dataset.....")
            pickle.dump(X, f, pickle.HIGHEST_PROTOCOL)


        # 保存模型
        with open("vectorizer.pickle", "w") as f:
            print("saving vectorizer model.....")
            pickle.dump(vectorizer, f)

        # 关闭数据库
        self.__close()
        print("finished. all documents has been vectorized.")


    def __close(self):
        """ 关闭数据库 """
        self.client.close()

    @staticmethod
    def __read_file(_id):
        """ 读取corpus """
        filename = './seg_corpus/' + str(_id) + '.txt'
        if os.path.exists(filename):
            return open(filename, "rb")
        else:
            raise Exception('文件：' + filename + " 不存在")


if __name__ == '__main__':
    vectorizer = Vectorizer()
    vectorizer.run()
