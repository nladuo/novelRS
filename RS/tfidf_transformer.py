# coding=utf-8
from sklearn.feature_extraction.text import TfidfTransformer
import sys
import cPickle as pickle
import json
import os
import numpy as np
from bson.objectid import ObjectId
sys.path.append("../")
from lib.model import *
from lib.utils import *
from lib.config import *

reload(sys)
sys.setdefaultencoding('utf8')


class MyTransformer:
    def __init__(self):
        self.client = init_client()
        self.db = self.client[config['db_name']]
        self.collection = self.db.novels
        self.collection.ensure_index('url', unique=True)
        self.novels = self.collection.find({
            'success': True,
            'is_segment': True,
        })

    def run(self):
        novels = []
        # 先把数据都读到内存里
        for novel in self.novels:
            novels.append(novel)
        X = []
        print "start transforming."
        # 读取向量
        for novel in novels:
            X.append(json.loads(novel['vector']))
        X = np.array(X)     # 转换为numpy的数组
        # 转换为tf-idf
        transformer = TfidfTransformer()
        tfidf = transformer.fit_transform(X).toarray().tolist()
        # 存到数据库中
        print "saving into database."
        for i, novel in enumerate(novels):
            vector = json.dumps(tfidf[i])
            self.__update_novel(novel['_id'], vector)
        # 关闭数据库
        self.__close()
        print "finished."

    def __update_novel(self, novel_id, vector):
        """ 更新novel的tfidf_vector """
        self.collection.update({'_id': ObjectId(novel_id)}, {
            '$set': {
                'tfidf_vector': vector
            },
        })

    def __close(self):
        """ 关闭数据库 """
        self.client.close()

    @staticmethod
    def __read_file(_id):
        """ 读取corpus """
        filename = '../crawler/corpus/' + _id + '.txt'
        if os.path.exists(filename):
            f = open(filename, "rb")
            text = f.read()
            f.close()
            return text
        else:
            raise Exception('文件：' + filename + " 不存在")

    @staticmethod
    def __get_vectorizer():
        """ 读取vectorizer.dat """
        f = open('vectorizer.dat', 'r')
        vectorizer = pickle.load(f)
        f.close()
        return vectorizer


if __name__ == '__main__':
    tfidf_transformer = MyTransformer()
    tfidf_transformer.run()
