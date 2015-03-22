__author__ = 'daxx'
from flask import Flask,render_template,request
app = Flask(__name__)
import json
import db

categories = ["Country", "Spanish", "Christian", "Talk Radio", "Contemporary", "News", "Classical", "Sports", "Hits", "Alternative", "Oldies", "Jazz"]

@app.route('/')
def hello_world():
    return render_template("index.html", categories=sorted(categories))

@app.route('/get_station')
def get_station():
    city = request.args.get('username')
    categories = request.args.get('categories')
    state = request.args.get('state')
    return json.dumps(db.get_stations_mason(city,state,categories))




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, threaded=True,debug=True)