from redditGraphTools import *
import json
import os


if __name__ == "__main__":
	subredditDir =  "/datasets_1/sagarj/IoPPN_collab/reddit_TheDonald/TheDonaldSub_more/"
	graphDir = "/datasets_1/sagarj/IoPPN_collab/reddit_TheDonald/theDonald_graph/"
	URL = "https://www.reddit.com"
	
	pageFiles = os.listdir(subredditDir)
	nxGraphDict = {}
	

	for file in pageFiles:
		
		with open(subredditDir+file,'rb') as f:
			posts = json.load(f)
		
		postList = posts['data']['children']
		for thread in postList:
			tId = thread['data']['id']
			perma = thread['data']['permalink']
			tUrl = URL + perma +".json" 
			jsDict = getThread(tUrl,tId,graphDir)
			print "Saving %s at %s"%(tId,graphDir)

	        graph = parseRedditJsonConvTree(jsDict)
	        nxGraphDict[tId] = graph

	print "Created %d Graphs"%(len(nxGraphDict.keys()))

	finalFile = graphDir + "TheDonald_TopPosts_replygraphs.pkl"
	with open(finalFile,'wb') as f:
		pkl.dump(nxGraphDict,f,protocol=pkl.HIGHEST_PROTOCOL)

	print "Done Saving !!!"