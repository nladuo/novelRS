# coding=utf-8
from sklearn.feature_extraction.text import CountVectorizer
import sys
import cPickle as pickle
import random
import json
import os
from bson.objectid import ObjectId
sys.path.append("../")
from lib.model import *
from lib.utils import *
from lib.config import *
from lib.stop_words import *

reload(sys)
sys.setdefaultencoding('utf8')


class Vectorizer:
    """ 章节内容向量化 """
    def __init__(self):
        self.client = init_client()
        self.db = self.client[config['db_name']]
        self.collection = self.db.novels
        self.collection.ensure_index('url', unique=True)
        self.novels = self.collection.find({
            'success': True,
            'is_segment': True,
            'is_vectorize': False
        })

    def run(self):
        novels = []
        # 先把数据都读到内存里
        for novel in self.novels:
            novels.append(novel)
        vectorizer = self.__get_vectorizer()
        # 开始分割
        for novel in novels:
            print "vectorizing ", novel['_id'], novel['name']
            text = self.__read_file(str(novel['_id']))
            X = vectorizer.transform([text])
            vector = json.dumps(X.toarray().tolist()[0])
            self.__save_file(novel['_id'], vector)
            self.__update_novel(novel['_id'])
        # 关闭数据库
        self.__close()
        print "finished. all documents has been vectorized."

    def __update_novel(self, novel_id):
        """ 更新novel的is_vectorize """
        self.collection.update({'_id': ObjectId(novel_id)}, {
            '$set': {
                'is_vectorize': True
            },
        })

    def __close(self):
        """ 关闭数据库 """
        self.client.close()

    @staticmethod
    def __read_file(_id):
        """ 读取corpus """
        filename = './seg_corpus/' + _id + '.txt'
        if os.path.exists(filename):
            f = open(filename, "rb")
            text = f.read()
            f.close()
            return text
        else:
            raise Exception('文件：' + filename + " 不存在")

    @staticmethod
    def __save_file(_id, text):
        """ 保存到vectors """
        filename = 'vectors/' + str(_id) + '.dat'
        f = open(filename, "wb")
        f.write(text)
        f.close()

    @staticmethod
    def __get_vectorizer():
        if os.path.exists('vectorizer.dat'):
            f = open('vectorizer.dat', 'r')
            vectorizer = pickle.load(f)
            f.close()
        else:
            # 对其中的500本小说进行向量化，提取feature_names
            MAX_FILES_NUM = 500
            filenames = os.listdir('./seg_corpus')
            random.shuffle(filenames)
            print "loading dataset...."
            contents = [open('./seg_corpus/' + filename).read()
                        for i, filename in enumerate(filenames) if i < MAX_FILES_NUM]
            vectorizer = CountVectorizer(stop_words=stop_words, min_df=20, max_df=300)
            vectorizer.fit(contents)
            # 保存vectorizer
            f = open('vectorizer.dat', 'w')
            pickle.dump(vectorizer, f)
            f.close()

        print 'vocabulary num:', len(vectorizer.vocabulary_)
        return vectorizer


if __name__ == '__main__':
    vectorizer = Vectorizer()
    vectorizer.run()
