# coding=utf-8
from __future__ import print_function
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
import numpy as np
import sys
from time import time
import cPickle as pickle


reload(sys)
sys.setdefaultencoding('utf8')


if __name__ == "__main__":
    print("loading ./dataset.pickle...")
    with open("./dataset.pickle", "rb") as f:
        X = np.load(f)
        print("shape of dataset:", X.shape)

    # 降维并归一化
    t0 = time()
    print("starting decomposition....")
    svd = TruncatedSVD(100)
    normalizer = Normalizer(copy=False)
    lsa = make_pipeline(svd, normalizer)

    X = lsa.fit_transform(X)

    print("done in %fs" % (time() - t0))

    # 保存模型, 用于Kmeans聚类
    print("saving decomposed_dataset.....")
    with open("decomposed_dataset.pickle", "wb") as f:
        pickle.dump(X, f, pickle.HIGHEST_PROTOCOL)

    # 保存模型, 用于以后的在线学习
    print("saving lsa.pickle.....")
    with open("lsa.pickle", "wb") as f:
        pickle.dump(X, f, pickle.HIGHEST_PROTOCOL)


    print("decomposition has been finished")

