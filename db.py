import glob
from sets import Set

states = glob.glob("radio_info/*.stations")
categories = Set()
for state in states:
    f = open(state, "r")
    for l in f:
        if len(l.split("\t"))!=5:
            continue
        tag, station, city, _, category = l.split("\t")
        category = category.replace("\n","")
        if category:
#             print category
            categories.add(category)


states = glob.glob("radio_info/*.stations")

ss = {}


for state in states:
    f = open(state, "r")
    state = state[len("radio_info/"):].replace(".stations","")
    ss[state] = []
    for l in f:
        if len(l.split("\t"))!=5:
            continue
        tag, station, city, _, category = l.split("\t")
        category = category.replace("\n","")
        category = category.split("/")
        if category!=[""]:
            ss[state].append([tag, station, city, category])

# print ss.keys()

def matches(ls1,ls2):
    #Category from user should be second
    for i1 in ls1:
        for i2 in ls2:
            i1 = i1.lower()
            i2 = i2.lower()
            if i1.find(i2)!=-1:
                return True
    return False

for state in states:
    f = open(state, "r")
    state = state[55:].replace(".stations","")
    ss[state] = []
    for l in f:
        if len(l.split("\t"))!=5:
            continue
        tag, station, city, _, category = l.split("\t")
        category = category.replace("\n","")
        category = category.split("/")
        if category!=[""]:
            ss[state].append([tag, station, city, category])

def get_stations_matchin_category(state,category):
    stations = []
    for tag, station, city, cat in ss[state]:
        if matches(cat,category):
            stations.append([tag,cat])
    return stations

def filter_by_category(category,stations):
    stations_r = []
    for s in stations:
        tag, station, city, cat = s
        if matches(cat, category):
            stations_r.append(s)
    return stations_r

def filter_by_city(cities, stations):
    stations_r = []
    for s in stations:
        tag, station, city, cat = s
        if matches([city], cities):
            stations_r.append(s)
    return stations_r

def get_stations_asher(categories, city_state):
    for states,city in city_state:
        stations = []
        for state in states:
            pass

def get_stations_mason(city,state,categories):
    # print ss
    stations = ss[state.lower().replace(" ","")]
    stations = filter_by_city([city],stations)
    stations = filter_by_category(categories,stations)
    return stations

