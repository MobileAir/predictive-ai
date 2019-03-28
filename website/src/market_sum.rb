require 'unirest'
require 'json'

def get_summary()
	response = Unirest.get "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-summary?",
  	headers:{
    "X-RapidAPI-Key" => "e22d42b163msh2dd6677c030d9dap18e2b7jsnd6f1f3578a95"
  	},
  	parameters:{
  		"region" => "US",
  		"lang" => "en"
  	}
  	r = JSON.pretty_generate(response.body["marketSummaryResponse"])
  	print(r)
end

get_summary()
