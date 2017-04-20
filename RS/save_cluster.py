# coding=utf-8
from __future__ import print_function
import cPickle as pickle
import sys
sys.path.append("../")
from lib.model import *
from lib.utils import *
from lib.config import *

reload(sys)
sys.setdefaultencoding('utf8')


def init_collection():
    client = init_client()
    db = client[config['db_name']]
    coll = db.novels
    coll.ensure_index('url', unique=True)
    return coll

if __name__ == "__main__":
    collection = init_collection()
    novels = collection.find({
        'success': True,
        'is_crawled': True,
        'is_segment': True
    })

    with open("km.pickle", "r") as f:
        print("loading km.pickle ...")
        km = pickle.load(f)

    with open("./vectorizer.pickle", "r") as f:
        print("loading vectorizer.pickle ...")
        vectorizer = pickle.load(f)

    print("start computation.")
    for novel in novels:
        f = open('seg_corpus/' + str(novel['_id']) + '.txt')
        vec = vectorizer.transform([f])
        which_cluster = int(km.predict(vec[0])[0])
        collection.update({'_id': novel['_id']}, {
            '$set': {
                'cluster': which_cluster
            }
        })
        print(novel['name'], which_cluster)

