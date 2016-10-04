# coding=utf-8
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import operator
import cPickle
import sys
from bson.objectid import ObjectId
sys.path.append("../")
from lib.model import *
from lib.utils import *
from lib.config import *

reload(sys)
sys.setdefaultencoding('utf8')


class SimilarityCounter:

    def __init__(self):
        self.client = init_client()
        self.db = self.client[config['db_name']]
        self.collection = self.db.novels
        self.collection.ensure_index('url', unique=True)

    def run(self):
        txts = os.listdir("./seg_corpus/")
        count = 1
        for filename in txts:
            if filename == '.gitignore':
                continue
            similarities = []
            novel_id = os.path.splitext(filename)[0]
            print count, '---->', novel_id
            for filename2 in txts:
                if (filename == filename2) or (filename2 == '.gitignore'):
                    continue
                text = self.__read_file(filename)
                text2 = self.__read_file(filename2)
                _id = os.path.splitext(filename2)[0]
                similarity = self.__get_cosine_similarity(text, text2)
                similarities.append(Similarity(_id, similarity))
            # 对相似度进行排序，把前30个更新到数据库中
            similarities.sort(key=operator.attrgetter("similarity"), reverse=True)
            self.__update_novel_similarities(novel_id, similarities)
            print "The most similar one is :", similarities[0]._id, similarities[0].similarity
            count += 1
        self.__close()

    def __get_cosine_similarity(self, text1, text2):
        """ 获取余弦相似度 """
        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform([text1, text2]).toarray()
        vec1 = np.array(X[0]).reshape(1, -1)
        vec2 = np.array(X[1]).reshape(1, -1)
        return cosine_similarity(vec1, vec2)[0][0]

    def __read_file(self, filename):
        """ 读取文件 """
        filename = './seg_corpus/' + filename
        f = open(filename, "rb")
        text = f.read()
        f.close()
        return text

    def __update_novel_similarities(self, novel_id, similarities):
        """ 更新novel集合的variables """
        similarities_str = cPickle.dumps(similarities[0: 30])
        self.collection.update({'_id': ObjectId(novel_id)}, {
            '$set': {'similarities': similarities_str},
        })

    def __close(self):
        self.client.close()


if __name__ == '__main__':
    counter = SimilarityCounter()
    counter.run()
