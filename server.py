from flask import Flask, make_response, request, send_from_directory

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='/static')


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


@app.route('/')
def root():
    return make_response(open('static/index.html').read())


if __name__ == "__main__":
    app.run(debug=True)
