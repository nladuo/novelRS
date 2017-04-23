# coding=utf-8
from __future__ import print_function
import sys
from time import time
import cPickle as pickle
from sklearn.neighbors import LSHForest

reload(sys)
sys.setdefaultencoding('utf8')

if __name__ == "__main__":
    print("loading ./dataset.pickle...")
    with open("./dataset.pickle", "rb") as f:
        X = pickle.load(f)
        print("shape of dataset:", X.shape)
    t0 = time()

    print("start fitting Locality Sensitive Hashing forest")
    lshf = LSHForest(min_hash_match=4, n_candidates=50, n_estimators=10,
          n_neighbors=30, radius=1.0, radius_cutoff_ratio=0.9,
          random_state=42).fit(X)

    print("done in %0.3fs" % (time() - t0))

    print("saving ./lshf.pickle")
    with open("./lshf.pickle", "wb") as f:
        pickle.dump(lshf, f, pickle.HIGHEST_PROTOCOL)

    print("lshf.py has been done")
