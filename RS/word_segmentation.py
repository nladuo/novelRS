# coding=utf-8
import jieba
import os
import sys

reload(sys)
sys.setdefaultencoding('utf8')


def word_segmentation(text):
    """ 用结巴分词 """
    words = jieba.cut_for_search(text)
    return " ".join(words)


def read_file(filename):
    """ 读取corpus """
    filename = '../crawler/corpus/' + filename
    f = open(filename, "rb")
    text = f.read()
    f.close()
    return text


def save_file(filename, text):
    """ 保存到seg_corpus """
    filename = 'seg_corpus/' + filename
    f = open(filename, "wb")
    f.write(text)
    f.close()


if __name__ == '__main__':
    jieba.enable_parallel(4)
    txts = os.listdir("../crawler/corpus/")
    for filename in txts:
        print filename
        text = read_file(filename)
        text = word_segmentation(text)
        save_file(filename, text)

    print "word segmentation finished."
