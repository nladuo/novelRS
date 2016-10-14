# coding=utf-8
from sklearn.feature_extraction.text import CountVectorizer
import os
import random
import sys
import cPickle as pickle
sys.path.append("../")
from lib.stop_words import *

reload(sys)
sys.setdefaultencoding('utf8')

if __name__ == '__main__':
    """ 对500本小说进行向量化，提取feature_names"""
    MAX_FILES_NUM = 500     # 随机提取500本小说

    filenames = os.listdir('./seg_corpus')
    random.shuffle(filenames)
    contents = [open('./seg_corpus/' + filename).read()
                for i, filename in enumerate(filenames) if i < MAX_FILES_NUM]

    vectorizer = CountVectorizer(stop_words=stop_words)
    vectorizer.fit(contents)

    f = open('vectorizer.dat', 'w')
    pickle.dump(vectorizer, f)
    print 'saved vectorizer.dat'

