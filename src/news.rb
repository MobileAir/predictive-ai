require 'unirest'
require 'json'

 def getStockNews(stock)
 	response = Unirest.get "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/get-news",

 	headers:{
 		"X-RapidAPI-Key" => "284a8b90d5mshdfea6ec830364fbp145a40jsn1964c0508916"
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




