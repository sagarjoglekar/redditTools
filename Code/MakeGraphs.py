from redditCrawler import redditCrawler
import json
import os
import networkx as nx
import pickle as pkl
import random
import bz2
import requests as rq
import time
import glob
import argparse
import sys


dumpPath = '/10TBdrive/datashare/geo_located_Reddit_crawl/yearlySubmissions/'
graphDir = '/10TBdrive/datashare/geo_located_Reddit_crawl/graphs/'
postDir = '/10TBdrive/datashare/geo_located_Reddit_crawl/posts/'
graphFile = "January2017_atleast10comments.pkl"



__name__ = '__curated__'

def getSubmissionPermalinks(filePath , comments_Thresh = 20 , limit=None):
    import json
    import bz2
    import lzma
    
    ext = filePath.split('.')[-1]
    openedDump = None
    if ext == 'bz2':
        openedDump = bz2.BZ2File(filePath, "r")
    elif ext == 'xz':
        openedDump = lzma.open(dump)
    else:
        print ("Invalid file type")
    count = 0
    returnData = dict()
    print("=============Parsing============")
    st = time.time()
    
    for line in openedDump:
        lineData = json.loads(line.strip())
        if lineData['num_comments'] > comments_Thresh:
            if (limit!=None and count > limit):
                return returnData
            try:
                returnData[lineData['id']] = lineData['permalink']
            except:
                print("Permalink not found, moving on!")
        if count%100000 == 0:
            end = time.time()
            print("Done parsing %d posts in %d seconds",(count,(end-st)))
            st = time.time()
        count+=1
    return returnData


def getPostDumps(path):
        paths = glob.glob(path+'/*.bz2')
        paths += glob.glob(path+'/*.xz')
        return paths

def getCrawledData(path):
    files = glob.glob(path + "*.pkl")
    threads = [f.split('/')[-1].split('.')[0] for f in files]
    return threads

def getSubPostPermas(permaDict , crawledList):
    subDict = dict()
    crawled = set(crawledList).intersection(permaDict.keys())
    print("Already got ", len(crawled) , len(permaDict))
    subset = list(set(permaDict.keys()).symmetric_difference(crawled))

    for k in subset:
        subDict[k] = permaDict[k]
    return subDict

if __name__ == "__main__":
        print ("Creating graph from posts")
        URL = "https://www.reddit.com"
        dumpFiles = getPostDumps(dumpPath)
        print(dumpFiles)
        postPermas = getSubmissionPermalinks(dumpFiles[0],comments_Thresh= 10)

        for p in postPermas:
                url = URL  + postPermas[p] + ".json"
                crawler = redditCrawler(50,300)
                print("Getting thread from",url)
                jsDict = crawler.getThread(url , p , postDir , save = True )
                print(jsDict)
                tId = p
                if jsDict == None:
                        continue
                print ("Saving %s at %s",(tId,graphDir))
                graph = crawler.parseRedditJsonConvTree(jsDict)
                print(type(graph))
                print(" Saving Graphs ")
                # nxGraphDict[tId] = graph
                graphPath = graphDir + str(tId) + '.pkl'
                with open(graphPath,'wb') as fi:
                        pkl.dump(graph,fi,protocol=pkl.HIGHEST_PROTOCOL)
        print ("Done Saving !!!")
        

if __name__ == "__curated__":
        parser = argparse.ArgumentParser(description='Instantiate crawler with a list of permalinks')
        parser.add_argument('-p', help='Pickle file for the permalinks')
        args = parser.parse_args()

        print ("Creating graph from posts")
        postDict = args.p
        URL = "https://www.reddit.com"
        try:
                Permas = pkl.load(open(postDict,'rb'))
                alreadyCrawled = getCrawledData(graphDir)
                postPermas = getSubPostPermas(Permas , alreadyCrawled)
                print ("Crawling :" , len(postPermas))
        except:
                print("The Pickled file you sent does not exist or is corrupt",postDict)
                sys.exit()
        
        for p in postPermas:
                try:
                    url = URL  + postPermas[p] + ".json"
                    crawler = redditCrawler(50,300)
                    print("Getting thread from",url)
                    jsDict = crawler.getThread(url , p , postDir , save = True )
                    print(jsDict)
                    tId = p
                    if jsDict == None:
                            continue
                    print ("Saving %s at %s",(tId,graphDir))
                    graph = crawler.parseRedditJsonConvTree(jsDict)
                    print(type(graph))
                    print(" Saving Graphs ")
                    graphPath = graphDir + str(tId) + '.pkl'
                    with open(graphPath,'wb') as fi:
                            pkl.dump(graph,fi,protocol=pkl.HIGHEST_PROTOCOL)
                except:
                    print("SomeThing went horribly wrong since you have an exception HERE!!")
        
        print ("Done Saving !!!")


if __name__ == '__test__':
    parser = argparse.ArgumentParser(description='Instantiate crawler with a list of permalinks')
    parser.add_argument('-p', help='Pickle file for the permalinks')
    args = parser.parse_args()

    print ("Creating graph from posts")
    postDict = args.p
    Permas = pkl.load(open(postDict,'rb'))
    alreadyCrawled = getCrawledData(graphDir)
    print(len(alreadyCrawled))
    postPermas = getSubPostPermas(Permas , alreadyCrawled)
    print ("Crawling :" , len(postPermas))