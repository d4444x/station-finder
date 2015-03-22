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
    city = request.args.get('city')
    categories = request.args.get('categories').split(",")
    state = request.args.get('state')
    print city,state,categories
    if categories==[""]:
        categories = ["Country"]
    ls = db.get_stations_mason(city,state,categories)
    print ls
    return json.dumps({"stations":[station[1] for station in ls]})




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, threaded=True,debug=True)