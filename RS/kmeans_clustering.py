# coding=utf-8
from __future__ import print_function
from sklearn.cluster import KMeans
import cPickle as pickle
from time import time
from bson.objectid import ObjectId
import numpy as np
import sys
sys.path.append("../")
from lib.utils import *
from lib.config import *


reload(sys)
sys.setdefaultencoding('utf8')

class Saver:
    """ 保存向量和簇编号到数据库 """
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.client = init_client()
        self.db = self.client[config['db_name']]
        self.collection = self.db.novels
        self.collection.ensure_index('url', unique=True)
        self.novels = self.collection.find({
            'success': True,
            'is_crawled': True,
            'is_segment': True
        })

    def save(self):
        print("start saving the vector and cluster...")
        index = 0
        for novel in self.novels:
            self.__save_one(novel["_id"], self.X[index], self.Y[index])
            index += 1
        self.__close()

    def __save_one(self, _id, x, y):
        vector = pickle.dumps(x)

        self.collection.update({'_id': ObjectId(_id)}, {
            '$set': {
                'vector': vector,
                'cluster': int(y),
                'is_compute': False
            }
        })

    def __close(self):
        self.client.close()


if __name__ == "__main__":

    with open("./decomposed_dataset.pickle", "rb") as f:
        X = np.load(f)
        print("shape of dataset:", X.shape)
    n_clusters = X.shape[0] / 500
    print("n_clusters is: %d" % n_clusters)
    km = KMeans(init='k-means++', n_clusters=n_clusters, verbose=1)
    t0 = time()
    Y = km.fit_predict(X)
    print("done in %0.3fs" % (time() - t0))

    for i in range(n_clusters):
        cluster_num = np.argwhere(Y == i)[:, 0].shape
        print(i, cluster_num)

    # 保存模型, 用于以后的在线学习
    with open("km.pickle", "wb") as f:
        print("saving km.pickle...")
        pickle.dump(km, f, pickle.HIGHEST_PROTOCOL)

    # 保存向量和簇编号到数据库
    saver = Saver(X, Y)
    saver.save()

    print("kmeans_clustering has been finished.")
