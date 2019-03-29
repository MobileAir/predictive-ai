import re
import json
import subprocess
import pandas as pd
import datetime as dt
from news import get_news, get_summary
from market_news import b_in, bloom, fin_t

class Analyst:
	def __init__(self):
		self.ticker = None
		self.company = None
		self.nasdaq = None # Daily Market Price change
		self.snp = None
		self.dow = None
		self.nasdaq_pct = None # percent change
		self.snp_pct = None # CHANGE TO NICE LOOKING LIST
		self.dow_pct = None
		self.stamps = None
		self.labels = None

		self.fif2hi = None
		self.fif2low = None
		self.fif2change = None

		self.lastHi = None
		self.cap = None
		self.last_fisc_yr = None
		self.profit_margins = None

		# News for the market
		self.bloom_t_1 = None
		self.bloom_t_2 = None
		self.bloom_t_3 = None
		self.bloom_t_4 = None
		self.bloom_cont_1 = None
		self.bloom_cont_2 = None
		self.bloom_cont_3 = None
		self.bloom_cont_4 = None
		self.bloom_url_1 = None
		self.bloom_url_2 = None
		self.bloom_url_3 = None
		self.bloom_url_4 = None

		self.fin_t_t_1 = None
		self.fin_t_t_2 = None
		self.fin_t_t_3 = None
		self.fin_t_t_4 = None
		self.fin_t_cont_1 = None
		self.fin_t_cont_2 = None
		self.fin_t_cont_3 = None
		self.fin_t_cont_4 = None
		self.fin_t_url_1 = None
		self.fin_t_url_2 = None
		self.fin_t_url_3 = None
		self.fin_t_url_4 = None

		self.b_in_t_1 = None
		self.b_in_t_2 = None
		self.b_in_cont_1 = None
		self.b_in_cont_2 = None
		self.b_in_url_1 = None
		self.b_in_url_2 = None
		self.b_in_img_1 = None
		self.b_in_img_2 = None

	def headlines(self):
		B_in = b_in()
		self.b_in_t_1 = B_in[0][0]
		self.b_in_t_2 = B_in[1][0]
		self.b_in_cont_1 = B_in[0][1]
		self.b_in_cont_2 = B_in[1][1]
		self.b_in_url_1 = B_in[0][2]
		self.b_in_url_2 = B_in[1][2]
		self.b_in_img_1 = B_in[0][3]
		self.b_in_img_2 = B_in[1][3]

		Bloom = bloom()
		self.bloom_t_1 = Bloom[0][0]
		self.bloom_t_2 = Bloom[1][0]
		self.bloom_t_3 = Bloom[2][0]
		self.bloom_t_4 = Bloom[3][0]
		self.bloom_cont_1 = Bloom[0][1]
		self.bloom_cont_2 = Bloom[1][1]
		self.bloom_cont_3 = Bloom[2][1]
		self.bloom_cont_4 = Bloom[3][1]
		self.bloom_url_1 = Bloom[0][2]
		self.bloom_url_2 = Bloom[1][2]
		self.bloom_url_3 = Bloom[2][2]
		self.bloom_url_4 = Bloom[3][2]

		Fin_t = fin_t()
		self.fin_t_t_1 = Fin_t[0][0]
		self.fin_t_t_2 = Fin_t[1][0]
		self.fin_t_t_3 = Fin_t[2][0]
		self.fin_t_t_4 = Fin_t[3][0]
		self.fin_t_cont_1 = Fin_t[0][1]
		self.fin_t_cont_2 = Fin_t[1][1]
		self.fin_t_cont_3 = Fin_t[2][1]
		self.fin_t_cont_4 = Fin_t[3][1]
		self.fin_t_url_1 = Fin_t[0][2]
		self.fin_t_url_2 = Fin_t[1][2]
		self.fin_t_url_3 = Fin_t[2][2]
		self.fin_t_url_4 = Fin_t[3][2]



	def market_sum(self):
		file = subprocess.check_output(['ruby', 'data_mine/market_sum.rb'])
		f = json.loads(file)
		
		self.snp = f['result'][0]["regularMarketChange"]["fmt"]
		self.dow = f['result'][1]["regularMarketChange"]["fmt"]
		self.nasdaq = f['result'][2]["regularMarketChange"]["fmt"]
	
		self.snp_pct = f['result'][0]["regularMarketChangePercent"]["fmt"]
		self.dow_pct = f['result'][1]["regularMarketChangePercent"]["fmt"]
		self.nasdaq_pct = self.snp_pct = f['result'][2]["regularMarketChangePercent"]["fmt"]


	def get_name(self, stock):
		# get the company name of the stock

		self.ticker = stock

		with open("names.txt", 'r') as f:
			names = json.load(f)
		f.close()

		# Google has a really weird name no one uses, so I just avoided it...
		if (names[stock]=="GOOG") or (names=="GOOGL"):
			self.company =  "Google"

		#self.company =  re.sub(" Corp*| Inc*| Group| Co", "", names[stock])
		self.company = names[stock]

	def charts(self, _int, _range):
		file =  json.loads(subprocess.check_output(['ruby', 'data_mine/charts.rb', self.ticker, _int, _range]))

		stamps = []
		close = []
		if _range=="1d":
			for t, c in zip(file["result"][0]["timestamp"], file["result"][0]["indicators"]["quote"][0]["close"]):
				t = dt.datetime.fromtimestamp(t)
				if t.minute==0:
					stamps.append(str(t.hour)+":"+str(t.minute)+"0")
				else:
					stamps.append(str(t.hour)+":"+str(t.minute))
				close.append(round(c, 2))

		else:
			for t, c in zip(file["result"][0]["timestamp"], file["result"][0]["indicators"]["quote"][0]["close"]):
				stamps.append(str(dt.datetime.fromtimestamp(t).date()))
				close.append(round(c, 2))
		
		self.labels = stamps
		self.stamps = close


	def analyze(self, stock):
		'''Get various metrics from call to ruby
		'''
		file = subprocess.check_output(['ruby', 'data_mine/stock_sum.rb', stock])

		f = json.loads(file)
		stats = f["defaultKeyStatistics"]
		details = f["summaryDetail"]

		self.fif2hi = details['fiftyTwoWeekHigh']['fmt']
		self.fif2low = details["fiftyTwoWeekLow"]["fmt"]
		self.cap = details["marketCap"]["fmt"]
		self.lastHi = details["dayHigh"]["fmt"]
		self.fif2change = stats["52WeekChange"]["fmt"]	
		self.profit_margins = stats["profitMargins"]["fmt"]

def is_valid(stock):
	stock = stock.strip()
	with open("names.txt", 'r') as f:
		names = json.load(f)
	f.close()

	if stock.lower()=="google":
		return "GOOG"

	for k, v in names.items():
		if k==stock:
			return k
		elif v[:len(stock)]==stock:
			# if it's a company name, return ticket
			return k
	return None







	

