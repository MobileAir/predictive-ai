import pandas as pd
import datetime as dt
import json
import pandas_datareader as dr
import fix_yahoo_finance as fix
fix.pdr_override()

def get_prices(stock):
	'''This fctn. gets the values of the stock'''

	# load the stock data, find the date range to search for
	today = dt.date.today()
	since = today - dt.timedelta(days=85)

	# get price updates from yahoo, then format

	prices = dr.get_data_yahoo(stock, since, today)

	prices = prices.tail(55) # CHANGE BACK TO 49
	prices['NewsData'] = 0
	prices['TweetScore'] = 0
	prices = prices.drop(['Volume', 'Adj Close'], axis=1)
	prices.reset_index(inplace=True)

	return prices

with open("../data/names1.txt") as f:
	names = json.load(f)
	for k,v in names.items():
		try:
			data = get_prices(k)
			data.to_csv("webData/"+k+".csv")
		except (dr._utils.RemoteDataError, KeyError) as e:
			print(v)
			continue