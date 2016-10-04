# coding=utf-8
import os
import time
from sklearn import datasets
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import sys

reload(sys)
sys.setdefaultencoding('utf8')


def get_cosine_similarity(text1, text2):
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform([text1, text2]).toarray()
    vec1 = np.array(X[0]).reshape(1, -1)
    vec2 = np.array(X[1]).reshape(1, -1)
    return cosine_similarity(vec1, vec2)[0][0]


def read_file(filename):
    filename = './seg_corpus/' + filename
    f = open(filename, "rb")
    text = f.read()
    f.close()
    return text

txts = os.listdir("./seg_corpus/")

for filename in txts:
    for filename2 in txts:
        if filename == filename2:
            continue
        text = read_file(filename)
        text2 = read_file(filename2)
        print get_cosine_similarity(text, text2)
        # time.sleep(2)

