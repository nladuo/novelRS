from flask import Flask, send_from_directory
import sys
sys.path.append("../")
from lib.utils import *
from lib.model import *
from lib.config import *

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
    print novel
    client.close()






@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('./dist/static', path)


@app.route('/api/<name>')
def search(name):
    get_novels(name)
    return "<h1>" + name + "</h1>"

if __name__ == '__main__':
    app.run(port=38438, debug=True)
