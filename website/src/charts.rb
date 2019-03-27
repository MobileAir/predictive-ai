require 'unirest'
require 'json'

def get_charts(stock, int, range)
	response = Unirest.get "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-charts?",
  	headers:{
    "X-RapidAPI-Key" => "c1270becb0msh59ba7b8effef8fcp1185cbjsn138d8347f9ac"
  	},
  	parameters:{
  		"region" => "us",
  		"lang" => "en",
  		"symbol" => stock,
  		"interval" => int,
  		"range" => range
  	}
  	r = JSON.pretty_generate(response.body["chart"])
 	print r
end

stock = ARGV[0]
int = ARGV[1]
range = ARGV[2]
get_charts(stock, int, range)