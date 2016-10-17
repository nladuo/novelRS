# coding=utf-8
import os
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import operator
import cPickle as pickle
import sys
import json
from datetime import datetime
from bson.objectid import ObjectId
sys.path.append("../")
from lib.model import *
from lib.utils import *
from lib.config import *

reload(sys)
sys.setdefaultencoding('utf8')


class SimilarityCounter:
    """ 在cluster内计算相似度 """
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
        novel_set = {}
        # 先把数据都读到内存里
        for novel in self.novels:
            if not novel['cluster'] in novel_set:   # 根据cluster来计算相似度
                novel_set[novel['cluster']] = []
            novel_set[novel['cluster']].append(novel)

        count = 1       # 记录计算了几个
        for cluster, novels in novel_set.items():
            for n in novels:
                if n['is_compute']:    # 计算过相似度的就不再计算了
                    continue
                nid = str(n['_id'])
                before_exec_time = datetime.now()
                similarities = []     # 保存所有的相似度
                vector = self.__get_vector_by_id(nid)
                print count, '---->', nid, "  ", n['name'], "  cluster:", cluster
                for n2 in novels:
                    nid2 = str(n2['_id'])
                    if nid == nid2:
                        continue
                    vector2 = self.__get_vector_by_id(nid2)
                    similarity = self.__get_cosine_similarity(vector, vector2)
                    similarities.append(Similarity(nid2, similarity))
                # 对相似度进行排序，把前30个更新到数据库中
                similarities.sort(key=operator.attrgetter("similarity"), reverse=True)
                self.__update_novel_similarities(nid, similarities)
                print "最相似的是:", self.__get_novel_name_by_id(similarities[0]._id), \
                    "(", similarities[0]._id, ")", \
                    " 相似度为：",similarities[0].similarity
                after_exec_time = datetime.now()
                print "耗时：", (after_exec_time - before_exec_time).seconds, "秒"
                count += 1
        # 关闭数据库
        self.__close()
        print "similarities counting finished."

    def __get_novel_name_by_id(self, id):
        novel = self.collection.find_one({'_id': ObjectId(id)})
        return novel['name']

    def __update_novel_similarities(self, novel_id, similarities):
        """ 更新novel集合的similarities和is_compute """
        similarities_str = pickle.dumps(similarities[0: 30])
        self.collection.update({'_id': ObjectId(novel_id)}, {
            '$set': {
                'similarities': similarities_str,
                'is_compute': True
            },
        })

    def __close(self):
        """ 关闭数据库 """
        self.client.close()

    @staticmethod
    def __get_vector_by_id(_id):
        text = SimilarityCounter.__read_file(_id)
        return json.loads(text)

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

    @staticmethod
    def __get_cosine_similarity(vector1, vector2):
        """ 获取余弦相似度 """
        vec1 = np.array(vector1).reshape(1, -1)
        vec2 = np.array(vector2).reshape(1, -1)

        return cosine_similarity(vec1, vec2)[0][0]


if __name__ == '__main__':
    counter = SimilarityCounter()
    counter.run()
