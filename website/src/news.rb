require 'unirest'
require 'json'

 def getStockNews(stock)
 	response = Unirest.get "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/get-news",

 	headers:{
 		"X-RapidAPI-Key" => "c1270becb0msh59ba7b8effef8fcp1185cbjsn138d8347f9ac"
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




