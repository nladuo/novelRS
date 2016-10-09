# coding=utf-8
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import operator
import cPickle
import sys
from datetime import datetime
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
        self.novels = self.collection.find({
            'success': True,
            'is_segment': True,
        })

    def run(self):

        novels = []
        # 先把数据都读到内存里
        for novel in self.novels:
            n = Novel(
                novel['name'],
                novel['author'],
                novel['category'],
                novel['word_num'],
                novel['url'],
                novel['is_crawled'],
                novel['success'],
                novel['is_segment'],
                novel['is_compute']
            )
            n._id = novel['_id']
            novels.append(n)

        count = 1       # 记录计算了几个
        # 开始分割
        for n in novels:
            if n.is_compute:    # 计算过相似度的就不再计算了
                continue
            nid = str(n._id)
            before_exec_time = datetime.now()
            similarities = []     # 保存所有的相似度
            content = self.__read_file(nid)
            print count, '---->', nid, "  ", n.name
            for n2 in novels:
                nid2 = str(n2._id)
                if (nid == nid2):
                    continue
                content2 = self.__read_file(nid2)
                similarity = self.__get_cosine_similarity(content, content2)
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

    def __get_cosine_similarity(self, text1, text2):
        """ 获取余弦相似度 """
        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform([text1, text2]).toarray()
        vec1 = np.array(X[0]).reshape(1, -1)
        vec2 = np.array(X[1]).reshape(1, -1)
        return cosine_similarity(vec1, vec2)[0][0]

    def __read_file(self, novel_id):
        """ 读取文件 """
        filename = './seg_corpus/' + novel_id + '.txt'
        if os.path.exists(filename):
            message = 'OK, the "%s" file exists.'
            f = open(filename, "rb")
            text = f.read()
            f.close()
            return text
        else:
            raise Exception('文件：' + filename + " 不存在")

    def __update_novel_similarities(self, novel_id, similarities):
        """ 更新novel集合的similarities和is_compute """
        similarities_str = cPickle.dumps(similarities[0: 30])
        self.collection.update({'_id': ObjectId(novel_id)}, {
            '$set': {
                'similarities': similarities_str,
                'is_compute': True
            },
        })

    def __close(self):
        self.client.close()


if __name__ == '__main__':
    counter = SimilarityCounter()
    counter.run()
