import tweepy
import re
from tweepy import OAuthHandler
from textblob import TextBlob
import pandas as pd
import json
import datetime as dt

def get_tweets(stock):

	def get_api():
		'''returns access to twitter api '''

		# get your own damn keys!
		with open("../keys.txt", "r") as f:
			keys = f.readlines()
			consumer_key = keys[0].strip()
			consumer_secret = keys[1].strip()
			access_token = keys[2].strip()
			access_secret = keys[3].strip()
		f.close()

		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_secret)

		return tweepy.API(auth)

	def get_query(stock):
		'''Returns the stock company name based on the ticker'''

		# reads the company names
		with open("data/names.txt", 'r') as f:
			names = json.load(f)
		f.close()

		# Google has a really weird name no one uses, so I just avoided it...
		if names[stock]=="GOOG":
			return "Google stock"

		return re.sub("Corp*|Inc*|Group|Co", "", names[stock])

	def get_polarity(content):
		'''Turn the tweet into a TextBlob Object
		and then returns the polarity metric from TextBlob'''

		content = re.sub(r'\W|https',' ', str(content))
		analysis = TextBlob(content)
		polarity = analysis.sentiment.polarity

		return polarity

	def twitter_update(stock):
		'''Returns a dictionary of tweet times and polarity '''
		api = get_api()
		query = get_query(stock)
		max_tweets = 50

		tweets = {}

		# Search the Twitter database for mentions of the Company's stock
		try: 
			searched_tweets = [status for status in tweepy.Cursor(api.search, q=query+' stock', lang='en').items(max_tweets)]

		except tweepy.error.TweepError:

			#print("Tweepy Error starting at {}".format(stock))
			return None

		for tweet in searched_tweets:
				polarity = get_polarity(tweet.text)

				if polarity != 0:

					tweet_date = dt.date(tweet.created_at.year, tweet.created_at.month, tweet.created_at.day)

					tweets[tweet_date] = polarity
		return tweets

	# returns a dictionary of tweet times and polarity for a given stock
	return twitter_update(stock)


