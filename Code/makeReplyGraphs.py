
import networkx as nx
import json
import os 
import pickle as pkl
import requests as rq 
from redditGraphTools import *

threadDir = "/datasets_1/sagarj/IoPPN_collab/reddit_suicideWatch/SW_morethan10_threads/"
graphDir = "/datasets_1/sagarj/IoPPN_collab/reddit_suicideWatch/SW_morethan10_graphs_complete_revised/"
#uncomment this to run test mode
# __name__ = "Test"



if __name__ == "__main__":
    print "main mode"
    conversations = os.listdir(threadDir)
    print "Converting %d Threads to Reply Graphs "%(len(conversations))
    nxGraphDict = {}

    for thread in conversations:
        path = threadDir + thread
        tId = thread.split('.')[0]
        jsDict = json.load(open(path,'rb'))
        print path
        # print jsDict
        graph = parseRedditJsonConvTree(jsDict)
        # nx.write_gexf(graph, graphDir + str(tId) + ".gexf")
        nxGraphDict[tId] = graph

    print "Created %d Graphs"%(len(nxGraphDict.keys()))

    finalFile = graphDir + "SW_morethan10_deeper_replygraphs_v2.pkl"
    with open(finalFile,'wb') as f:
        pkl.dump(nxGraphDict,f,protocol=pkl.HIGHEST_PROTOCOL)

    print "Done Saving !!!"




else:
    test_graph= threadDir + "fp8lm.json"
    print "Running testmode"
    print "working with : " + test_graph

    jsDict = json.load(open(test_graph,'rb'))

    graph = parseRedditJsonConvTree(jsDict)

    print graph.nodes()
    print graph.edges()
    print nx.get_node_attributes(graph,'text')

