__author__ = 'daxx'
from flask import Flask,render_template
app = Flask(__name__)

categories = ['Rock', 'News']

@app.route('/')
def hello_world():
    return render_template("index.html", categories=categories)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, threaded=True,debug=True)