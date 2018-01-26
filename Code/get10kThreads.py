import pandas as pd
from redditThreadCrawl import getThread
from time import sleep

downloadDir = "/datasets_1/sagarj/IoPPN_collab/reddit_suicideWatch/SW_AllThreads/"

dataFrame = "/datasets_1/sagarj/IoPPN_collab/reddit_suicideWatch/filteredSuicideWatch_All_valid.pkl"

sleepTime = 0.2


if __name__ == "__main__":

	data = pd.read_pickle(open(dataFrame,'rb'))

	for index, row in data.iterrows():
		tId = row['id']
		perma = row['permalink']
		url = "http://www.reddit.com"+perma+".json"

		print "Crawling: " + url
		try:
			getThread(url, tId , downloadDir)
			sleep(sleepTime)
		except:
			print "something went wrong while crawling"
			continue

