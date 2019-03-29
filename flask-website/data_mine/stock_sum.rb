require 'unirest'
require 'json'

def stock_info(stock)
	response = Unirest.get "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/get-detail?",
  headers:{
    "X-RapidAPI-Key" => "e22d42b163msh2dd6677c030d9dap18e2b7jsnd6f1f3578a95"
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
