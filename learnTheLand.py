## ========================================================
## ========================================================
##				INSTALL WIKIPEDIA
## ========================================================
## ========================================================

import random

import requests

import wikipedia


app_id = "Q9WERY-K3HTGTL99H"
cache = {}
## Wikipedia Summary for cities
def getSummary(search):
    try:
        temp = wikipedia.summary(search)
    except:
        return search+"\n"+search + " was famous a location around here"
    temp = temp.split(".")

    res = temp[0]
    i = 0

    isOneSentence = True

    while isOneSentence:
        res = res + "."

        if ord(temp[i][len(temp[i]) - 1]) < 97 or ord(temp[i][len(temp[i]) - 1]) > 122:
            res = res + temp[i + 1]
        else:
            isOneSentence = False

        i += 1

    return search + "\n" + res


## WIKIPEDIA SUMMARY FOR OTHER STUFF
def getSummaryPerson(search, city):
    try:
        temp = wikipedia.summary(search + " " + city)
    except:
        return search+"\n"+search + "was famous in " + city
    temp = temp.split(".")

    res = temp[0]
    i = 0

    isOneSentence = True

    while isOneSentence:
        res = res + "."

        if ord(temp[i][len(temp[i]) - 1]) < 97 or ord(temp[i][len(temp[i]) - 1]) > 122:
            res = res + temp[i + 1]
        else:
            isOneSentence = False

        i += 1

    return search + "\n" + res


## LATITUDE (N) LONGITUDE (E)
def getCity(lat, lon):
    query = "http://api.wolframalpha.com/v2/query?appid=" + str(app_id) + "&input=" + str(lat) + "%20North%2C%20" + str(
        lon) + "%20East&format=plaintext&includepodid=CartographicNearestCity"

    if query not in cache:
        r = requests.get(query)

        startIndex = r.text.find("<plaintext>")  # +11
        endIndex = r.text.find("(")

        if startIndex == -1 or startIndex + 11 == endIndex:
            return "NULL"

        res = r.text[startIndex + 11:endIndex]
        res = res.replace(", United States", "")
        cache[query] = res

    return cache[query]


## POPULATION DATA:
def getPopulationData(city):
    query = "http://api.wolframalpha.com/v2/query?appid=" + str(app_id) + "&input= " + str(
        city) + " &format=plaintext&includepodid=Population:CityData"

    if query not in cache:
        r = requests.get(query)

        startIndex = r.text.find("<plaintext>")  # +11
        endIndex = r.text.find("(2012 estimate)")  # +15

        if startIndex == -1 or startIndex + 11 == endIndex:
            return "NULL"

        res = r.text[startIndex + 11:endIndex + 15]
        cache[query] = res

    return cache[query]


## CRIME DATA
def getCrimeData(city):
    query = "http://api.wolframalpha.com/v2/query?appid=" + str(app_id) + "&input=crime " + str(
        city) + " &format=plaintext&includepodid=Result"

    if query not in cache:
        r = requests.get(query)

        startIndex = r.text.find("<plaintext>")  # +11
        endIndex = r.text.find(")")

        if startIndex == -1 or startIndex + 11 == endIndex:
            return "NULL"

        res = r.text[startIndex + 11:endIndex + 1]
        cache[query] = res

    return cache[query]


## NICKNAMES
def getNickName(city):
    query = "http://api.wolframalpha.com/v2/query?appid=" + str(app_id) + "&input=nicknames " + str(
        city) + " &format=plaintext&includepodid=Result"

    if query not in cache:
        r = requests.get(query)

        startIndex = r.text.find("<plaintext>")  # +11
        endIndex = r.text.find("</plaintext>")

        if startIndex == -1 or startIndex + 11 == endIndex:
            return "NULL"

        res = r.text[startIndex + 11:endIndex]

        res = res.split("  |  ")

        cache[query] = res

    rand = int((len(cache[query])) * random.random())
    return cache[query][rand]


## LANDMARKS
def getLandmarks(city):
    query = "http://api.wolframalpha.com/v2/query?appid=" + str(
        app_id) + "&input=historical%20site%20within%2050%20miles%20of " + str(
        city) + "&format=plaintext&includepodid=Result&podstate=Result__More"

    if query not in cache:
        r = requests.get(query)

        startIndex = r.text.find("<plaintext>")  # +11
        endIndex = r.text.find("</plaintext>")

        ## NULL
        if startIndex == -1 or startIndex + 11 == endIndex:
            return "NONE"

        res = r.text[startIndex + 11:endIndex]
        res = res.split("\n")

        landmark = []  # Goodies

        for building in res:
            building = building.split("  ")
            landmark.append(building[0])

        cache[query] = landmark

    rand = int(len(cache[query]) * random.random())

    return cache[query][rand]


def getNotablePeople(city):
    query = "http://api.wolframalpha.com/v2/query?appid=" + str(app_id) + "&input=notable%20people%20in " + str(
        city) + " &format=plaintext&includepodid=Result"

    if query not in cache:
        r = requests.get(query)

        startIndex = r.text.find("<plaintext>")
        endIndex = r.text.find("</plaintext>")

        ## NULL
        if startIndex == -1 or startIndex + 11 == endIndex:
            return "NONE"

        res = r.text[startIndex + 11:endIndex]
        res = res.split("\n")

        names = []  # Goodies

        for person in res:
            person = person.split("  ")
            if len(person) != 2:
                continue
            name, date = person
            names.append(name)

        cache[query] = names

    rand = int(len(cache[query]) * random.random())

    return cache[query][rand]

## EXECUTION
if __name__ == "__main__":
    test = "Nashville, Tennessee"

    print getNickName(test)
    print getNickName(test)

    landmark = getLandmarks(test)
    print landmark
    print getLandmarks(test)

    print getPopulationData(test)
    print getPopulationData(test)

    print getCrimeData(test)
    print getCrimeData(test)

    city = getCity(36.15, -86.76)
    print city
    print getCity(36.15, -86.76)

    person = getNotablePeople(test)
    print person
    print getNotablePeople(test)

    print getSummary(landmark)
    print getSummary(city)
    print getSummaryPerson(person, city)


