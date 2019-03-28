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
		links = {}

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

			# now get the links with {title:url}
			links[article['title']] = article['link']

		return articles, links

	file = subprocess.check_output(['ruby', 'news.rb', stock])

	articles, links = newsUpdate(stock, file)

	return articles, links


