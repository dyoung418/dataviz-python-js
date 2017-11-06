import flask

app = flask.Flask(__name__)

winners = [
        {'name': 'Albert Einstein', 'category':'Physics'},
        {'name': 'V.S. Naipaul', 'category':'Literature'},
        {'name': 'Dorothy Hodgkin', 'category':'Chemistry'}
        ]

@app.route("/")  #directs traffic.  "/" goes to root, i.e. http://localhost:8000
def hello():
    return "Hello World! <a href=/demolist>demolist</a>"

@app.route("/demolist")
def demo():
    return flask.render_template('testj2.html', heading="A little winners' list",
            winners=winners)

if __name__ == "__main__":
    app.run(port=8000, debug=True)
