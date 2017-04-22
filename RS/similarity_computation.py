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
    """ 在cluster内计算相似度 """
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
        novel_set = {}
        # 先把数据都读到内存里
        for novel in self.novels:
            if not novel['cluster'] in novel_set:   # 根据cluster来计算相似度
                novel_set[novel['cluster']] = []
            novel_set[novel['cluster']].append(novel)

        count = 1       # 记录计算了几个
        for cluster, novels in novel_set.items():
            # 逐个计算
            for n in novels:
                if n['is_compute']:    # 计算过相似度的就不再计算了
                    continue
                nid = str(n['_id'])
                t0 = time()
                similarities = []     # 保存所有的相似度
                print(count, '---->', nid, "  ", n['name'], "  cluster:", cluster)
                for n2 in novels:
                    nid2 = str(n2['_id'])
                    if nid == nid2:
                        continue
                    similarity = self.__get_cosine_similarity(n['vector'], n2['vector'])
                    similarities.append(Similarity(nid2, similarity))
                # 对相似度进行排序，把前30个更新到数据库中
                similarities.sort(key=operator.attrgetter("similarity"), reverse=True)
                self.__update_novel_similarities(nid, similarities)
                print( "最相似的是:", self.__get_novel_name_by_id(similarities[0].novel_id),
                    "(", similarities[0].novel_id, ")",
                    " 相似度为：",similarities[0].similarity )
                print("耗时：%0.3fs" % (time() - t0), "秒")
                count += 1

        self.__close()  # 关闭数据库
        print("similarities counting finished.")

    def __get_novel_name_by_id(self, _id):
        novel = self.collection.find_one({'_id': ObjectId(_id)})
        return novel['name']

    def __update_novel_similarities(self, novel_id, similarities):
        """ 更新novel集合的similarities和is_compute """
        if len(similarities) < 30:
            similarities_str = pickle.dumps(similarities)
        else:
            similarities_str = pickle.dumps(similarities[0: 30])
        self.collection.update({'_id': ObjectId(novel_id)}, {
            '$set': {
                'similarities': similarities_str,
                'is_compute': True
            },
        })

    def __close(self):
        self.client.close()

    @staticmethod
    def __get_cosine_similarity(vector1, vector2):
        """ 获取余弦相似度 """
        vec1 = pickle.loads(str(vector1))
        vec2 = pickle.loads(str(vector2))

        vec1 = np.array(vec1).reshape(1, -1)
        vec2 = np.array(vec2).reshape(1, -1)

        return cosine_similarity(vec1, vec2)[0][0]


if __name__ == '__main__':
    computer = SimilarityComputation()
    computer.run()

    # with open("./dataset.pickle", "rb") as f:
    #     X = np.load(f)
    #     print("shape of dataset:", X.shape)
    #
    # t0 = time()
    # # 转化向量
    # print(cosine_similarity(X[0], X[1])[0][0])
    # print("done in %0.3fs" % (time() - t0))

