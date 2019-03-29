require 'unirest'
require 'json'

def get_charts(stock, int, range)
	response = Unirest.get "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-charts?",
  	headers:{
    "X-RapidAPI-Key" => "e22d42b163msh2dd6677c030d9dap18e2b7jsnd6f1f3578a95"
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