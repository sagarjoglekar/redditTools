import networkx as nx
import json
import os 
import pickle as pkl
import requests as rq 

import sys
#increase recursion limit, dangerous step, comment out if not sure about the computer's stack size
sys.setrecursionlimit(2000)

def getThread(url,threadId,dDir):
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
    print url
    client = rq.session()
    resp = client.get(url , headers=session_headers)
    if resp.status_code == 200:
        # with open(dDir+threadId+".json" , 'wb') as f:
        #     f.write(resp.content)
        json_data = json.loads(resp.text)
        return json_data

    else:
        print "Failed to get the thread"
        return None


def getSubThread(url):
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
        print "Failed to get the thread"
        return None

def getAffects(text):
    return {'a':1,'b':1,'c':1}

def sanitizeText(text):
    return text.encode('utf8').replace('\n', '').replace('\r', '')


def parseChildren(jsonDict , graph , permUrl , motherDepthOffset):
    if jsonDict['kind'] == 'more':
        print "Need Deeper Probing !!!!!! "
        deepterThreadId = jsonDict['data']['parent_id'].split('_')[1]
        print deepterThreadId
        offsetDepth = motherDepthOffset + jsonDict['data']['depth']+1
        print offsetDepth
        #Return if the recusion goes beyond 200 depth
        if offsetDepth > 200:
            return
        getUrl = permUrl +".json"
        print "Getting Nested Thread from : " + getUrl
        deeperDict = getSubThread(getUrl)
        if deeperDict != None:
            graph = parseRedditJsonConvTree(deeperDict,graph,offsetDepth)
            return
        else:
            print "Silently Returning"
            return
        
    data = jsonDict['data']
    affects = getAffects(sanitizeText(data['body']))
    # print data['name']
    propertyDict = {'author' : data['author'] , 'ups' : data['ups'] , 'downs' : data['downs'] , 'text' : sanitizeText(data['body']) , 'depth' : (motherDepthOffset + data['depth'])-1 , 'affects' : sum(affects.values()) }
    graph.add_node(data['name'] , propertyDict )
    graph.add_edge(data['name'], data['parent_id'] , weight=1 )
    if data['replies'] != '':
        permUrl = "http://www.reddit.com" + data['permalink']
        if len(data['replies']['data']['children']) > 0:
            for k in data['replies']['data']['children']:
                parseChildren(k, graph , permUrl , motherDepthOffset )
    else:
        return
    
def parseRedditJsonConvTree(jsonDict,motherGraph=None,DepthOffset=0):
    if motherGraph != None:
        replyGraph = motherGraph
        root = jsonDict[1]
        perma = root['data']['children'][0]['data']['permalink']
        url = "http://www.reddit.com"+perma
        print url

    else:
        root = jsonDict[0]
        perma = root['data']['children'][0]['data']['permalink']
        url = "http://www.reddit.com"+perma
        print url
        replyGraph = nx.DiGraph()
        data = root['data']['children'][0]['data']
        affects = getAffects(data['selftext'])
        propertyDict = {'author' : data['author'] , 'ups' : data['ups'] , 'downs' : data['downs'] , 'text' : sanitizeText(data['selftext']) , 'depth' : DepthOffset-1, 'affects' : sum(affects.values())}
        replyGraph.add_node(data['name'] , propertyDict )
    
    if len(jsonDict[1]['data']['children']) > 0:
        for k in jsonDict[1]['data']['children']:
            parseChildren(k , replyGraph , url , DepthOffset)
    return replyGraph