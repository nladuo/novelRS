# coding=utf-8
from __future__ import print_function
from sklearn.cluster import MiniBatchKMeans
import sys
import cPickle as pickle
import json
import os
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
        ids = []
        # 先把数据的id读取到
        for novel in self.novels:
            ids.append(novel['_id'])
        print('loading dataset....')
        X = self.__load_dataset(ids)
        num_clusters = int(len(ids) / 300) + 1   # 平均每个cluster中300本小说
        print("num_clusters = ", num_clusters)
        print("starting clustering...")
        mbk = MiniBatchKMeans(init='k-means++', n_clusters=num_clusters, batch_size=100,
                      n_init=10, max_no_improvement=10, verbose=1,
                      random_state=0)
        mbk.fit(X)

        # 存到数据库中
        print("saving into database...")
        for i, _id in enumerate(ids):
            cluster = int(mbk.labels_[i])
            self.__update_novel(_id, cluster)
        # 关闭数据库
        self.__close()
        print("finished.")

    def __load_dataset(self, ids):
        dataset = []
        for _id in ids:
            text = self.__read_file(_id)
            dataset.append(json.loads(text))
        return dataset

    def __update_novel(self, novel_id, cluster):
        """ 更新novel的cluster """
        self.collection.update({'_id': ObjectId(novel_id)}, {
            '$set': {
                'cluster': cluster
            }
        })

    def __close(self):
        """ 关闭数据库 """
        self.client.close()

    @staticmethod
    def __read_file(_id):
        """ 读取corpus """
        filename = './vectors/' + str(_id) + '.dat'
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
