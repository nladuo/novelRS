# coding=utf-8
from __future__ import print_function
from sklearn.metrics.pairwise import cosine_similarity
import operator
import cPickle as pickle
import sys
from bson.objectid import ObjectId
sys.path.append("../")
from lib.model import *
from lib.utils import *
from lib.config import *
from time import time
import numpy as np

reload(sys)
sys.setdefaultencoding('utf8')


class SimilarityComputation:
    """ 计算相似度 """
    def __init__(self, novel_name):
        self.client = init_client()
        self.db = self.client[config['db_name']]
        self.collection = self.db.novels
        self.collection.ensure_index('url', unique=True)
        self.novels = self.collection.find({
            'success': True,
            'is_crawled': True,
            'is_segment': True
        })
        self.search_novel = self.collection.find_one({"name": novel_name})

        with open("vectorizer.pickle", "rb") as f:
            self.vectorizer = pickle.load(f)

    def __get_vector(self, _id):
        filename = './seg_corpus/' + str(_id) + '.txt'
        X = self.vectorizer.transform([open(filename, "rb")])
        return X[0].toarray()


    def run(self):
        t0 = time()
        search_vec = self.__get_vector(self.search_novel["_id"])
        similarities = []
        for novel in self.novels:
            nid = novel["_id"]
            if nid == self.search_novel["_id"]:
                continue

            vec = self.__get_vector(nid)
            similarity = self.__get_cosine_similarity(search_vec, vec)
            similarities.append(Similarity(nid, similarity))

        similarities.sort(key=operator.attrgetter("similarity"), reverse=True)
        print("耗时：%0.3fs" % (time() - t0), "秒")

        for s in similarities[:30]:
            print(self.__get_novel_name_by_id(s.novel_id), "-->", s.similarity)

        self.__close()  # 关闭数据库


    def __get_novel_name_by_id(self, _id):
        novel = self.collection.find_one({'_id': ObjectId(_id)})
        return novel['name']


    def __close(self):
        self.client.close()

    @staticmethod
    def __get_cosine_similarity(vector1, vector2):
        """ 获取余弦相似度 """
        vec1 = np.array(vector1).reshape(1, -1)
        vec2 = np.array(vector2).reshape(1, -1)

        return cosine_similarity(vec1, vec2)[0][0]


if __name__ == '__main__':
    computer = SimilarityComputation("诛仙")
    computer.run()
