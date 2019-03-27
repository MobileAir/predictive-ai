from flask import Flask, render_template, request, make_response
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from functools import wraps, update_wrapper
from predictor import Predictor #finds a file that is predictor.py, and then you call the predictor
from analysis import Analyst, is_valid


#load model AT THE BEGINNING
predictor = Predictor()
# create a class for easy data fetching
a = Analyst()
a.market_sum() # get the market prices
a.headlines() # get news headlines
# initialize the flask application
app = Flask(__name__)

'''
@app.route('/')
def home():
	return render_template('base.html', bl_t_1=a.bloom_t_1, bl_t_2=a.bloom_t_2,bl_t_3=a.bloom_t_3,bl_t_4=a.bloom_t_4,\
										bl_c_1=a.bloom_cont_1, bl_c_2=a.bloom_cont_2, bl_c_3=a.bloom_cont_3, bl_c_4=a.bloom_cont_4,\
										bl_u_1=a.bloom_url_1, bl_u_2=a.bloom_url_2, bl_u_3=a.bloom_url_3, bl_u_4=a.bloom_url_4, \
										ft_t_1=a.fin_t_t_1, ft_t_2=a.fin_t_t_2, ft_t_3=a.fin_t_t_3, ft_t_4=a.fin_t_t_4, \
										ft_c_1=a.fin_t_cont_1,ft_c_2=a.fin_t_cont_2, ft_c_3=a.fin_t_cont_3, ft_c_4=a.fin_t_cont_4, \
										ft_u_1=a.fin_t_url_1, ft_u_2=a.fin_t_url_2, ft_u_3=a.fin_t_url_3, ft_u_4=a.fin_t_url_4, \
										bin_t_1=a.b_in_t_1, bin_t_2=a.b_in_t_2, bin_c_1=a.b_in_cont_1, bin_c_2=a.b_in_cont_2,
										bin_u_1=a.b_in_url_1, bin_u_2=a.b_in_url_2, bin_i_1=a.b_in_img_1, bin_i_2=a.b_in_img_2)'''


