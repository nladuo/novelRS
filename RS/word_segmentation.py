# coding=utf-8
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
        # 开始分割
        for novel in novels:
            print "spliting ", novel._id, novel.name
            text = self.__read_file(str(novel._id))
            text = self.__segment(text)
            self.__save_file(str(novel._id), text)
            self.__update_novel(novel._id)
        # 关闭数据库
        self.__close()
        print "word segmentation finished."


    def __segment(self, text):
        """ 用结巴分词 """
        words = jieba.cut_for_search(text)
        return " ".join(words)

    def __read_file(self, _id):
        """ 读取corpus """
        filename = '../crawler/corpus/' + _id + '.txt'
        if os.path.exists(filename):
            f = open(filename, "rb")
            text = f.read()
            f.close()
            return text
        else:
            raise Exception('文件：' + filename + " 不存在")

    def __save_file(self, _id, text):
        """ 保存到seg_corpus """
        filename = 'seg_corpus/' + _id + '.txt'
        f = open(filename, "wb")
        f.write(text)
        f.close()

    def __update_novel(self, novel_id):
        self.db.novels.update({'_id': ObjectId(novel_id)}, {
            '$set': {'is_segment': True},
        })

    def __close(self):
        self.client.close()


if __name__ == '__main__':
    jieba.enable_parallel(config['cpu_num'] - 1)  # 并发分词
    segmenter = WordSegmentation()
    segmenter.run()
