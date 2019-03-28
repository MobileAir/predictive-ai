import pandas as pd
import datetime as dt
from getNews import get_news
from getTweets import get_tweets
from getStocks import get_prices

def compile(df, articles, tweets):
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

	return df

stock = "MSFT"
tweets = get_tweets(stock)
news = get_news(stock)

df = get_prices(stock)


print(df.columns)