require 'unirest'
require 'json'

def get_stock_prices(stock, from, today)
	response = Unirest.get "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/get-histories?",
  headers:{
    "X-RapidAPI-Key" => "284a8b90d5mshdfea6ec830364fbp145a40jsn1964c0508916"
  },
  parameters:{
  	"region" => "us",
  	"lang" => "en",
  	"symbol" => stock,
  	"from" => from,
  	"to" => today,
  	"events" => "div",
  	"interval" => "1d",
  }
  r = JSON.pretty_generate(response.body["chart"]["result"])
  print(r)
end

stock = ARGV[0]
from = ARGV[1]
today = ARGV[2]
get_stock_prices(stock, from, today)