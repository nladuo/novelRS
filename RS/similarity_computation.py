# coding=utf-8
from __future__ import print_function
import cPickle as pickle
import sys
from bson.objectid import ObjectId
sys.path.append("../")
from RS.lib.model import *
from RS.lib.utils import *
from RS.lib.config import *
from scipy.sparse import csr_matrix

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

        # 加载数据集
        print("loading ./dataset.pickle...")
        with open("./dataset.pickle", "rb") as f:
            X = pickle.load(f)
            print("shape of dataset:", X.shape)

        # 加载lsh树
        print("loading ./lshf.pickle")
        with open("./lshf.pickle", "rb") as f:
            lshf = pickle.load(f)

        # 把相似度保存在数据库
        index_map = {}
        for index, novel in enumerate(self.novels):
            index_map[index] = novel

        for index in index_map.keys():
            novel = index_map[index]
            print(index, '---->', str(novel["_id"]), "  ", novel['name'])
            fit_matrix = csr_matrix(X[index, :].toarray())
            distances, indices = lshf.kneighbors(fit_matrix, n_neighbors=30)

            similarities = []
            for i, idex in enumerate(indices[0]):
                n = index_map[idex]
                similarities.append(Similarity(str(n["_id"]), 1.0-distances[0][i]))
            self.__update_novel_similarities(str(novel["_id"]), similarities)
            print("最相似的是:", self.__get_novel_name_by_id(similarities[1].novel_id),
                              "(", similarities[1].novel_id, ")",
                              " 相似度为：",similarities[1].similarity )

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


if __name__ == '__main__':
    computer = SimilarityComputation()
    computer.run()
