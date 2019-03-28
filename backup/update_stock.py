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

def getTwitterApi():
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

def getTweetQuery(stock):
	'''Returns the stock company name based on the ticker'''

	# reads the company names
	with open("../data/names.txt", 'r') as f:
		names = json.load(f)
	f.close()

	# Google has a really weird name no one uses, so I just avoided it...
	if names[stock]=="GOOG":
		return "Google"

	return re.sub("Corp*|Inc*|Group|Co", "", names[stock])


def analyze(text):
	'''returns the polarity score for a chunk of text.'''
	text = re.sub(r'\W|https',' ',str(text))
	text = TextBlob(text)

	return text.sentiment.polarity

def stockUpdate(stock):
	'''This fctn. gets the values of the stock since the last time its csv file was updated.'''

	# load the stock data, find the date range to search for
	df = pd.read_csv("../data/bigdata/"+stock+".csv")
	since = df["Date"].max()
	try:
		since = dt.datetime.strptime(since, '%Y-%m-%d').date()
	except ValueError:
		since = dt.datetime.strptime(since[:-9], '%Y-%m-%d').date()
	today = dt.date.today()

	# get price updates from yahoo, then format
	updates = dr.get_data_yahoo(stock, since, today)
	updates['NewsData'] = 0
	updates['TweetScore'] = 0
	updates.reset_index(inplace=True)

	return updates


def newsUpdate(stock):
	'''Returns a dictionary of articles with their date and polarity'''
	articles = {}

	# load the news articles
	with open("../data/yahNews/"+stock+".txt", encoding='utf-8') as f:
		json_dict = json.load(f)

	# iterate through each article
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
		# add the results to the row with the corresponding date
		#for row in df.iterrows():

			#df_date = row[1].Date.date()

			#if df_date == publish_date:
				#df['NewsData'][df['Date']==row[1].Date] = score

def twitterUpdate(stock):
	'''Returns a dictionary of tweet scores and polarity '''
	api = getTwitterApi()
	query = getTweetQuery(stock)
	max_tweets = 50

	tweets = {}

	# Search the Twitter database for mentions of the Company's stock
	try: 
		searched_tweets = [status for status in tweepy.Cursor(api.search, q=query+' stock', lang='en').items(max_tweets)]

	except tweepy.error.TweepError:

		print("Tweepy Error starting at {}".format(stock))
		return None

	for tweet in searched_tweets:
			polarity = analyze(tweet.text)

			if polarity != 0:

				tweet_date = dt.date(tweet.created_at.year, tweet.created_at.month, tweet.created_at.day)

				tweets[tweet_date] = polarity
	return tweets




def appendBigData(stock, df, articles, tweets):
	''' The last step will be to update the data
	'''
	# Append the values to their corresponing rows in the df that will be appended to the large one
	for row in df.iterrows():
		df_date = row[1].Date.date()

		for date, score in articles.items():
			if df_date == date:
				df['NewsData'][df['Date']==row[1].Date] = score
		if tweets != None:
			for date, score in tweets.items():
				if df_date == date:
					df['TweetScore'][df['Date']==row[1].Date] = score

	big_df = pd.read_csv("../data/bigdata/"+stock+".csv")

	combined = pd.concat([big_df, df], sort=True)

	combined = combined.drop(["Unnamed: 0"], axis=1)

	combined.to_csv("../data/"+stock+".csv")

#reading date from cmd line
stock = sys.argv[1]

df = stockUpdate(stock)
articles = newsUpdate(stock)
tweets = twitterUpdate(stock)

appendBigData(stock, df, articles, tweets)

