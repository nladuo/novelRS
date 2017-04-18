# coding=utf-8
from __future__ import print_function
from sklearn.cluster import KMeans
import cPickle as pickle
from time import time
import numpy as np
import sys

reload(sys)
sys.setdefaultencoding('utf8')


if __name__ == "__main__":

    with open("./dataset.pickle", "rb") as f:
        X = np.load(f)
        print("shape of dataset:", X.shape)

    km = KMeans(init='k-means++', n_clusters=2, verbose=1)
    t0 = time()
    km.fit(X)
    print("done in %0.3fs" % (time() - t0))

    for center in km.cluster_centers_:
        print(center, km.predict(center))

    with open("km.pickle", "wb") as f:
        print("saving km.pickle...")
        pickle.dump(km, f, pickle.HIGHEST_PROTOCOL)

    print("kmeans_clustering has been finished.")
