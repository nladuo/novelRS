from flask import Flask, send_from_directory

app = Flask(__name__, static_folder='dist')


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('./dist/static', path)


@app.route('/api/<name>')
def search(name):
    return "<h1>" + name + "</h1>"

if __name__ == '__main__':
    app.run(port=8888, debug=True)
