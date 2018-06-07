from RedditConfig import Parser
import praw 
import datetime
from time import mktime
import logging



if __name__ == '__main__':
	Reddit_config = Parser("S4ge.config")

	# Reddit_config.printAll()

	reddit = praw.Reddit(client_id=Reddit_config.getId(),
                     client_secret=Reddit_config.getSecret(),
                     password=Reddit_config.getPassword(),
                     user_agent='testscript by /u/S4ge',
                     username=Reddit_config.getUsername())
	print reddit.user
	print(reddit.user.me())


	sub = reddit.subreddit("askscience")

	# This loops through search results and writes them in the open HTML file
	for submission in sub.top('year',limit=None):
	    print submission.url