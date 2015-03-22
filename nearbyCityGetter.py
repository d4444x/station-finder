import requests

def getNearbyCities(longNorth, lattEast, mileRadius, appID):
    queryString = 'http://api.wolframalpha.com/v2/query?appid=' + appID + '&input=cities%20within%20' + str(mileRadius) + '%20miles%20of%20' + str(longNorth) + '%C2%B0North%20' + str(lattEast) + '%C2%B0East&format=plaintext&podstate=Result__More&podstate=Result__More&podstate=Result__More&podstate=Result__More&includepodid=Result'
    r = requests.get(queryString)
    
    ellipsis = r.text.find('\n(vertical ellipsis)')
    if ellipsis == -1:
        toParse = r.text[11 + r.text.find('<plaintext>'):r.text.find('</plaintext>')]
    else:
        toParse = r.text[11 + r.text.find('<plaintext>'):ellipsis]

    parsing = toParse.encode('ascii', 'ignore').splitlines()
    length = len(parsing)
    nearbyStates = []
    for i in range(length):
        parsing[length - i - 1], newState = parseLine(parsing[length - i - 1], nearbyStates)
        if newState != '' and newState not in nearbyStates:
            nearbyStates.append(newState)

    return parsing
    

def parseLine(line, possibleStates):
    beginParen = line.find('(')
    firstComma = line.find(',')
    if firstComma == -1:
        return (line[:beginParen - 1], possibleStates, line[beginParen:]), ''
    else:
        secondComma = line.find(',', firstComma + 1)
        return (line[:firstComma], [line[firstComma + 2:secondComma]], line[beginParen:]), line[firstComma + 2:secondComma]


if __name__ == "__main__":
    # good ole nashville, TN
    print getNearbyCities(37.84, -87.58, 52, 'Q9WERY-K3HTGTL99H')
