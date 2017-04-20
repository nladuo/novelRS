# coding=utf-8
from __future__ import print_function
from sklearn.cluster import KMeans
import cPickle as pickle
from time import time
import numpy as np
import sys

reload(sys)
sys.setdefaultencoding('utf8')


X = None # 定义数据集
num_cluster = 0


class TreeNode:
    """ 定义二叉树节点 """

    def __init__(self, sequence, center, cluster, parent, X):
        global num_cluster
        num_cluster += 1
        print("cluster num:", num_cluster, sequence.shape[0])
        self.parent = parent      # 定义父节点
        self.sequence = sequence  # 定义截取的序列
        self.center = center      # 定义聚类中心
        self.cluster = cluster
        self.X = X

        if sequence.shape[0] < 100:
            self.km = None          # 定义分类器
            self.left_node = None
            self.right_node = None
        else:
            self.km = KMeans(init='k-means++', n_clusters=2, verbose=1)
            x = self.__get_dataset()
            print("x:", x.shape)

            y = self.km.fit_predict(x)
            del x   # 释放内存


            self.left_node = TreeNode(sequence=np.argwhere(y==0)[:,0], center=self.km.cluster_centers_[0],
                                      cluster=0, parent=self)
            self.right_node = TreeNode(sequence=np.argwhere(y==1)[:,0], center=self.km.cluster_centers_[1],
                                       cluster=1, parent=self)

    def __get_dataset(self):
        sequences = []
        clusters = []
        p = self
        while p is not None:
            sequences.append(p.sequence)
            clusters.append(p.cluster)
            p = p.parent

        x = X
        for seq  in sequences[::-1]:
            x = x[seq]

        print("computing cluster: ", end="")
        for cls in clusters[::-1]:
            print(cls, end="")
        print("")
        return x


class BinaryTree:
    """ 定义二叉树跟节点 """

    def __init__(self):
        # 定义分类器
        self.km = KMeans(init='k-means++', n_clusters=2, verbose=1)
        self.left_node = None
        self.right_node = None

    def build(self):
        y = self.km.fit_predict(X)
        self.left_node = TreeNode(sequence=np.argwhere(y==0)[:,0], center=self.km.cluster_centers_[0],
                                  cluster=0, parent=None)
        self.right_node = TreeNode(sequence=np.argwhere(y == 1)[:, 0], center=self.km.cluster_centers_[1],
                                   cluster=1, parent=None)


if __name__ == "__main__":

    with open("./dataset.pickle", "rb") as f:
        X = np.load(f)
        print("shape of dataset:", X.shape)
    num_cluster = 0

    kmeans_tree = BinaryTree()
    kmeans_tree.build()

    print("the total cluster: ", num_cluster)

    print("saving ./kmeans_tree.pickle...")
    with open("./kmeans_tree.pickle", "wb") as f:
        pickle.dump(kmeans_tree, f)

    print("clustering has been finished.")
