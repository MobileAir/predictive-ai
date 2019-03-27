import pandas as pd
import datetime as dt
import pandas_datareader as dr
import fix_yahoo_finance as fix
fix.pdr_override()

def get_prices(stock):
	'''This fctn. gets the values of the stock'''

	# load the stock data, find the date range to search for
	today = dt.date.today()
	since = today - dt.timedelta(days=80)

	# get price updates from yahoo, then format
	prices = dr.get_data_yahoo(stock, since, today)
	prices = prices.tail(50)
	prices['NewsData'] = 0
	prices['TweetScore'] = 0
	prices = prices.drop(['Volume', 'Adj Close'], axis=1)
	prices.reset_index(inplace=True)

	return prices