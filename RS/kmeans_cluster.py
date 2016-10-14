# coding=utf-8
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.cluster import KMeans
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


class KMeansCluster:
    """ KMeans聚类 """
    def __init__(self):
        self.client = init_client()
        self.db = self.client[config['db_name']]
        self.collection = self.db.novels
        self.collection.ensure_index('url', unique=True)
        self.novels = self.collection.find({
            'success': True,
            'is_segment': True,
            'is_vectorize': True
        })

    def run(self):
        novels = []
        # 先把数据都读到内存里
        for novel in self.novels:
            novels.append(novel)
        X = []
        # 读取tfidf向量
        for novel in novels:
            X.append(json.loads(novel['tfidf_vector']))
        X = np.array(X)     # 转换为numpy的数组

        num_clusters = int(len(novels) / 500) + 1   # 平均每个cluster中500本小说
        print "num_clusters = ", num_clusters
        print "starting clustering..."
        km = KMeans(n_clusters=num_clusters, init='random', n_init=1, verbose=1)
        km.fit(X)

        # 存到数据库中
        print "saving into database..."
        for i, novel in enumerate(novels):
            cluster = int(km.labels_[i])
            self.__update_novel(novel['_id'], cluster)
        # 关闭数据库
        self.__close()
        print "finished."

    def __update_novel(self, novel_id, cluster):
        """ 更新novel的cluster """
        self.collection.update({'_id': ObjectId(novel_id)}, {
            '$set': {
                'cluster': cluster
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


if __name__ == '__main__':
    cluster = KMeansCluster()
    cluster.run()
