from redditCrawler import redditCrawler
import json
import os
import networkx as nx
import pickle as pkl
import random

#Main file to create replygraphs from sub or posts

__name__  = "__from__posts__"

def getPosts(Dir):
	if os.path.exists(Dir):
		files = os.listdir(Dir)
		posts = [f for f in files]
		return posts
	else:
		print "Invalid path to post files"
		return None

if __name__ == "__main__":
	subredditDir =  "/datasets_1/sagarj/IoPPN_collab/reddit_askScience/reddit_askScience_FP/"
	graphDir = "/datasets_1/sagarj/IoPPN_collab/reddit_askScience/reddit_askScience_Graphs/"
	URL = "https://www.reddit.com"
	
	pageFiles = os.listdir(subredditDir)
	nxGraphDict = {}
	for file in pageFiles:
		
		with open(subredditDir+file,'rb') as f:
			posts = json.load(f)
		
		postList = posts['data']['children']
		for thread in postList:
			crawler = redditCrawler(15,300)
			tId = thread['data']['id']
			print "Reading %s"%tId
			perma = thread['data']['permalink']
			tUrl = URL + perma +".json" 
			jsDict = {}
			jsDict = crawler.getThread(tUrl,tId,graphDir,True)
			if jsDict == None:
				continue
			print "Saving %s at %s"%(tId,graphDir)
			graph = crawler.parseRedditJsonConvTree(jsDict)
			print type(graph)
			print " Saving Graphs "
			nxGraphDict[tId] = graph
			print "Got %d Graphs now "%(len(nxGraphDict.keys()))
	        # tempGraphFile = graphDir + tId + ".gpickle"
	        # nx.write_gpickle(nxGraphDict[tId], tempGraphFile)
		print "Created %d Graphs"%(len(nxGraphDict.keys()))
		finalFile = graphDir + "AskScience_replygraphs.pkl"
		with open(finalFile,'wb') as f:
			pkl.dump(nxGraphDict,f,protocol=pkl.HIGHEST_PROTOCOL)
		print "Done Saving !!!"


#Crawl threads based on post json.

if __name__ == "__from__posts__":
	print "Creating graph from posts"
	URL = "https://www.reddit.com"

	postDir = "/datasets_1/sagarj/IoPPN_collab/FrontPage/posts/"
	graphDir = "/datasets_1/sagarj/IoPPN_collab/FrontPage/graphs/"
	graphFile = "frontPage_replygraphs_depth_fixed.pkl"

	nxGraphDict = {}
	allPosts = getPosts(postDir)
	posts = random.sample(allPosts,12000)

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