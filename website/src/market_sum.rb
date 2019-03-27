require 'unirest'
require 'json'

def get_summary()
	response = Unirest.get "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-summary?",
  	headers:{
    "X-RapidAPI-Key" => "c1270becb0msh59ba7b8effef8fcp1185cbjsn138d8347f9ac"
  	},
  	parameters:{
  		"region" => "US",
  		"lang" => "en"
  	}
  	r = JSON.pretty_generate(response.body["marketSummaryResponse"])
  	print(r)
end

get_summary()
