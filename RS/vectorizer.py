# coding=utf-8
from __future__ import print_function
import sys
import cPickle as pickle
import os
from sklearn.feature_extraction.text import HashingVectorizer, TfidfTransformer
from sklearn.pipeline import make_pipeline
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
        # Perform an IDF normalization on the output of HashingVectorizer
        hasher = HashingVectorizer(n_features=1000000,
                                   stop_words=stop_words, non_negative=True,
                                   norm=None, binary=False)
        vectorizer = make_pipeline(hasher, TfidfTransformer())

        print("start vectorizing...")
        # 转化向量
        X = vectorizer.fit_transform(contents)
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
            with open(filename, "rb") as f:
                text = f.read()
            return text
        else:
            raise Exception('文件：' + filename + " 不存在")


if __name__ == '__main__':
    vectorizer = Vectorizer()
    vectorizer.run()
