import random
import wikipedia
import wolframalpha

app_id = "Q9WERY-K3HTGTL99H"
client = wolframalpha.Client(app_id)
cache = {}
## Wikipedia Summary for cities
def getSummary(search):
	temp = wikipedia.summary(search)
	temp = temp.split(".")
	
	res = temp[0]
	i = 0

	isOneSentence = True

	while isOneSentence:
		res = res + "."

		if ord(temp[i][len(temp[i]) - 1]) < 97 or ord(temp[i][len(temp[i]) - 1]) >122:
			res = res + temp[i + 1]
		else:
			isOneSentence = False

		i += 1

	return search + "\n" + res

## WIKIPEDIA SUMMARY FOR OTHER STUFF
def getSummaryPerson(search, city):

	temp = wikipedia.summary(search + " " + city)
	temp = temp.split(".")
	
	res = temp[0]
	i = 0

	isOneSentence = True

	while isOneSentence:
		res = res + "."

		if ord(temp[i][len(temp[i]) - 1]) < 97 or ord(temp[i][len(temp[i]) - 1]) >122:
			res = res + temp[i + 1]
		else:
			isOneSentence = False

		i += 1

	return search + "\n" + res

## LATITUDE (N) LONGITUDE (E)
def getCity(lat, lon):
	query = "%s North, %s East" % (lat, lon)

	if query not in cache:
		data = client.query(query)
		cache[query] = data
	
	try:
		res = (next(cache[query].nearestCityCenter).text).split("(")[0]
	except:
		getCity(lat, lon)

	res = res.replace(", United States", "")

	return res

## POPULATION DATA: 
def getPopulationData(city):
	query = city

	if query not in cache:
		data = client.query(query)
		cache[query] = data

	try:
		res = (next(cache[query].population).text).split("(")[0]
	except:
		getPopulationData(city)

	return res

## CRIME DATA
def getCrimeData(city):
	query = city

	if query not in cache:
		data = client.query(query)
		cache[query] = data

	try:
		res = (next(cache[query].crime).text).split("  ")[0] + " x national average"
	except:
		getCrimeData(city)

	return res

## NICKNAMES
def getNickName(city):
	query = city + " nicknames"

	if query not in cache:
		data = client.query(query)

		try:
			res = next(data.result).text
		except:
			getNickName(city)

		if res == "":
			return "NONE"

		res = res.split("  |  ")

		cache[query] = res

	rand = int((len(cache[query])-1) * random.random())

	return cache[query][rand]

## LANDMARKS
def getLandmarks(city):
	query = "Closest Historical Site " + city

	if query not in cache:
		data = client.query(query)

		try:
			result = next(data.landmark).text
		except:
			getLandmarks(city)

		landmark = [] # Goodies

		if result == "":
			return "NONE"

		result = result.split("\n")

		for building in result:
			building = building.split("  ")
			landmark.append(building[0])

		cache[query] = landmark

	rand = int((len(cache[query])-1) * random.random())

	return cache[query][rand]

def getNotablePeople(city):
	query = "notable people in " + city

	if query not in cache:
		data = client.query(query)

		try:
			people = (next(data.result).text)
		except:
			getNotablePeople(city)

		## NULL
		if people == "":
			return "NONE"

		people = people.split('\n')

		names = [] ## has all the goodies to search

		for person in people:
			person = person.split("  ")
			if len(person)!=2:
				continue
			name,date = person
			names.append(name)

		cache[query] = names

	rand = int((len(cache[query])-1) * random.random())

	return cache[query][rand]

## EXECUTION
if __name__=="__main__":
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


