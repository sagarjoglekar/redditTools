from redditGraphTools import *
import json
import os
import networkx as nx

if __name__ == "__main__":
	subredditDir =  "/datasets_1/sagarj/IoPPN_collab/reddit_CMV/CMV_sub/"
	graphDir = "/datasets_1/sagarj/IoPPN_collab/reddit_CMV/CMV_graph/"
	URL = "https://www.reddit.com"
	
	pageFiles = os.listdir(subredditDir)
	nxGraphDict = {}
	for file in pageFiles:
		
		with open(subredditDir+file,'rb') as f:
			posts = json.load(f)
		
		postList = posts['data']['children']
		for thread in postList:
			tId = thread['data']['id']
			print "Reading %s"%tId
			perma = thread['data']['permalink']
			tUrl = URL + perma +".json" 
			jsDict = {}
			jsDict = getThread(tUrl,tId,graphDir)
			if jsDict == None:
				continue
			print "Saving %s at %s"%(tId,graphDir)
			graph = parseRedditJsonConvTree(jsDict)
			print type(graph)
			print " Saving Graphs "
			nxGraphDict[tId] = graph
			print "Got %d Graphs now "%(len(nxGraphDict.keys()))
	        tempGraphFile = graphDir + tId + ".gpickle"
	        nx.write_gpickle(nxGraphDict[tId], tempGraphFile)
	print "Created %d Graphs"%(len(nxGraphDict.keys()))
	finalFile = graphDir + "CMV_TopPosts_replygraphs.pkl"
	with open(finalFile,'wb') as f:
		pkl.dump(nxGraphDict,f,protocol=pkl.HIGHEST_PROTOCOL)
	print "Done Saving !!!"