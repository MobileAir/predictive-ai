import tweepy
import re
from tweepy import OAuthHandler
from textblob import TextBlob
import pandas as pd
import json
import datetime as dt


def getQuery(stock):
	'''Returns the stock company name based on the ticker'''

	# reads the company names
	with open("../data/names.txt", 'r') as f:
		names = json.load(f)
	f.close()

	# Google has a really weird name no one uses, so I just avoided it...
	if names[stock]=="GOOG":
		return "Google stock"

	return re.sub("Corp*|Inc*|Group|Co", "", names[stock])

def getPolarity(content):
	'''Turn the tweet into a TextBlob Object
	and then returns the polarity metric from TextBlob'''

	content = re.sub(r'\W|https',' ', str(content))
	analysis = TextBlob(content)
	polarity = analysis.sentiment.polarity

	return polarity


def getTweets(stock, query, df):
	tweets = {}
	# Want the moost recent tweets
	max_tweets = 10

	# Search the Twitter database for mentions of the Company's stock
	try: searched_tweets = [status for status in tweepy.Cursor(api.search, q=query+' stock', lang='en').items(max_tweets)]

		for tweet in searched_tweets:

			polarity = getPolarity(tweet.text)
			
			if polarity != 0:

				tweet_date = dt.date(tweet.created_at.year, tweet.created_at.month, tweet.created_at.day)

				# append to dictionary
				tweets[tweet_date] = polarity

				# update the dataframe for the day of the tweet, based on the score.
				return tweets
		return 0

	# Error handling for when I run out of allowed tweets/hour
	except tweepy.error.TweepError:
		return 1

# list of Stock tickers you want data for
ticks = ['YUM', 'ZBH', 'ZION', 'ZTS']

api = get_api()

for stock in ticks:
	query = getQuery(stock)
	df = pd.read_csv("noTweets/"+stock+".csv", index_col='Date')
	
	code = getTweets(stock, query, df)

	if code == 1:
		print("Twitter sweep completed up to (but not including) {}".format(stock))
		break

