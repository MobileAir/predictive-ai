import re
import json
import pandas as pd
import datetime as dt
from news import get_news, get_summary
from tweets import get_tweets
from prices import get_prices
from model import predict_price

class Predictor():

	def __init__(self):
		self.company=None
		self.ticker=None
		self.predictions=None
		self.articles = None
		self.high = None
		self.low = None
		self.close = None
		self.news_score = None
		self.tweet_score = None

	def predict(self, stock):

		def compile_data(df, articles, tweets):
			''' The last step will be to update the data'''
			# Append the values to their corresponing rows in the df
			for row in df.iterrows():
				df_date = row[1].Date.date()

				for date, score in articles.items():
					if df_date == date:
						df['NewsData'][df['Date']==row[1].Date] = score

				#if I have some tweets
				if tweets != None:
					for date, score in tweets.items():
						if df_date == date:
							df['TweetScore'][df['Date']==row[1].Date] = score

			df = df.drop(['Date'], axis=1)
			return df

		self.ticker = stock
		tweets = get_tweets(stock) # get a dict of {time: score}
		news = get_news(stock) #'' '', links contains news headlines and their urls
		prices = get_prices(stock) # get stock prices from last 50 days from yahoo! finance

		# Get polarity for website
		if tweets!=None:
			for k,v in tweets.items():
				if v!=0:
					self.tweet_score = "{:,.2f}".format(v);
					break
		if news!=None:
			for k,v in news.items():
				if v!=0:
					self.news_score = "{:,.2f}".format(v);
					break

			
		df = compile_data(prices, news, tweets) # mash the data together in a df
		preds = predict_price(df)
		print(preds)

		# make the numbers look nice
		self.high = "${:,.2f}".format(float(preds.tail(1).High.values))
		self.low = "${:,.2f}".format(float(preds.tail(1).Low.values))
		self.close = "${:,.2f}".format(float(preds.tail(1).Close.values))

p = Predictor()
p.predict("AON")
print(p.low)