require 'unirest'
require 'json'

def stock_info(stock)
	response = Unirest.get "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/get-detail?",
  headers:{
    "X-RapidAPI-Key" => "c1270becb0msh59ba7b8effef8fcp1185cbjsn138d8347f9ac"
  },
  parameters:{
  	"region" => "US",
  	"lang" => "en",
  	"symbol" => stock
  }
  r = JSON.pretty_generate(response.body)
  print r
end

stock = ARGV[0]
stock_info(stock)
