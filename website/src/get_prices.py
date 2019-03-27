import datetime as dt
import pandas as pd
import subprocess
import json

def get_history(stock):
	today = str(int(dt.datetime.now().timestamp()))

	since = dt.datetime.today() - dt.timedelta(days=75)
	since = str(int(since.timestamp()))


	file = subprocess.check_output(['ruby', 'stock_prices.rb', stock, since, today])

	f = json.loads(file)
	try:
		dates = []
		for time in f[0]["timestamp"]:
			dates.append(dt.datetime.fromtimestamp(time).date())

		data = {"Date": dates, "High": f[0]["indicators"]["quote"][0]["high"], "Low":f[0]["indicators"]["quote"][0]["low"], \
		 		"Open": f[0]["indicators"]["quote"][0]["open"], "Close": f[0]["indicators"]["quote"][0]["close"]}

		df = pd.DataFrame(data)
		df.to_csv("../data/train_data/"+stock+"_0.csv")
	except KeyError:
		print("Key error at: {}".format(stock))


with open("../data/names.txt", "r") as f:
	names = json.load(f)
	for k,v in names.items():
		try:
			get_history(k)
		except subprocess.CalledProcessError:
			continue