@app.route('/', methods=['POST', 'GET'])
def home():
	if request.method == "POST": # if you are getting the prediction
		stock = request.form.get('company')
		stock = is_valid(stock) # verify it's a good stock

		# load a new prediction for each company form
		if(stock!=None):
			predictor.predict(stock)
			a.get_name(stock)
			a.analyze(stock)
			a.charts("1d", "3mo")
			labels = a.labels
			stamps = a.stamps
			#stamps= ['2018-12-27', '2018-12-28', '2018-12-31', '2019-01-02', '2019-01-03', '2019-01-04', '2019-01-07', '2019-01-08', '2019-01-09', '2019-01-10', '2019-01-11', '2019-01-14', '2019-01-15', '2019-01-16', '2019-01-17', '2019-01-18', '2019-01-22', '2019-01-23', '2019-01-24', '2019-01-25', '2019-01-28', '2019-01-29', '2019-01-30', '2019-01-31', '2019-02-01', '2019-02-04', '2019-02-05', '2019-02-06', '2019-02-07', '2019-02-08', '2019-02-11', '2019-02-12', '2019-02-13', '2019-02-14', '2019-02-15', '2019-02-19', '2019-02-20', '2019-02-21', '2019-02-22', '2019-02-25', '2019-02-26', '2019-02-27', '2019-02-28', '2019-03-01', '2019-03-04', '2019-03-05', '2019-03-06', '2019-03-07', '2019-03-08', '2019-03-11', '2019-03-12', '2019-03-13', '2019-03-14', '2019-03-15', '2019-03-18', '2019-03-19', '2019-03-20', '2019-03-21', '2019-03-22', '2019-03-25', '2019-03-26', '2019-03-27']
			#labels = [101.18, 100.39, 101.57, 101.12, 97.4, 101.93, 102.06, 102.8, 104.27, 103.6, 102.8, 102.05, 105.01, 105.38, 106.12, 107.71, 105.68, 106.71, 106.2, 107.17, 105.08, 102.94, 106.38, 104.43, 102.78, 105.74, 107.22, 106.03, 105.27, 105.67, 105.25, 106.89, 106.81, 106.9, 108.22, 108.17, 107.15, 109.41, 110.97, 111.59, 112.36, 112.17, 112.03, 112.53, 112.26, 111.7, 111.75, 110.39, 110.51, 112.83, 113.62, 114.5, 114.59, 115.91, 117.57, 117.65, 117.52, 120.22, 117.05, 117.66, 117.91, 116.64]

			return render_template('analysis.html', title=a.ticker, name=a.company, articles=predictor.articles, \
		 			High=predictor.high, Low=predictor.low, Close=predictor.close,\
		 			fif2hi=a.fif2hi, fif2low=a.fif2low, fif2change=a.fif2change,\
		 		 	nas=a.nasdaq, nas_pct=a.nasdaq_pct, snp=a.snp, snp_pct=a.snp_pct, dow=a.dow, dow_pct=a.dow_pct, \
		 		 	stamps=stamps, labels=labels, tweets=predictor.tweet_score, news=predictor.news_score, \
		 		 	cap=a.cap, margin=a.profit_margins)

		else:
			return render_template('base.html', title='home', nas=a.nasdaq, nas_pct=a.nasdaq_pct, snp=a.snp, snp_pct=a.snp_pct, \
			dow=a.dow, dow_pct=a.dow_pct, stock=None, \
			bl_t_1=a.bloom_t_1, bl_t_2=a.bloom_t_2,bl_t_3=a.bloom_t_3,bl_t_4=a.bloom_t_4,\
			bl_c_1=a.bloom_cont_1, bl_c_2=a.bloom_cont_2, bl_c_3=a.bloom_cont_3, bl_c_4=a.bloom_cont_4,\
			bl_u_1=a.bloom_url_1, bl_u_2=a.bloom_url_2, bl_u_3=a.bloom_url_3, bl_u_4=a.bloom_url_4, \
			ft_t_1=a.fin_t_t_1, ft_t_2=a.fin_t_t_2, ft_t_3=a.fin_t_t_3, ft_t_4=a.fin_t_t_4, \
			ft_c_1=a.fin_t_cont_1,ft_c_2=a.fin_t_cont_2, ft_c_3=a.fin_t_cont_3, ft_c_4=a.fin_t_cont_4, \
			ft_u_1=a.fin_t_url_1, ft_u_2=a.fin_t_url_2, ft_u_3=a.fin_t_url_3, ft_u_4=a.fin_t_url_4, \
			bin_t_1=a.b_in_t_1, bin_t_2=a.b_in_t_2, bin_c_1=a.b_in_cont_1, bin_c_2=a.b_in_cont_2,
			bin_u_1=a.b_in_url_1, bin_u_2=a.b_in_url_2, bin_i_1=a.b_in_img_1, bin_i_2=a.b_in_img_2)

	else:
		return render_template('base.html', title='home', nas=a.nasdaq, nas_pct=a.nasdaq_pct, \
			snp=a.snp, snp_pct=a.snp_pct, dow=a.dow, dow_pct=a.dow_pct,stock=None,\
			bl_t_1=a.bloom_t_1, bl_t_2=a.bloom_t_2,bl_t_3=a.bloom_t_3,bl_t_4=a.bloom_t_4,\
			bl_c_1=a.bloom_cont_1, bl_c_2=a.bloom_cont_2, bl_c_3=a.bloom_cont_3, bl_c_4=a.bloom_cont_4,\
			bl_u_1=a.bloom_url_1, bl_u_2=a.bloom_url_2, bl_u_3=a.bloom_url_3, bl_u_4=a.bloom_url_4, \
			ft_t_1=a.fin_t_t_1, ft_t_2=a.fin_t_t_2, ft_t_3=a.fin_t_t_3, ft_t_4=a.fin_t_t_4, \
			ft_c_1=a.fin_t_cont_1,ft_c_2=a.fin_t_cont_2, ft_c_3=a.fin_t_cont_3, ft_c_4=a.fin_t_cont_4, \
			ft_u_1=a.fin_t_url_1, ft_u_2=a.fin_t_url_2, ft_u_3=a.fin_t_url_3, ft_u_4=a.fin_t_url_4, \
			bin_t_1=a.b_in_t_1, bin_t_2=a.b_in_t_2, bin_c_1=a.b_in_cont_1, bin_c_2=a.b_in_cont_2,
			bin_u_1=a.b_in_url_1, bin_u_2=a.b_in_url_2, bin_i_1=a.b_in_img_1, bin_i_2=a.b_in_img_2)


if __name__ == '__main__':
   app.run()


