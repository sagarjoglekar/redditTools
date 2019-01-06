import json
import requests as rq 

def getThread(url):
	session_headers = {
	'Host': 'www.reddit.com',
	'Connection': 'keep-alive',
	'Cache-Control': 'max-age=0',
	'Upgrade-Insecure-Requests': '1',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	#'Referer': 'http://localhost:9000/notebooks/Reddit/Notebooks/SuicideWatchSubreddit.ipynb'
	'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'en-GB,en-US;q=0.8,en;q=0.6',
	'Cookie': "loid=00000000000gslzvdi.2.1507591930964.Z0FBQUFBQlozQWI3M243MTdFMUgzNWtQNzNVbzg5Z3NXYmxpLUdRTWVXdEpWQzBfbkxBSVNNVVF3dE1zQlN5cVMzeGtxZXlmT0JQY2JvTld2NWlVeGlGeFpkNnBYM2ZIYlNNR2xMWGFFS3hieDZpWEJ5OVlyTng0MUFZZjNYdjQ0ZURFNTFlSmlVRGw; edgebucket=T8nkTF0z7WPnNzlE8B; __gads=ID=ab9c1b0fcb7eaefc:T=1507591936:S=ALNI_Mao2tvEoyJzEDEuxxhfZBlOQHXlsA; eu_cookie_v2=3; _ga=GA1.2.1088810883.1507591931; __utma=55650728.1088810883.1507591931.1507912304.1507912553.14; __utmz=55650728.1507912553.14.11.utmcsr=reddit|utmccn=(not%20set)|utmcmd=hot|utmcct=comments; aa=1; _recentclicks2=t3_7cfzsx%2Ct3_7cfw08%2Ct3_7cdofu%2Ct3_7caog1%2Ct3_7cdvud; _recent_srs=t5_2qpzs%2Ct5_2qh1q%2Ct5_2qh49%2Ct5_2rtff%2Ct5_36buk%2Ct5_2r7yd%2Ct5_2rks3%2Ct5_3j2jr%2Ct5_2sumw%2Ct5_2xp2o; pc=r3; session_tracker=tPgx9U9yPt99jYRDqC.0.1510585492994.Z0FBQUFBQmFDYlNWcWZHclI5WWxDWW9kQ0dURk9FRU9BZjFJTURWZElzaldRbkROaEJUOWE1czRQUWxPUzUwOFFwY3R3ckI5VkNDUlhJc01NVEtEeHVWd25CdUpXWEI1X012RkJaS3cyNXdNbk5vOE9DSXp5ZlhuTzF3a2pxT2dLZ3laMDhtQlhib3k; initref=localhost"
	}

	client = rq.session()
	resp = client.get(url , headers=session_headers)
	if resp.status_code == 200:
		json_data = json.loads(resp.text)
		return json_data
	else:
		print "Failed to get page"
		return None

def writeJson(fileName , dictionary):
	print "Saving " + fileName
	with open(fileName,'wb') as f:
		json.dump(dictionary,f)

def getSubreddit(baseURL , baseString , destinationDirectry):
	start = 1
	firstURL = baseURL + ".json"
	firstJson = getThread(firstURL)

	nxt = firstJson['data']['after']
	firstFile = destinationDirectry + baseString + str(start) +".json"
	start+=1
	writeJson(firstFile,firstJson)
	
	while nxt != None:
		nextUrl = baseURL + ".json" + "?after=" + nxt
		nextJson = getThread(nextUrl)
		if nextJson == None:
			continue
		print "Saving page %d"%(start)
		nxt = nextJson['data']['after']
		nextFile = destinationDirectry + baseString + str(start) +".json"
		start+=1
		writeJson(nextFile,nextJson)

def getSubredditByCount(baseURL , baseString , destinationDirectry):
	start = 1
	firstURL = baseURL + ".json" + "?t=all"
	firstJson = getThread(firstURL)

	nxt = firstJson['data']['after']
	firstFile = destinationDirectry + baseString + str(start) +".json"
	start+=1
	count = 25
	writeJson(firstFile,firstJson)
	
	while nxt != None:
		nextUrl = baseURL + ".json" + "?t=all&count=" + str(count) + "&after=" + nxt
		print nextUrl
		nextJson = getThread(nextUrl)
		if nextJson == None:
			continue
		print "Saving page %d"%(start)
		nxt = nextJson['data']['after']
		nextFile = destinationDirectry + baseString + str(start) +".json"
		start+=1
		count+=25
		writeJson(nextFile,nextJson)

def getSearchByTimestamp(baseURL , baseString , destinationDirectry):
	start = 1
	firstURL = baseURL
	firstJson = getThread(firstURL)

	nxt = firstJson['data']['after']
	firstFile = destinationDirectry + baseString + str(start) +".json"
	start+=1
	writeJson(firstFile,firstJson)
	
	while nxt != None:
		nextUrl = baseURL + "&after=" + nxt
		print nextUrl
		nextJson = getThread(nextUrl)
		if nextJson == None:
			continue
		print "Saving page %d"%(start)
		nxt = nextJson['data']['after']
		nextFile = destinationDirectry + baseString + str(start) +".json"
		start+=1
		writeJson(nextFile,nextJson)

if __name__ == "__main__":

	SaveDir = "/datasets_1/sagarj/IoPPN_collab/reddit_depression/pages/"
	subredditUrl = "https://www.reddit.com/r/depression/"
	# searchUrL = "https://www.reddit.com/r/thedonald/search.json?sort=new&q=timestamp%3A1354716928..1512483328&restrict_sr=on&syntax=cloudsearch&limit=100"
	# getSubreddit(subredditUrl , "TheDonald_", SaveDir)
	getSubredditByCount(subredditUrl , "depression_", SaveDir)
	# getSearchByTimestamp(searchUrL , "TheDonald_", SaveDir)


