import pandas as pd
import datetime as dt
from news import get_news
from tweets import get_tweets
from prices import get_prices
from model import predict_price

def predict(stock):
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

	tweets = get_tweets(stock) # get a dict of {time: score}
	news = get_news(stock) #'' ''
	prices = get_prices(stock) # get stock prices from last 50 days from yahoo! finance

	df = compile_data(prices, news, tweets) # mash the data together in a df

	return predict_price(df)


print(predict(""))
