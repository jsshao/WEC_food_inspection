#!/usr/bin/env python
import json

from flask import Flask, Response, make_response, jsonify, send_from_directory
from analyze import load_data
from flask import render_template

all_data = []
# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='/static')

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


@app.route('/restaurant/<rid>')
def stores(rid):
    return render_template('restaurant.html', name='ABCD', entries=[])


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
    all_data = load_data()
    print "Load data done!"
    app.run(debug=True)
