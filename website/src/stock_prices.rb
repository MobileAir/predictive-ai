require 'unirest'
require 'json'

def get_stock_prices(stock, from, today)
	response = Unirest.get "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/get-histories?",
  headers:{
    "X-RapidAPI-Key" => "e22d42b163msh2dd6677c030d9dap18e2b7jsnd6f1f3578a95"
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