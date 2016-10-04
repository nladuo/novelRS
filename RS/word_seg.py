# coding=utf-8
import jieba
import os
import sys
from stop_words import *

reload(sys)
sys.setdefaultencoding('utf8')


def word_segmentation(text):
    words = jieba.cut_for_search(text)
    result = ''
    for word in words:
        if word in stop_words:
            continue
        result += word + " "
    return result


def read_file(filename):
    filename = '../crawler/corpus/' + filename
    f = open(filename, "rb")
    text = f.read()
    f.close()
    return text


def save_file(filename, text):
    filename = 'seg_corpus/1/' + filename
    f = open(filename, "wb")
    f.write(text)
    f.close()


if __name__ == '__main__':
    txts = os.listdir("../crawler/corpus/")
    for filename in txts:
        print filename
        text = read_file(filename)
        text = word_segmentation(text)
        save_file(filename, text)

    print "word segmentation finished."
