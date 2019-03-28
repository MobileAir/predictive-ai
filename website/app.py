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
			labels3 = a.labels
			stamps3 = a.stamps
			a.charts("15m", "1d")
			labels1 = a.labels
			stamps1 = a.stamps
			a.charts("1wk", "1y")
			labelsyr = a.labels
			stampsyr = a.stamps

			return render_template('analysis.html', title=a.ticker, name=a.company, articles=predictor.articles, \
		 			High=predictor.high, Low=predictor.low, Close=predictor.close,\
		 			fif2hi=a.fif2hi, fif2low=a.fif2low, fif2change=a.fif2change,\
		 		 	nas=a.nasdaq, nas_pct=a.nasdaq_pct, snp=a.snp, snp_pct=a.snp_pct, dow=a.dow, dow_pct=a.dow_pct, \
		 		 	labels3=labels3, data3=stamps3, labels1=labels1, data1=stamps1, labelsy=labelsyr, datay=stampsyr, \
		 		 	tweets=predictor.tweet_score, news=predictor.news_score, cap=a.cap, margin=a.profit_margins)

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


