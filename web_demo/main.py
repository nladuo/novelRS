# coding=utf-8
from flask import Flask, send_from_directory
import cPickle as pickle
from bson.objectid import ObjectId
import json
import sys
sys.path.append("../")
from lib.utils import *
from lib.config import *

reload(sys)
sys.setdefaultencoding('utf8')


app = Flask(__name__, static_folder='dist')


def get_novels(name):
    client = init_client()
    collection = client[config['db_name']].novels
    novel = collection.find_one({
        'name': name,
        'success': True,
        'is_compute': True
    })
    if novel is None:
        return []
    result = []
    similarities = pickle.loads(str(novel['similarities']))
    for similarity in similarities[1:]:
        novel = collection.find_one({
            '_id': ObjectId(similarity.novel_id),
            'success': True,
            # 'is_compute': True
        })

        if novel is None:
            continue
        n = {
            'name': novel['name'],
            'author': novel['author'],
            'category': novel['category'],
            'word_num': novel['word_num'],
            'similarity': similarity.similarity
        }
        result.append(n)
    client.close()
    return result


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('./dist/static', path)


@app.route('/api/search/<name>')
def search(name=""):
    return json.dumps(get_novels(name))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=38438, debug=True)
