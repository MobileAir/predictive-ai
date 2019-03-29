require 'unirest'
require 'json'

 def getStockNews(stock)
 	response = Unirest.get "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/get-news",

 	headers:{
 		"X-RapidAPI-Key" => "e22d42b163msh2dd6677c030d9dap18e2b7jsnd6f1f3578a95"
 	},
 	parameters:{
 		"region" => "us",
 		"category" => stock
 	}

 	r = JSON.pretty_generate(response.body["items"])
 	print r
end


stock = ARGV[0]
getStockNews(stock)




