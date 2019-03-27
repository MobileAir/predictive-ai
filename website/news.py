import subprocess
import sys
import re
import json
import pandas as pd
import datetime as dt
import tweepy
from tweepy import OAuthHandler
import pandas_datareader as dr
from textblob import TextBlob
import fix_yahoo_finance as fix
fix.pdr_override()

def get_news(stock):
	
	def analyze(text):
		'''returns the polarity score for a chunk of text.'''
		text = re.sub(r'\W|https',' ',str(text))
		text = TextBlob(text)

		return text.sentiment.polarity

	def newsUpdate(stock,f):
		'''Returns a dictionary of articles with their date and polarity'''
		articles = {}

		# load the news articles
		json_dict = json.loads(f)

		# get the score and link for each article
		for article in json_dict['result']:

			publish_date = dt.date.fromtimestamp(article['published_at'])

			# get the content from the article
			content = ''
			for k,v in article.items():
				if k == 'title':
					content += v
				if k == 'summary':
					content += v
				if f == 'content':
					content += v

			# now each article gets a score based on its content
			score = analyze(content)
			articles[publish_date] = score

		return articles

	# get info from ruby file
	file = subprocess.check_output(['ruby', 'src/news.rb', stock])

	articles = newsUpdate(stock, file)

	return articles

def get_summary():

	markets = {}
	# get info from ruby file
	file = subprocess.check_output(['ruby', 'src/market_sum.rb'])

	market_json = json.loads(file)
	for market in (market_json["result"]):
		try:
			if (market['shortName']=='S&P 500') or (market['shortName']=='Dow 30') or (market['shortName']=='Nasdaq'):
				markets[market['shortName']] = [market['regularMarketChange']['fmt'], market['regularMarketChangePercent']['fmt']]
		except KeyError:
			continue

	return markets
