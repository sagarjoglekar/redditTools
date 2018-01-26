import json
import csv
import re


def getUnames(tweet):
    regex = r"\B@([^\W]+)"
    matches = re.finditer(regex, tweet)
    unames = ''
    for matchNum, match in enumerate(matches):
        unames = unames + "|" + tweet[match.start()+1:match.end()]
    return unames


with open("westMin.replies",'rb') as f:
    replies = f.readlines()

with open("westMin.tweets",'rb') as f:
    tweets = f.readlines()

tweetMap = dict()
for t in tweets:
    comps = t.strip().split('|||')
    tweetMap[comps[0]] = dict()
    tweetMap[comps[0]]['uid'] = comps[2]
    tweetMap[comps[0]]['uname'] = comps[4]
    tweetMap[comps[0]]['likes'] = comps[7]
    tweetMap[comps[0]]['retweet'] = comps[6]
    tweetMap[comps[0]]['content'] = comps[1]
    tweetMap[comps[0]]['time'] = comps[5]




edgeMap = []
for i in range(len(replies)):
    comps = replies[i].strip().split('|||')
    edge = dict()
    if comps[-1] == 'null':
        edge['dest']=''
        edge['parent'] = ''
        edge['src']=replies[i+1].strip().split('|||')[-1]
        edge['content']=comps[0]
        edge['likes'] = tweetMap[edge['src']]['likes']
        edge['retweet'] = tweetMap[edge['src']]['retweet']
        edge['uid'] = tweetMap[edge['src']]['uid']
        edge['uname'] = tweetMap[edge['src']]['uname']
        edge['time'] = tweetMap[edge['src']]['time']
        edge['dstUnames'] = getUnames(comps[0])
    else:
        edge['dest']=comps[-2]
        edge['parent'] = comps[-1]
        edge['src']=comps[0]
        edge['content']=comps[1]
        edge['likes'] = comps[7]
        edge['retweet'] = comps[6]
        edge['uid'] = comps[2]
        edge['uname'] = comps[4]
        edge['time'] = comps[5]
        edge['dstUnames'] = getUnames(comps[1])

        tweetMap[comps[0]] = dict()
        tweetMap[comps[0]]['uid'] = comps[2]
        tweetMap[comps[0]]['uname'] = comps[4]
        tweetMap[comps[0]]['likes'] = comps[7]
        tweetMap[comps[0]]['retweet'] = comps[6]
        tweetMap[comps[0]]['content'] = comps[1]
        tweetMap[comps[0]]['time'] = comps[5]

    edgeMap.append(edge)




# with open('tweetMap.json', 'w') as fp:
#     json.dump(tweetMap, fp)



# with open('edges.csv','wb') as f:
#     line = "src" + ',' + "dest" + "," + "parent" + ',' + "uid" + ',' + "likes" + ',' + "retweet" + ',' + "content" + ',' + "\n"
#     f.write(line)
#     for e in edgeMap:
#         line = e['src'] + "," + e['dest'] + ',' + e['parent'] + ',' + e['uid'] + ',' + e['likes'] + ',' + e['retweet'] + ',' + e['content'] + "\n"
#         f.write(line)




with open('edges.csv', 'w') as csvfile:
    fieldnames = ['src' , 'dest'  , 'parent', 'uid' , 'uname' , 'destunames', 'likes' , 'retweet' , 'content' ,'timestamp' ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for e in edgeMap:
        writer.writerow({'src': e['src'], 'dest': e['dest'], 'parent' : e['parent'] , 'uid': e['uid'], 'uname':e['uname'] , 'destunames': e['dstUnames'] , 'likes': e['likes'] , 'retweet': e['retweet'] , 'content':e['content'] , 'timestamp':e['time'] })
