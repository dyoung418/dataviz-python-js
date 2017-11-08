# server_nosql.py
import flask
import dataset
import bson.json_util

app = flask.Flask(__name__)

db = dataset.connect('sqlite:///data/nobel_winners.db')

@app.route('/api/winners')
def get_country_data():
    print('Request args: ' + str(dict(flask.request.args)))
    query_dict = {}
    for key in ['country', 'category', 'year']:
        arg = flask.request.args.get(key) # gives args of request ('?country=Australia&categor=Chemistry')
        if arg:
            query_dict[key] = arg
    winners = db['winners'].find(**query_dict)
    if winners:
        return dumps(winners) # this dumps can serialize date objects
    flask.abort(404) # resource not found

if __name__ == '__main__':
    app.run(port=8000, debug=True)

