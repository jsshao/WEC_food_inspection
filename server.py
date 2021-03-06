#!/usr/bin/env python
import json

from flask import Flask, Response, make_response, jsonify, send_from_directory
from analyze import load_data, load_data_as_df, group_by_restaurants, get_infractions_for_restaurant
from flask import render_template
# import sys  
# reload(sys)  
# sys.setdefaultencoding('utf8')

all_data = []
df_data = []
# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='/static')

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


@app.route('/restaurant/<rid>')
def stores(rid):
    res = None
    for entry in all_data:
        if entry['id'] == rid:
            res = entry
            break
    inf = get_infractions_for_restaurant(df_data, rid)
    for i in range(len(inf)):
        if isinstance(inf[i]['category_code'], basestring):
            inf[i]['category_code'] = inf[i]['category_code'].decode('utf-8','ignore').encode("utf-8")
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
        for infraction in infractions:
            infraction.pop('category_code', None)
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
