# coding=utf-8
from __future__ import print_function
import jieba
import os
import sys
from bson.objectid import ObjectId
sys.path.append("../")
from lib.config import *
from lib.utils import *
from lib.model import *

reload(sys)
sys.setdefaultencoding('utf8')


class WordSegmentation:
    """ 使用jieba进行分词 """
    def __init__(self):
        self.client = init_client()
        self.db = self.client[config['db_name']]
        self.collection = self.db.novels
        self.collection.ensure_index('url', unique=True)
        self.novels = self.collection.find({
            'success': True,
            'is_segment': False
        })

    def run(self):
        novels = []
        # 先把数据都读到内存里
        for novel in self.novels:
            novels.append(novel)
        # 开始分割
        for novel in novels:
            print("spliting ", novel['_id'], novel['name'])
            text = self.__read_file(str(novel['_id']))
            text = self.__segment(text)
            self.__save_file(str(novel['_id']), text)
            self.__update_novel(novel['_id'])
        # 关闭数据库
        self.__close()
        print("word segmentation finished.")

    def __update_novel(self, novel_id):
        """ 更新is_segment """
        self.db.novels.update({'_id': ObjectId(novel_id)}, {
            '$set': {
                'is_segment': True
            }
        })

    def __close(self):
        """ 关闭数据库 """
        self.client.close()

    def __segment(self, text):
        """ 用结巴分词 """
        words = jieba.cut(text)
        return " ".join(words)

    @staticmethod
    def __read_file(_id):
        """ 读取corpus """
        filename = '../crawler/corpus/' + _id + '.txt'
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                text = f.read()
            return text
        else:
            raise Exception('文件：' + filename + " 不存在")

    @staticmethod
    def __save_file(_id, text):
        """ 保存到seg_corpus """
        filename = 'seg_corpus/' + _id + '.txt'
        with open(filename, "wb") as f:
            f.write(text)


if __name__ == '__main__':
    segmenter = WordSegmentation()
    segmenter.run()