'''
ticks = ['MMM', 'ABT', 'ABBV', 'ACN', 'ATVI', 'AYI', 'ADBE', 'AAP', 'AES', 'AET', 'AMG', 'AFL', 'A', 'APD', 'AKAM', 'ALK', 'ALB', 'ALXN', 'ALLE', 'AGN', 'ADS', 'LNT', 'ALL', 'GOOGL', 'GOOG', 'MO', 'AMZN', 'AEE', 'AAL', 'AEP', 'AXP', 'AIG', 'AMT', 'AWK', 'AMP', 'ABC', 'AME', 'AMGN', 'APH', 'APC', 'ADI', 'ANTM', 'AON', 'APA', 'AIV', 'AAPL', 'AMAT', 'ADM', 'ARNC', 'AJG', 'AIZ', 'T', 'ADSK', 'ADP', 'AN', 'AZO', 'AVB', 'AVY', 'BHI', 'BLL', 'BAC', 'BCR', 'BAX', 'BBT', 'BDX', 'BBBY', 'BRK.B', 'BBY', 'BIIB', 'BLK', 'HRB', 'BA', 'BWA', 'BXP', 'BSX', 'BMY', 'AVGO', 'BF.B', 'CHRW', 'CA', 'COG', 'CPB', 'COF', 'CAH', 'KMX', 'CCL', 'CAT', 'CBG', 'CBS', 'CELG', 'CNC', 'CNP', 'CTL', 'CERN', 'CF', 'SCHW', 'CHTR', 'CHK', 'CVX', 'CMG', 'CB', 'CHD', 'CI', 'XEC', 'CINF', 'CTAS', 'CSCO', 'C', 'CFG', 'CTXS', 'CME', 'CMS', 'COH', 'KO', 'CTSH', 'CL', 'CMCSA', 'CMA', 'CAG', 'CXO', 'COP', 'ED', 'STZ', 'GLW', 'COST', 'COTY', 'CCI', 'CSRA', 'CSX', 'CMI', 'CVS', 'DHI', 'DHR', 'DRI', 'DVA', 'DE', 'DLPH', 'DAL', 'XRAY', 'DVN', 'DLR', 'DFS', 'DISCA', 'DISCK', 'DG', 'DLTR', 'D', 'DOV', 'DOW', 'DPS', 'DTE', 'DD', 'DUK', 'DNB', 'ETFC', 'EMN', 'ETN', 'EBAY', 'ECL', 'EIX', 'EW', 'EA', 'EMR', 'ENDP', 'ETR', 'EVHC', 'EOG', 'EQT', 'EFX', 'EQIX', 'EQR', 'ESS', 'EL', 'ES', 'EXC', 'EXPE', 'EXPD', 'ESRX', 'EXR', 'XOM', 'FFIV', 'FB', 'FAST', 'FRT', 'FDX', 'FIS', 'FITB', 'FSLR', 'FE', 'FISV', 'FLIR', 'FLS', 'FLR', 'FMC', 'FTI', 'FL', 'F', 'FTV', 'FBHS', 'BEN', 'FCX', 'FTR', 'GPS', 'GRMN', 'GD', 'GE', 'GGP', 'GIS', 'GM', 'GPC', 'GILD', 'GPN', 'GS', 'GT', 'GWW', 'HAL', 'HBI', 'HOG', 'HAR', 'HRS', 'HIG', 'HAS', 'HCA', 'HCP', 'HP', 'HSIC', 'HES', 'HPE', 'HOLX', 'HD', 'HON', 'HRL', 'HST', 'HPQ', 'HUM', 'HBAN', 'IDXX', 'ITW', 'ILMN', 'IR', 'INTC', 'ICE', 'IBM', 'IP', 'IPG', 'IFF', 'INTU', 'ISRG', 'IVZ', 'IRM', 'JBHT', 'JEC', 'SJM', 'JNJ', 'JCI', 'JPM', 'JNPR', 'KSU', 'K', 'KEY', 'KMB', 'KIM', 'KMI', 'KLAC', 'KSS', 'KHC', 'KR', 'LB', 'LLL', 'LH', 'LRCX', 'LEG', 'LEN', 'LUK', 'LVLT', 'LLY', 'LNC', 'LLTC', 'LKQ', 'LMT', 'L', 'LOW', 'LYB', 'MTB', 'MAC', 'M', 'MNK', 'MRO', 'MPC', 'MAR', 'MMC', 'MLM', 'MAS', 'MA', 'MAT', 'MKC', 'MCD', 'MCK', 'MJN', 'MDT', 'MRK', 'MET', 'MTD', 'KORS', 'MCHP', 'MU', 'MSFT', 'MAA', 'MHK', 'TAP', 'MDLZ', 'MON', 'MNST', 'MCO', 'MS', 'MSI', 'MUR', 'MYL', 'NDAQ', 'NOV', 'NAVI', 'NTAP', 'NFLX', 'NWL', 'NFX', 'NEM', 'NWSA', 'NWS', 'NEE', 'NLSN', 'NKE', 'NI', 'NBL', 'JWN', 'NSC', 'NTRS', 'NOC', 'NRG', 'NUE', 'NVDA', 'ORLY', 'OXY', 'OMC', 'OKE', 'ORCL', 'PCAR', 'PH', 'PDCO', 'PAYX', 'PYPL', 'PNR', 'PBCT', 'PEP', 'PKI', 'PRGO', 'PFE', 'PCG', 'PM', 'PSX', 'PNW', 'PXD', 'PBI', 'PNC', 'RL', 'PPG', 'PPL', 'PX', 'PCLN', 'PFG', 'PG', 'PGR', 'PLD', 'PRU', 'PEG', 'PSA', 'PHM', 'PVH', 'QRVO', 'QCOM', 'PWR', 'DGX', 'RRC', 'RTN', 'O', 'RHT', 'REGN', 'RF', 'RSG', 'RAI', 'RHI', 'ROK', 'COL', 'ROP', 'ROST', 'RCL', 'R', 'SPGI', 'CRM', 'SCG', 'SLB', 'SNI', 'STX', 'SEE', 'SRE', 'SHW', 'SIG', 'SPG', 'SWKS', 'SLG', 'SNA', 'SO', 'LUV', 'SWN', 'SE', 'SWK', 'SPLS', 'SBUX', 'STT', 'SRCL', 'SYK', 'STI', 'SYMC', 'SYF', 'SYY', 'TROW', 'TGT', 'TEL', 'TGNA', 'TDC', 'TSO', 'TXN', 'TXT', 'BK', 'CLX', 'COO', 'HSY', 'MOS', 'TRV', 'DIS', 'TMO', 'TIF', 'TWX', 'TJX', 'TMK', 'TSS', 'TSCO', 'TDG', 'RIG', 'TRIP', 'FOXA', 'FOX', 'TSN', 'USB', 'UDR', 'ULTA', 'UA', 'UAA', 'UNP', 'UAL', 'UNH', 'UPS', 'URI', 'UTX', 'UHS', 'UNM', 'URBN', 'VFC', 'VLO', 'VAR', 'VTR', 'VRSN', 'VRSK', 'VZ', 'VRTX', 'VIAB', 'V', 'VNO', 'VMC', 'WMT', 'WBA', 'WM', 'WAT', 'WEC', 'WFC', 'HCN', 'WDC', 'WU', 'WRK', 'WY', 'WHR', 'WFM', 'WMB', 'WLTW', 'WYN', 'WYNN', 'XEL', 'XRX', 'XLNX', 'XL', 'XYL', 'YHOO', 'YUM', 'ZBH', 'ZION', 'ZTS']
for stock in ticks:
	df = loadStock(stock)
	getArticles(stock,df)

	df.to_csv("../data/noTweets/"+stock+".csv")'''

