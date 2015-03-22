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
    if not session.has_key("time"):
        session["time"] = None
    lat = float(request.args.get('lat'))
    long = float(request.args.get("lng"))
    if not lat or not long:
        return "Lat or long not given"

    if session["time"] and session["time"]-time.now()>500:
        session["time"] = None
    elif session.has_key("lat") and session.has_key("long"):
        lat = session["lat"]
        long = session["long"]

    if session["time"] == None:
        session["lat"] = lat
        session["long"] = long
        session["city"] = learnTheLand.getCity(lat,long)

    r = random.randint(1,80)
    city = session["city"]
    if r <5:
        say = "In "+city+" there are " +learnTheLand.getCrimeData(city)
    elif r<10:
        say = city+" is also known as "+ learnTheLand.getNickName(city)
    elif r<50:
        person = learnTheLand.getNotablePeople(city)
        say = learnTheLand.getSummaryPerson(person,city)
        if person not in say:
            say = person + " "+ say
        say = "Born in "+city+" "+say
    else:
        landmark = learnTheLand.getLandmarks(city)
        say = learnTheLand.getSummary(landmark)
        if landmark not in say:
            say = landmark+" "+say
            say = say
        say = "In "+city+" "+say

    print say
    return jsonify({"to_say":say})








if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, threaded=True,debug=True)