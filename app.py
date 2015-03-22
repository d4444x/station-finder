__author__ = 'daxx'
from flask import Flask,render_template,request,jsonify,session
import random
app = Flask(__name__)
import json
import db
import learnTheLand
import time

app.secret_key = '123ksjdfa9123afd'
categories = ["Country", "Spanish", "Christian", "Talk Radio", "Contemporary", "News", "Classical", "Sports", "Hits", "Alternative", "Oldies", "Jazz"]

@app.route('/')
def hello_world():
    return render_template("index.html", categories=sorted(categories))

@app.route('/get_station_2')
def get_station():
    city = request.args.get('city')
    categories = request.args.get('categories')[:-1].split(",")
    state = request.args.get('state')
    print city,state,categories

    ls = db.get_stations_mason(city,state,categories)
    print ls
    return jsonify({"stations":[station[1] for station in ls]})

@app.route("/get_station")
def lat_long():
    lat = float(request.args.get('lat'))
    long = float(request.args.get("lng"))
    categories = request.args.get('categories').split(",")
    categories.pop()
    if categories==[]:
        categories = ["Country"]
    print categories
    print request.args.get('categories')
    print "Looking up "+str(lat)+" "+str(long)+" "+str(categories)
    ls = db.get_stations_long_lat(lat,long,categories)
    print ls
    return jsonify({"stations":[station[1] for station in ls]})

@app.route("/land")
def get_info():
    if not session.has_key("time") or not session.has_key("to_say") or session["to_say"]==None:
        session["time"] = None
        session["to_say"] = []
    lat = float(request.args.get('lat'))
    long = float(request.args.get("lng"))
    if not lat or not long:
        return "Lat or long not given"
    if session["time"] and session["time"]-time.now()>500 or session["to_say"] or len(session["to_say"])==0:
        session["time"] = None

    if session["time"] == None:
        session["to_say"] = generate_to_say()
        session["time"] = time.now()
    say = session["to_say"].pop()
    print say
    return jsonify({"to_say":say})

def generate_to_say(lat, long):
    city = learnTheLand.getCity(lat,long)
    ret = learnTheLand.getLandmarks(city)
    # ret += learnTheLand.getNickName(city)
    # ret += learnTheLand.getCrimeData(city)
    people = learnTheLand.getNotablePeople(city)
    if len(people)>8:
        random.shuffle(people)
        people = people[:8]
    ret += people
    random.shuffle(ret)
    return ret







if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, threaded=True,debug=True)