# coding=utf-8
from __future__ import print_function
from sklearn.cluster import MiniBatchKMeans
import cPickle as pickle
from time import time
import numpy as np
import sys

reload(sys)
sys.setdefaultencoding('utf8')


if __name__ == "__main__":

    with open("./decomposed_dataset.pickle", "rb") as f:
        X = np.load(f)
        print("shape of dataset:", X.shape)
    n_clusters = X.shape[0] / 300
    print("n_clusters is: %d" % n_clusters)
    km = MiniBatchKMeans(init='k-means++', n_clusters=n_clusters, verbose=0)
    t0 = time()
    y = km.fit_predict(X)
    print("done in %0.3fs" % (time() - t0))

    # centers = []
    # for center in km.cluster_centers_:
    #     cluster = km.predict(center)
    #     print(center, km.predict(center))
    #     centers.append({
    #         "cluster": cluster,
    #         "center": center
    #     })

    print(y.shape)
    for i in range(n_clusters):
        print(i, np.argwhere(y == i)[:, 0].shape)

    # with open("center.pickle", "wb") as f:
    #     print("saving center.pickle...")
    #     pickle.dump(centers, f, pickle.HIGHEST_PROTOCOL)
    #
    # with open("km.pickle", "wb") as f:
    #     print("saving km.pickle...")
    #     pickle.dump(km, f, pickle.HIGHEST_PROTOCOL)

    print("kmeans_clustering has been finished.")
