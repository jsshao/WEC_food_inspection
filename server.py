#!/usr/bin/env python
import json

from flask import Flask, Response, make_response, jsonify, send_from_directory
from analyze import load_data, load_data_as_df, group_by_restaurants, get_infractions_for_restaurant
from flask import render_template

all_data = []
df_data = []
# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='/static')

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


@app.route('/restaurant/<rid>')
def stores(rid):
    rid = '00213C39-2B44-4CEF-AF1D-627B7A4E7ADC'
    res = None
    for entry in all_data:
        if entry['id'] == rid:
            res = entry
            break
    print res
    inf = get_infractions_for_restaurant(df_data, rid)
    print 'jason cancer', inf[0]['category_code']
    print inf
    return render_template('restaurant.html', res=res, inf=inf)


@app.route('/violation.html')
def send_violations():
    return make_response(open('static/html/violation.html').read())


@app.route('/')
def root():
    return make_response(open('static/html/index.html').read())


@app.route('/data')
def all_restaurants():
    return Response(json.dumps(all_data),  mimetype='application/json')


@app.route('/top_k')
def top_k():
    all_data = load_data_as_df()
    top = group_by_restaurants(all_data, 10)
    results = []
    for g in top:
        infractions = g[1].T.to_dict().values()
        count = len(infractions)
        results.append({
            'infraction': infractions[0],
            'count': count
        })
    return Response(json.dumps(results),  mimetype='application/json')


if __name__ == "__main__":
    all_data = load_data()
    df_data = load_data_as_df()
    print "Load data done!"
    app.run(debug=True)
