# flask_serve.py
import flask

app = flask.Flask(__name__)

@app.route('/')
def root():
    return flask.send_from_directory('.', 'index.html')

@app.route('/css/<file>')
def css(file):
    return flask.send_from_directory('css', file)

@app.route('/js/<file>')
def js(file):
    return flask.send_from_directory('js', file)

@app.route('/data/<file>')
def data(file):
    return flask.send_from_directory('data', file)

@app.route('/data/nwinners_by_country/<file>')
def country_data(file):
    return flask.send_from_directory('data/nwinners_by_country', file)

if __name__ == "__main__":
    app.run(port=8000)
