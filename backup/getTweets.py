import tweepy
import re
from tweepy import OAuthHandler
from textblob import TextBlob
import pandas as pd
import json
import datetime as dt


def get_api():
	'''returns access to twitter api '''

	# get your own damn keys!
    with open("../../keys.txt", "r") as f:
        keys = f.readlines()
        consumer_key = keys[0].strip()
        consumer_secret = keys[1].strip()
        access_token = keys[2].strip()
        access_secret = keys[3].strip()
    f.close()

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)

	return tweepy.API(auth)


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

	# Want the moost recent tweets
	max_tweets = 4

	# Search the Twitter database for mentions of the Company's stock
	try: searched_tweets = [status for status in tweepy.Cursor(api.search, q=query+' stock', lang='en').items(max_tweets)]

		for tweet in searched_tweets:

			polarity = getPolarity(tweet.text)
	
			if polarity != 0:
				# get the data into a nice format
				tweet_date = dt.date(tweet.created_at.year, tweet.created_at.month, tweet.created_at.day)

				# update the dataframe for the day of the tweet, based on the score.
				df.set_value(str(tweet_date), ['TweetScore'], polarity)

		clean = df.dropna(axis=0)
		clean = clean.drop(["Unnamed: 0"], axis=1)

		# Update the big data table
		clean.to_csv("bigdata/"+stock+".csv")

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

