#!/usr/bin/env python
import json

from flask import Flask, Response, make_response, jsonify, send_from_directory
from analyze import load_data
from flask import render_template

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='/static')


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


@app.route('/restaurant/<rid>')
def stores(rid):
    res = []
    for entry in all_data:
        if entry['id'] == rid:
            res = entry
            break
    return render_template('restaurant.html', res=[])


@app.route('/violation.html')
def send_violations():
    return make_response(open('static/html/violation.html').read())


@app.route('/')
def root():
    return make_response(open('static/html/index.html').read())


@app.route('/data')
def all_restaurants():
    return Response(json.dumps(all_data),  mimetype='application/json')


if __name__ == "__main__":
    app.run(debug=True)
    global all_data
    all_data = load_data()
