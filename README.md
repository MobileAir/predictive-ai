# Stock-Analysis

The aim of this project was to develop a model predict a stock's market price based off of news articles, tweets, and its past prices. 
It was completed as part of the McGill AI Society's Accelrated ML bootcamp. Checkout their blogpost [here](https://mcgillai.com/). For more project info, look in the deliverables folder.

#### Table of contents:
1. [Data Aquisition](https://github.com/MobileAir/Stock-Analysis/blob/master/README.md#data-mining)
2. [Data Preprocessing](https://github.com/MobileAir/Stock-Analysis/blob/master/README.md#data-preprocessing)
3. [Model](https://github.com/MobileAir/Stock-Analysis/blob/master/README.md#model)
4. [Results](https://github.com/MobileAir/Stock-Analysis/blob/master/README.md#results)
5. [Next Steps](https://github.com/MobileAir/Stock-Analysis/blob/master/README.md#next-steps)

## Data Aquisition

To collect data for each stock, I used pandas datareader, RapidAPI and Twitter to gather stock prices, news, and tweets.

Aquiring stock prices was done with the code below. I was interested in the stock prices from the last 50 days.

```
    prices = pd.datareader.get_data_yahoo(stock, since, today)
```

For this project, I observed four prices: the high, open, low, and close for each of the 50 days.

I collected tweets using Twitter's python library (tweepy). This made it easy to search and collect tweets mentioning a given company and thier stock.

To get news articles I used RapidAPI's Yahoo Finance endpoint. It was an excellent source news as well as stock trends that I included in the website.

 
## Data Preprocessing
There were two central components of in this stage: TextBlob's sentiment polarity and MinMax Scaling.

Textblob's sentiment polarity encoded the tweets and news articles. Their Naive Bayes model uses calculates polarity (in range [-1,1]), to define how "positive" or negative" a text is. Each article and tweet got its own polarity score before being added to the feature matrix.

Here is a glimpse at Bank of America's data:
![](https://github.com/MobileAir/Stock-Analysis/blob/master/.extras/sampData.png)

Lastly, I used sklearn's MinMax scaler to normalize the data before feeding my Neural Network. The algorithm is as follows:
<p align="center">
<img src="https://latex.codecogs.com/gif.latex?x%5E%7B%27%7D%20%3D%20%5Cfrac%7Bx%20-%20min%28x%29%7D%7Bmax%28x%29%20-%20min%28x%29%7D">
</p>

## Model
Finally, I had a nice feature matrix: 49 rows x 6 columns, with each row being one day. It was now time to let my model do some heavy lifting. I obtained the best results using two Gated Recurrent Units followed by a fully connected layer. [Here](https://github.com/MobileAir/Stock-Analysis/blob/master/src/model.py) is the implementation.

Celebrating my Candian heritage I used the <strong>Adam optimizer</strong> to update my parameters.

## Results
This model outperforms the toughest Kaggle competitor (though Kaggle projects used only the stock prices). The tweets and news articles were clearly a welcomed addition! The best error I could find on Kaggle was from Rohit Verma. Checkout his project [here](https://github.com/deadskull7/New-York-Stock-Exchange-Predictions-RNN-LSTM).

|           |    Best on Kaggle    |    This model    |
|-----------|----------------------|------------------|
| Train MSE | 1.91 x 10<sup>-4     | 5.90 x 10<sup>-7 |
| Test MSE  | 3.28 x 10<sup>-4     | 6.21 x 10<sup>-7 |


#### Test MSE on normalized stock prices:

|    High          |    Low           |    Close         |
|------------------|------------------|------------------|
| 6.87 x 10<sup>-7 | 5.81 x 10<sup>-6 | 8.34 x 10<sup>-7 |




## Next Steps

##### 1. Training a more refined NLP classifier for data preprocessing
The polarity score is vague and much too generalized for my data. I would like to add some language processing that would return a score for how the news impacts the stock market, not just if the news sounds good or bad.

##### 2. Exploring other influences
Since the news and tweets boosted the model's performance, I'd love to tap into other news and social media outlets and see if I can improve the predictions.

##### 3. Longer forecast
The model corrently predicts for one day in advance. It would be nice to predict further into the future, though I get the feeling that if that was possible, someone might have beat me to it!


Thanks again to the McGill AI society for a great course
