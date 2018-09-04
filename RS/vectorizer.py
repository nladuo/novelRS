# coding=utf-8
from __future__ import print_function
import sys
import cPickle as pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from time import time
sys.path.append("../")
from RS.lib.utils import *
from RS.lib.config import *
from RS.lib.stop_words import stop_words

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
        contents = [self.__read_file(novel['_id'])
                        for novel in self.novels]
        vectorizer = TfidfVectorizer(input="file", stop_words=stop_words, max_features=50000)

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
        print("Finished!! All documents has been vectorized.")


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
