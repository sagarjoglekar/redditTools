import MakeGraphs
import multiprocessing as mp
import itertools

def split_dict(x, chunks):      
    i = itertools.cycle(range(chunks))       
    split = [dict() for _ in range(chunks)]
    for k, v in x.items():
        split[next(i)][k] = v
    return split 

def crawlLoop(postPermas):
    print('crawling %d threads in this process'%len(postPermas))
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
    return True



if __name__ == "__main__":
        parser = argparse.ArgumentParser(description='Instantiate crawler with a list of permalinks')
        parser.add_argument('-p', help='Pickle file for the permalinks')
        # parser.add_argument('-p', help='Number of parallel processes to spawn')
        args = parser.parse_args()

        print ("Creating graph from posts")
        postDict = args.i
        processes = 12 #args.p
        URL = "https://www.reddit.com"
        try:
                Permas = pkl.load(open(postDict,'rb'))
                alreadyCrawled = getCrawledData(graphDir)
                postPermas = getSubPostPermas(Permas , alreadyCrawled)
                print ("Crawling :" , len(postPermas))
        except:
                print("The Pickled file you sent does not exist or is corrupt",postDict)
                sys.exit()
        #Split permadict into p chunks
        chunked_dict = split_dict(postPermas , processes)

        #Instansiate a pool of processes
        pool = mp.Pool(processes)

        #Map each chunk onto one process
        results = pool.map(crawlLoop, chunked_dict)
        pool.close()