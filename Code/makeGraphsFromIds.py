from redditCrawler import redditCrawler
import json
import os
import networkx as nx
import pickle as pkl
import random

#Main file to create replygraphs from sub or posts

__name__  = "__main__"

def getPostids(Dir):
	if os.path.exists(Dir):
		files = os.listdir(Dir)
		posts = [f for f in files]
		return posts
	else:
		print "Invalid path to post files"
		return None



#Crawl threads based on post json.

if __name__ == "__main__":
    
	print "Creating graph from Ids"
    subredditFrag = "/r/changemyview/comments/"
	URL = "https://www.reddit.com"

	postDir = "/datasets_1/sagarj/IoPPN_collab/changeMyView/posts/"
	graphDir = "/datasets_1/sagarj/IoPPN_collab/changeMyView/graphs/"
	graphFile = "frontPage_replygraphs_50k.pkl"

	nxGraphDict = {}
	allPosts = getPosts(postDir)
	posts = random.sample(allPosts,50000)

	for p in posts:
		crawler = redditCrawler(50,300)
		postJson = json.load(open(postDir + p , 'rb'))
		perma = postJson['data']['permalink']
		tId = postJson['data']['id']
		print perma
		print tId
		tUrl = URL + perma +".json"
		jsDict = None
		jsDict = crawler.getThread(tUrl,tId,graphDir,True)
		if jsDict == None:
			continue
		print "Saving %s at %s"%(tId,graphDir)
		graph = crawler.parseRedditJsonConvTree(jsDict)
		print type(graph)
		print " Saving Graphs "
		nxGraphDict[tId] = graph
		print "Got %d Graphs now "%(len(nxGraphDict.keys()))

	print "Created %d Graphs"%(len(nxGraphDict.keys()))
	finalFile = graphDir + graphFile
	with open(finalFile,'wb') as f:
		pkl.dump(nxGraphDict,f,protocol=pkl.HIGHEST_PROTOCOL)
	print "Done Saving !!!"