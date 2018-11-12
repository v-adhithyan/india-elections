import tweepy
from Tkinter import *
from time import sleep
from datetime import datetime
#
consumer_key = '9nmKIsynEPIALH9EDEC1m9isI'
consumer_secret = 'yI9SH0I1ynbsh4ZYMhdpWryJoDKdMpjcz5rw6pyVCfqle9STxC'
access_token = '2909118727-BSCAqzZSHGinmgyjiIVipKCSUYuSamxxkZlzAPs'
access_token_secret = 'bbh9oTakHVEW5P2xW9ZIGOGPmuUiqQO8y2skxBzldnHVC'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
csvFile = open('p1.csv', 'a')
import csv
csvWriter = csv.writer(csvFile)
for tweet in tweepy.Cursor(api.search,q="#NDA",count=100,
                           lang="en",
                           since="2017-04-03").items():
    print (tweet.created_at, tweet.text)
    csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])
